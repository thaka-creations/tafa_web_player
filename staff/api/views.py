from rest_framework import viewsets
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from video import models as video_models
from . import serializers


# add user
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = video_models.Product.objects.all()
    serializer_class = serializers.ListProductSerializer
    pagination_class = DatatablesPageNumberPagination
