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

    def get_queryset(self):
        qs = super().get_queryset()
        client = self.request.GET.get('client', None)
        if client:
            qs = qs.filter(client__id=client)
        return qs


class SerialKeyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = video_models.KeyStorage.objects.all()
    serializer_class = serializers.ListSerialKeySerializer
    pagination_class = DatatablesPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('request_id')
        client = self.request.GET.get('client', None)
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        if client:
            queryset = queryset.filter(product__client__id=client)
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
        client = self.request.GET.get('client')
        if not client:
            qs = video_models.Product.objects.none()
        elif not param:
            qs = video_models.Product.objects.filter(client__id=client)
        else:
            try:
                int(param)
                qs = video_models.Product.objects.filter(Q(id=param) | Q(name__icontains=param),
                                                         client__id=client)
            except ValueError:
                qs = video_models.Product.objects.filter(name__icontains=param, client__id=client)

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


class UpdateSerialKeyView(APIView):
    def post(self, request, pk):
        serializer = serializers.UpdateSerialKeyViewSerializer(data=self.request.data)
        if not serializer.is_valid():
            return JsonResponse({"message": serializer.errors}, status=400)

        validated_data = serializer.validated_data
        try:
            key = video_models.KeyStorage.objects.get(key=pk)
        except video_models.KeyStorage.DoesNotExist:
            return JsonResponse({"message": "Invalid key"}, status=400)

        if key.status == "REVOKED":
            return JsonResponse({"message": "Key is already revoked"}, status=400)
        key.__dict__.update(validated_data)
        key.save()
        return JsonResponse({"message": "Key updated successfully"}, status=200)
