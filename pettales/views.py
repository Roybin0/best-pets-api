from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetTale
from .serializers import PetTaleSerializer


class PetTaleList(APIView):
    serializer_class = PetTaleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    
    def get(self, request):
        pettales = PetTale.objects.all()
        serializer = PetTaleSerializer(
            pettales, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PetTaleSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
