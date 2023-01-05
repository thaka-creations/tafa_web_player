from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from video import models as video_models
from . import serializers


# todo : add user
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = video_models.Product.objects.all()
    serializer_class = serializers.ListProductSerializer
    pagination_class = DatatablesPageNumberPagination


class SerialKeyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = video_models.KeyStorage.objects.all()
    serializer_class = serializers.ListSerialKeySerializer
    pagination_class = DatatablesPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('request_id')
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        return queryset


class ProductContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = video_models.Video.objects.all()
    serializer_class = serializers.ListProductContentSerializer
    pagination_class = DatatablesPageNumberPagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(product__id=self.request.GET.get('request_id'))
        return super(ProductContentViewSet, self).list(request, *args, **kwargs)


class SearchProductView(APIView):
    def get(self, request):
        param = self.request.GET.get("q")
        if not param:
            qs = video_models.Product.objects.all()
        else:
            try:
                int(param)
                qs = video_models.Product.objects.filter(Q(id=param) | Q(name__icontains=param))
            except ValueError:
                qs = video_models.Product.objects.filter(name__icontains=param)

        return JsonResponse({"results": serializers.SearchProductSerializer(qs, many=True).data})


class SearchVideoView(APIView):
    def get(self, request):
        param = self.request.GET.get("q")
        product_id = self.request.GET.get("product_id")
        if not product_id:
            qs = video_models.Video.objects.none()
        else:
            if not param:
                qs = video_models.Video.objects.filter(product__id=product_id)
            else:
                qs = video_models.Video.objects.filter(
                    name__icontains=param, product__id=product_id)
        return JsonResponse({"results": serializers.SearchVideoSerializer(qs, many=True).data})
