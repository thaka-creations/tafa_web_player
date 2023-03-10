from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users import utils as user_utils

from . import utils, serializers as video_serializers, models as video_models


class VideoViewSet(viewsets.ViewSet):
    @action(
        methods=['POST'],
        detail=False,
        url_path='list-client-keys'
    )
    def list_client_keys(self, request):
        payload = request.data
        username = payload['username']
        password = payload['JWTAUTH']
        request_id = payload['request_id']

        # try to authenticate user
        user = authenticate(username=username, password=password)
        if not user or user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        keys = list(video_models.KeyStorage.objects.filter(
            client=user, status="ACTIVE").exclude(app__id=request_id).values_list(
            'key', flat=True))
        return Response({"message": keys}, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
        url_path='list-app-keys',
    )
    def list_app_keys(self, request):
        keys = list(video_models.KeyStorage.objects.filter(
            app__id=self.request.query_params.get('request_id'), status="ACTIVE").values_list(
            'key', flat=True))
        return Response({"message": keys}, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['GET'],
            url_name='list-numeric-keys',
            url_path='list-numeric-keys')
    def list_numeric_keys(self, request):
        qs = video_models.KeyStorage.objects.all()
        serializer = video_serializers.ListNumericKeySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='keygen',
        url_name='keygen'
    )
    def keygen(self, request):
        payload = request.data
        serializer = video_serializers.NumericKeyGenSerializer(data=payload)
        if not serializer.is_valid():
            return Response({"message": user_utils.format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        quantity = validated_data['quantity']
        product = validated_data['product']
        expires_at = validated_data['expires_at']
        validity = validated_data['validity']
        watermark = validated_data['watermark']
        second_screen = validated_data['second_screen']
        videos = validated_data['videos']
        user = validated_data['user']

        # key generation
        resp = utils.numeric_keygen(quantity)

        with transaction.atomic():
            # save key
            for i in resp:
                instance = video_models.KeyStorage.objects.create(
                    key=i['key'],
                    time_stamp=i['time_stamp'],
                    product=product,
                    expires_at=expires_at,
                    validity=validity,
                    watermark=watermark,
                    second_screen=second_screen,
                    user=user
                )
                if bool(videos):
                    instance.videos.set(videos)

        return Response({"message": "Serial key(s) generated successfully"}, status=status.HTTP_200_OK)

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

        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)

        if not user or user is None:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_403_FORBIDDEN)

        if not user.phone_verified:
            return Response({"message": "Phone number not verified"}, status=status.HTTP_403_FORBIDDEN)

        if user.account_status != "ACTIVE":
            return Response({"message": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)

        try:
            instance = video_models.KeyStorage.objects.get(key=validated_data['key'])
        except video_models.KeyStorage.DoesNotExist:
            return Response({"message": "Invalid key"}, status=status.HTTP_400_BAD_REQUEST)

        if instance.expires_at < utils.get_date():
            return Response({"message": "Key has expired"}, status=status.HTTP_400_BAD_REQUEST)

        if instance.activated:
            return Response({"message": "Key has already been activated"}, status=status.HTTP_400_BAD_REQUEST)

        instance.activated = True
        instance.status = "ACTIVE"
        instance.client = user
        instance.app_id = validated_data['app_id']
        instance.date_activated = timezone.now()
        instance.save()

        return Response({"message": video_serializers.KeyDetailSerializer(instance).data},
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
            serial_number=validated_data['serial_number'], model_name=validated_data['model_name'],
            encryptor=validated_data.get('encryptor', False)
        )

        serializer = video_serializers.AppRegisteredSerializer(created, many=False)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='add-video',
        url_name='add-video'
    )
    def add_video(self, request):
        serializer = video_serializers.CreateVideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        file_list = validated_data['file_list']
        product = validated_data['product']

        with transaction.atomic():
            data = []
            for i in file_list:
                instance = video_models.Video.objects.create(
                    product=product,
                    name=i['name'],
                    file_extension=i['extension'],
                    file_size=i['size'],
                    duration=i['duration'],
                )
                data.append({
                    "video_id": str(instance.id),
                    "file_path": i['file_path'],
                    "name": instance.name
                })

            return Response({"message": data}, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
        url_path='player-version',
        url_name='player-version'
    )
    def player_version(self, request):
        qs = video_models.AppVersion.objects.filter(app_type='player').order_by('-created_at')
        if not qs.exists():
            return Response({"version": "1.0.0"}, status=status.HTTP_200_OK)
        instance = qs.first()
        return Response({"version": instance.version}, status=status.HTTP_200_OK)



class ProductViewSet(viewsets.ModelViewSet):
    queryset = video_models.Product.objects.all()
    serializer_class = video_serializers.ProductSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(client=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(user_utils.format_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        resp = utils.keygen()
        if not resp:
            return Response({"message": "Error creating product"}, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        with transaction.atomic():
            video_models.Product.objects.create(
                **validated_data, encryptor=resp, client=request.user)
            return Response("Product created successfully", status=status.HTTP_200_OK)


class ListProductVideoApiView(APIView):

    def get(self, request):
        try:
            product = video_models.Product.objects.get(id=self.request.GET.get('request_id'))
        except video_models.Product.DoesNotExist:
            return Response({"message": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = video_serializers.ListProductVideoSerializer(product.product_videos.all(), many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)



