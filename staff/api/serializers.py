from datetime import datetime

from rest_framework import serializers
from video import models as video_models


class ListProductSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    class Meta:
        model = video_models.Product
        fields = [
            'DT_RowId', 'DT_RowAttr', 'id', 'name', 'title', 'short_description',
            'long_description'
        ]

    @staticmethod
    def get_DT_RowId(obj):
        return obj.id

    @staticmethod
    def get_DT_RowAttr(obj):
        return {'pk': obj.id}


class ListSerialKeySerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = video_models.KeyStorage
        fields = ['DT_RowId', 'DT_RowAttr', 'key', 'product', 'product_name', 'validity', 'status']

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
