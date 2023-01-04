from datetime import datetime, timedelta
from rest_framework import serializers

from video.models import AppModel, KeyStorage, Product, Video


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
    videos = serializers.SerializerMethodField()

    class Meta:
        model = KeyStorage
        fields = ['key', 'encryption_key', 'watermark', 'activated', 'expires_at', 'second_screen', 'product_name',
                  'product_id', 'videos']

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

    @staticmethod
    def get_videos(obj):
        if not obj.videos.exists():
            return "all"
        return list(obj.videos.values_list('id', flat=True))


class ProductSerializer(serializers.ModelSerializer):
    encryption_key = serializers.SerializerMethodField()
    title = serializers.CharField(required=True)
    short_description = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'encryptor', 'encryption_key', 'title', 'short_description', 'long_description']
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
    videos = serializers.ListField(child=serializers.CharField(), required=True)

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

        # validate videos
        videos = attrs['videos']
        if videos == ['all']:
            videos = None
        else:
            videos = Video.objects.filter(id__in=videos)
            if len(videos) != len(attrs['videos']):
                raise serializers.ValidationError('Some of the videos do not exist')
        attrs.update({'expires_at': expires_at, 'product': product, 'videos': videos})
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


class VideoFileSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    size = serializers.CharField(required=True)
    extension = serializers.CharField(required=True)
    duration = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    file_path = serializers.CharField(required=True)


class CreateVideoSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    file_list = serializers.ListField(child=VideoFileSerializer(), allow_empty=False)

    def validate(self, attrs):
        try:
            product = Product.objects.get(id=attrs['product'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        attrs.update({'product': product})
        return attrs


class ListProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'name',
            'file_extension',
            'file_size',
            'duration',
        ]
