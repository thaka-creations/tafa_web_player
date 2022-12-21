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
        try:
            utils.keygen()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Key generated successfully"}, status=status.HTTP_200_OK)

