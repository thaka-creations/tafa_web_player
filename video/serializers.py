from datetime import datetime, timedelta
from rest_framework import serializers

from video.models import AppModel, KeyStorage, Product


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
    encryption_key = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = KeyStorage
        fields = ['key', 'encryption_key', 'watermark', 'activated', 'expires_at', 'second_screen', 'product_name',
                  'product_id']

    @staticmethod
    def get_encryption_key(obj):
        return obj.product.encryptor[2:-1]

    @staticmethod
    def get_product_name(obj):
        try:
            return obj.product.name
        except AttributeError:
            return None

    @staticmethod
    def get_product_id(obj):
        try:
            return obj.product.id
        except AttributeError:
            return None


class ProductSerializer(serializers.ModelSerializer):
    encryption_key = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'encryptor', 'encryption_key']
        extra_kwargs = {
            'id': {'read_only': True}, 'encryption_key': {'read_only': True}}

    @staticmethod
    def get_encryption_key(obj):
        return obj.encryptor[2:-1]


class NumericKeyGenSerializer(serializers.Serializer):
    validity_choices = [
        ('1', '1 day'),
        ('7', '7 days'),
        ('30', '1 month'),
        ('60', '2 months'),
        ('365', '1 year'),
        ('730', '2 years'),
        ('Unlimited', 'Unlimited')
    ]
    quantity = serializers.IntegerField(required=True, min_value=1, max_value=1000)
    product = serializers.IntegerField(required=True)
    validity = serializers.ChoiceField(choices=validity_choices, required=True)
    watermark = serializers.CharField(allow_blank=True, allow_null=True, required=True)
    second_screen = serializers.BooleanField(default=True)

    def validate(self, attrs):
        try:
            product = Product.objects.get(id=attrs['product'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')

        # expires at
        if attrs['validity'] == 'Unlimited':
            expires_at = None
        else:
            expires_at = datetime.now() + timedelta(days=int(attrs['validity']))
            expires_at = expires_at.strftime('%Y-%m-%d')
        attrs.update({'expires_at': expires_at, 'product': product})
        return attrs


class ListNumericKeySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()

    class Meta:
        model = KeyStorage
        fields = ['id', 'key', 'product', 'expires_at', 'activated', 'watch_time', 'second_screen', 'validity',
                  'watermark']

    @staticmethod
    def get_product(obj):
        try:
            return obj.product.name
        except AttributeError:
            return None

    @staticmethod
    def get_expires_at(obj):
        if obj.expires_at:
            return obj.expires_at.strftime('%Y-%m-%d')
        return None
