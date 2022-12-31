import base64

from django.db import transaction
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import utils, serializers as video_serializers, models as video_models


class VideoViewSet(viewsets.ViewSet):
    @action(
        methods=['POST'],
        detail=False,
        url_path='keygen',
        url_name='keygen'
    )
    def keygen(self, request):
        # key generation
        time_stamp, key = utils.numeric_keygen()
        # save key
        video_models.KeyStorage.objects.create(
            key=key,
            time_stamp=time_stamp
        )
        return Response({"details": key}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='activate-key',
        url_name='activate-key'
    )
    def activate_key(self, request):
        # key activation
        serializer = video_serializers.ActivateKeySerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        key = serializer.validated_data.get('key')
        if not video_models.KeyStorage.objects.filter(key=key.encode()).exists():
            return Response({"message": "Invalid key"}, status=status.HTTP_400_BAD_REQUEST)

        # activate key
        qs = video_models.KeyStorage.objects.filter(key=key.encode())
        qs.update(activated=True)
        instance = qs.first()
        return Response({"message": video_serializers.KeyDetailSerializer(instance, context=key).data},
                        status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='encrypt-file',
        url_name='encrypt-file'
    )
    def encrypt_file(self, request):
        # encrypt file
        serializer = video_serializers.EncryptDecryptFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        resp = utils.encrypt_file(serializer.validated_data['key'])
        if not resp:
            return Response({"message": "Error encrypting file"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "File encrypted successfully"}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='decrypt-file',
        url_name='decrypt-file'
    )
    def decrypt_file(self, request):
        # decrypt file
        serializer = video_serializers.EncryptDecryptFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        resp = utils.decrypt_file(serializer.validated_data['key'])
        if not resp:
            return Response({"message": "Error decrypting file"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "File decrypted successfully"}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='add-watermark',
        url_name='add-watermark'
    )
    def add_watermark(self, request):
        # add watermark
        resp = utils.add_watermark()
        if not resp:
            return Response({"message": "Error adding watermark"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Watermark added successfully"}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='app-registered',
        url_name='app-registered'
    )
    def app_registered(self, request):
        payload_serializer = video_serializers.AppRegisteredSerializer(data=request.data)
        if not payload_serializer.is_valid():
            return Response({"message": payload_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = payload_serializer.validated_data

        created, _ = video_models.AppModel.objects.get_or_create(
            serial_number=validated_data['serial_number'])

        serializer = video_serializers.AppRegisteredSerializer(created, many=False)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = video_models.Product.objects.all()
    serializer_class = video_serializers.ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = utils.keygen()
        if not resp:
            return Response({"message": "Error creating product"}, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        video_models.Product.objects.create(**validated_data, encryptor=resp)
        return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)









