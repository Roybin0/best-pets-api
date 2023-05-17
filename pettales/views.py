from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetTale
from .serializers import PetTaleSerializer


class PetTaleList(APIView):
    def get(self, request):
        pettales = PetTale.objects.all()
        serializer = PetTaleSerializer(
            pettales, many=True, context={'request': request}
        )
        return Response(serializer.data)
