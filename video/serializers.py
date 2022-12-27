from rest_framework import serializers


class EncryptDecryptFileSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)


class ActivateKeySerializer(serializers.Serializer):
    key = serializers.CharField(required=True)


class AppRegisteredSerializer(serializers.Serializer):
    serial_number = serializers.CharField(required=True)
