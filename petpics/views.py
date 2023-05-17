from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetPic
from .serializers import PetPicSerializer


class PetPicList(APIView):
    def get(self, request):
        petpics = PetPic.objects.all()
        serializer = PetPicSerializer(
            petpics, many=True, context={'request': request}
        )
        return Response(serializer.data)