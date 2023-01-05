from django.db.models import Q
from rest_framework import serializers
from users import models as user_models
from phonenumbers.phonenumberutil import is_possible_number
from phonenumber_field.phonenumber import to_python


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)  # username is email
    first_name = serializers.CharField(required=True, trim_whitespace=True)
    last_name = serializers.CharField(required=True, trim_whitespace=True)
    middle_name = serializers.CharField(required=True, trim_whitespace=True,
                                        allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=True)
    confirm_password = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        username = attrs['username']
        phone = attrs['phone']
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if user_models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with email already exists")

        if user_models.User.objects.filter(phone=phone, phone_verified=True).exists():
            raise serializers.ValidationError("User with phone number already exists")

        try:
            phone_number = to_python(phone, "KE")

            if phone_number and not is_possible_number(phone_number) or not phone_number.is_valid():
                raise serializers.ValidationError("Enter a valid phone number")
        except Exception:
            raise serializers.ValidationError("Enter a valid phone number")

        if password != confirm_password:
            raise serializers.ValidationError("Password do not match")

        attrs.pop('confirm_password')
        return attrs


class VerifyOtpCodeSerializer(serializers.Serializer):
    send_to = serializers.CharField(required=True, trim_whitespace=True)
    otp = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        phone = attrs['send_to']
        otp = attrs['otp']

        try:
            user = user_models.User.objects.get(phone=phone, phone_verified=False)
        except user_models.User.DoesNotExist:
            raise serializers.ValidationError("User with phone number does not exist")

        if not user.otp_code == otp:
            raise serializers.ValidationError("Invalid OTP code")

        return attrs


class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=True)

