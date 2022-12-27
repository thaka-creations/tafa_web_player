from rest_framework import serializers
from video.models import AppModel


class EncryptDecryptFileSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)


class ActivateKeySerializer(serializers.Serializer):
    key = serializers.CharField(required=True)


class AppRegisteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}}

