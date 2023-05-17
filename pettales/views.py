from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetTale
from .serializers import PetTaleSerializer
from bp_api.permissions import IsOwnerOrReadOnly


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


class PetTaleDetail(APIView):
    serializer_class = PetTaleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            pettale = PetTale.objects.get(pk=pk)
            self.check_object_permissions(self.request, pettale)
            return pettale
        except PetTale.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pettale = self.get_object(pk)
        serializer = PetTaleSerializer(
            pettale, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        pettale = self.get_object(pk)
        serializer = PetTaleSerializer(
            pettale, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pettale = self.get_object(pk)
        pettale.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )