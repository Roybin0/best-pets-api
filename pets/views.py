from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pet
from .serializers import PetSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetList(APIView):
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(
            pets, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PetSerializer(
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


class PetDetail(APIView):
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            pet = Pet.objects.get(pk=pk)
            self.check_object_permissions(self.request, pet)
            return pet
        except Pet.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetSerializer(
            pet, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetSerializer(
            pet, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pet = self.get_object(pk)
        pet.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )