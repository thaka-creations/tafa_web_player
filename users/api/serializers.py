from rest_framework import serializers
from users import models as user_models


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)  # username is email
    first_name = serializers.CharField(required=True, trim_whitespace=True)
    last_name = serializers.CharField(required=True, trim_whitespace=True)
    middle_name = serializers.CharField(required=True, trim_whitespace=True,
                                        allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        username = attrs['username']
        phone = attrs['phone']

        if user_models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with email already exists")

        if user_models.User.objects.filter(phone=phone, phone_verified=True).exists():
            raise serializers.ValidationError("User with phone number already exists")

        return attrs

