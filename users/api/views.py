import requests
from django.contrib.auth import authenticate
from django.db import transaction
from oauth2_provider.models import get_application_model
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from users.api import serializers as user_serializers
from users import models as user_models
from users import utils as user_utils


oauth2_user = user_utils.ApplicationUser()


class RegisterUserView(APIView):
    @staticmethod
    def post(request):
        serializer = user_serializers.RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        password = validated_data.pop('password')

        with transaction.atomic():
            # create user
            user = user_models.User.objects.create(**validated_data)
            user.set_password(password)
            user.save()

            # create public user
            user_models.PublicUser.objects.create(user=user)

            # create oauth2 user
            oauth2_user.create_application_user(user)

            url = 'https://tafa.co.ke/mfa/otp/generate'
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

            return Response({"message": "Successfully registered. Otp has been sent to your phone"},
                            status=status.HTTP_200_OK)


class VerifyOtpCodeView(APIView):
    def post(self, request):
        serializer = user_serializers.VerifyOtpCodeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        phone = validated_data['phone']
        code = validated_data['code']
        status_code, response = user_utils.verify_otp(code, phone)

        if not status_code:
            return Response({"message": response}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": response}, status=status.HTTP_200_OK)


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
            return Response({"message": "Verify phone number first"}, status=status.HTTP_400_BAD_REQUEST)

        if user.account_status != "ACTIVE":
            return Response({"message": "Your account has been {}".format(user.account_status.lower())},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = get_application_model().objects.get(user=user)
        except get_application_model().DoesNotExist:
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
            "jwt_token": oauth2_user.generate_jwt_token(user)
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












