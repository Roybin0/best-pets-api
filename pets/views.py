from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pet
from .serializers import PetSerializer


class PetList(APIView):
    def get(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(
            pets, many=True, context={'request': request}
        )
        return Response(serializer.data)

