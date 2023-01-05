from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.serializers import RegisterUserSerializer
from users import models as user_models


class RegisterUserView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        with transaction.atomic():
            user = user_models.User.objects.create(**validated_data)

            # create public user
            user_models.PublicUser.objects.create(user=user)



