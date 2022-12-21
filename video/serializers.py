from rest_framework import serializers


class EncryptDecryptFileSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
