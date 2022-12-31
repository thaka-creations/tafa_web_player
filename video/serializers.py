import base64

from rest_framework import serializers

from video.models import AppModel, KeyStorage


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


class KeyDetailSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = KeyStorage
        fields = '__all__'

    def get_key(self, obj):
        return self.context


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {'read_only': True}}
