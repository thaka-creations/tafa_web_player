import requests
from django.contrib.auth import authenticate
from django.db import transaction
from oauth2_provider.models import get_application_model
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.api import serializers as user_serializers
from users import models as user_models
from users import utils as user_utils


oauth2_user = user_utils.ApplicationUser()


class RegisterUserView(APIView):
    @staticmethod
    def post(request):
        serializer = user_serializers.RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": user_utils.format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        password = validated_data.pop('password')
        is_staff = validated_data.pop('is_staff')

        with transaction.atomic():
            # create user
            user = user_models.User.objects.create(**validated_data)
            user.set_password(password)

            if is_staff:
                user.is_staff = True
                user_models.Staff.objects.create(user=user)
            else:
                # create public user
                user_models.PublicUser.objects.create(user=user)

            user.save()
            # create oauth2 user
            oauth2_user.create_application_user(user)

            url = 'https://tafa.co.ke/api/v1/mfa/otp/generate'
            payload = {
                "expiry_time": 600,
                "send_to": user.phone
            }
            try:
                response = requests.post(url, json=payload)
            except requests.exceptions.ConnectionError:
                transaction.set_rollback(True)
                return Response({"message": "Could not connect to server. Try again later"},
                                status=status.HTTP_400_BAD_REQUEST)

            if response.status_code != 200:
                transaction.set_rollback(True)
                return Response({"message": "An error occurred. Try again later"},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": str(user.id)},
                            status=status.HTTP_200_OK)


class VerifyOtpCodeView(APIView):
    def post(self, request):
        serializer = user_serializers.VerifyOtpCodeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({"message": user_utils.format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        phone = validated_data['phone']
        code = validated_data['code']
        user = validated_data['send_to']
        status_code, response = user_utils.verify_otp(code, phone)

        if not status_code:
            return Response({"message": response}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user.phone_verified = True
            user.account_status = "ACTIVE"
            user.save()

            # check if user is staff or public user
            if hasattr(user, 'staff_user'):
                user.staff_user.profile_status = "ACTIVE"
                user.staff_user.save()
            else:
                user.public_user.profile_status = "ACTIVE"
                user.public_user.save()

        return Response({"message": response}, status=status.HTTP_200_OK)


class ResendOtpCodeView(APIView):
    def post(self, request):
        serializer = user_serializers.ResendOtpCodeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({"message": user_utils.format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        phone = validated_data['phone']

        url = 'https://tafa.co.ke/api/v1/mfa/otp/generate'
        payload = {
            "expiry_time": 600,
            "send_to": phone
        }

        try:
            response = requests.post(url, json=payload)
        except requests.exceptions.ConnectionError:
            return Response({"message": "Could not connect to server. Try again later"},
                            status=status.HTTP_400_BAD_REQUEST)

        if response.status_code != 200:
            return Response({"message": "An error occurred. Try again later"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OTP code sent successfully"}, status=status.HTTP_200_OK)


class AuthenticationViewSet(viewsets.ViewSet):
    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = user_serializers.LoginViewSerializer(
            data=self.request.data, many=False
        )

        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']

        user = authenticate(username=username, password=password)

        if not user or user is None:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.phone_verified:
            return Response({"message": "Verify phone number first", "user": str(user.id)},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.account_status != "ACTIVE":
            return Response({"message": "Your account has been {}".format(user.account_status.lower())},
                            status=status.HTTP_400_BAD_REQUEST)

        if "usertype" in validated_data.keys():
            usertype = validated_data['usertype']
            if usertype == 'staff':
                if not user.is_staff:
                    return Response({"message": "Unauthorized. User is not a staff member"},
                                    status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_application_model().objects.get(user=user)
        except get_application_model().DoesNotExist:
            print("these")
            return Response({"message": "Invalid client"}, status=status.HTTP_400_BAD_REQUEST)

        dt = {
            "grant_type": "password",
            "username": user.username,
            "password": password,
            "client_id": instance.client_id,
            "client_secret": instance.client_secret
        }

        response = oauth2_user.get_client_details(dt)

        if not response:
            return Response({"message": "Invalid client"}, status=status.HTTP_400_BAD_REQUEST)

        userinfo = {
            "access_token": response['access_token'],
            "expires_in": response['expires_in'],
            "token_type": response['token_type'],
            "refresh_token": response['refresh_token'],
            "jwt_token": oauth2_user.generate_jwt_token(user),
            "name": user.first_name + " " + user.last_name,
            "phone": user.phone,
        }

        return Response({"message": userinfo}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        authorization_token = request.headers.get('Authorization', b'')
        auth_token = authorization_token.split()
        logged_in_user = request.user
        status_code, resp = oauth2_user.logout(auth_token[1], logged_in_user)

        if not status_code:
            return Response({"message": resp}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": resp}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['user_details', 'get_user_details']:
            return user_serializers.UserProfileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='user-details')
    def user_details(self, request):
        serializer = self.get_serializer(request.user)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='get-user-details')
    def get_user_details(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"message": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = user_models.User.objects.get(id=user_id)
        except user_models.User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)












