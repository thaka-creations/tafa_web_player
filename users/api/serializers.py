from django.db.models import Q
from rest_framework import serializers
from users import models as user_models
from phonenumbers.phonenumberutil import is_possible_number
from phonenumber_field.phonenumber import to_python


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # username is email
    first_name = serializers.CharField(required=True, trim_whitespace=True)
    last_name = serializers.CharField(required=True, trim_whitespace=True)
    phone = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=True)
    confirm_password = serializers.CharField(required=True, trim_whitespace=True)
    is_staff = serializers.BooleanField(default=False)

    def validate(self, attrs):
        email = attrs['email']
        phone = attrs['phone']
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if user_models.User.objects.filter(username=email).exists():
            raise serializers.ValidationError("User with email already exists")

        # if user_models.User.objects.filter(phone=phone, phone_verified=True).exists():
        #     raise serializers.ValidationError("User with phone number already exists")

        try:
            phone_number = to_python(phone, "KE")

            if phone_number and not is_possible_number(phone_number) or not phone_number.is_valid():
                raise serializers.ValidationError("Enter a valid phone number")
        except Exception:
            raise serializers.ValidationError("Enter a valid phone number")

        if password != confirm_password:
            raise serializers.ValidationError("Password do not match")

        attrs.pop('confirm_password')
        attrs['username'] = attrs.pop('email')

        return attrs


class ResendOtpCodeSerializer(serializers.Serializer):
    send_to = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        send_to = attrs['send_to']

        try:
            user = user_models.User.objects.get(id=send_to)
        except user_models.User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        attrs['send_to'] = user
        attrs['phone'] = user.phone

        return attrs


class VerifyOtpCodeSerializer(ResendOtpCodeSerializer):
    code = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=True)

