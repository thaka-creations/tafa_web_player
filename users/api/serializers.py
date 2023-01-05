from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, trim_whitespace=True)
    last_name = serializers.CharField(required=True, trim_whitespace=True)
    middle_name = serializers.CharField(required=True, trim_whitespace=True,
                                        allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=True, trim_whitespace=True)

    def validate(self, attrs):
        email = attrs['email']
