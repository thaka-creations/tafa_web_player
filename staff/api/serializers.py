from rest_framework import serializers
from video import models as video_models


class ListProductSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()

    class Meta:
        model = video_models.Product
        fields = [
            'DT_RowId', 'DT_RowAttr', 'name'
        ]

    @staticmethod
    def get_DT_RowId(obj):
        return obj.id

    @staticmethod
    def get_DT_RowAttr(obj):
        return {'pk': obj.id}
