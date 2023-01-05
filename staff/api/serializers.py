from datetime import datetime
from django.utils import timezone

from rest_framework import serializers
from video import models as video_models


class ListProductSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = video_models.Product
        fields = [
            'DT_RowId', 'DT_RowAttr', 'id', 'name', 'title', 'short_description',
            'long_description', 'created_at'
        ]

    @staticmethod
    def get_DT_RowId(obj):
        return obj.id

    @staticmethod
    def get_DT_RowAttr(obj):
        return {'pk': obj.id}

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime('%b %d, %Y %H:%M:%S')


class ListSerialKeySerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    access_status = serializers.SerializerMethodField()

    class Meta:
        model = video_models.KeyStorage
        fields = ['DT_RowId', 'DT_RowAttr', 'key', 'product', 'product_name', 'validity', 'status',
                  'created_at', 'access_status']

    @staticmethod
    def get_DT_RowId(obj):
        return obj.id

    @staticmethod
    def get_DT_RowAttr(obj):
        return {'pk': obj.id}

    @staticmethod
    def get_product_name(obj):
        try:
            return obj.product.name
        except AttributeError:
            return ''

    @staticmethod
    def get_status(obj):
        if bool(obj.expires_at):
            if obj.expires_at < datetime.now().date():
                return 'Expired'
        if obj.activated:
            return 'Activated'
        else:
            return 'Open'

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime('%b %d, %Y %H:%M:%S')

    @staticmethod
    def get_access_status(obj):
        if obj.videos.exists():
            return 'Selected'
        else:
            return 'All'


class SearchProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = video_models.Product
        fields = ['id', 'name']

    @staticmethod
    def get_name(obj):
        return obj.name + " (" + str(obj.id) + ")"


class SearchVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = video_models.Video
        fields = ['id', 'name']


class ListProductContentSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = video_models.Video
        fields = ['name', 'file_size', 'file_extension', 'duration', 'created_at', 'DT_RowId', 'DT_RowAttr']

    @staticmethod
    def get_DT_RowId(obj):
        return obj.id

    @staticmethod
    def get_DT_RowAttr(obj):
        return {'pk': obj.id}

    @staticmethod
    def get_file_extension(obj):
        return obj.file_extension[1:]

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime('%b %d, %Y %H:%M:%S')

