from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import utils


class VideoViewSet(viewsets.ViewSet):
    @action(
        methods=['POST'],
        detail=False,
        url_path='keygen',
        url_name='keygen'
    )
    def keygen(self, request):
        # key generation
        resp = utils.keygen()
        if not resp:
            return Response({"message": "Error generating key"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"key": str(resp)}, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        url_path='encrypt-file',
        url_name='encrypt-file'
    )
    def encrypt_file(self, request):
        # encrypt file
        resp = utils.encrypt_file(request.data['key'])
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
        resp = utils.decrypt_file(request.data['key'])
        if not resp:
            return Response({"message": "Error decrypting file"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "File decrypted successfully"}, status=status.HTTP_200_OK)

