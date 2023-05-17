from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetPic
from .serializers import PetPicSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetPicList(APIView):
    serializer_class = PetPicSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        petpics = PetPic.objects.all()
        serializer = PetPicSerializer(
            petpics, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PetPicSerializer(
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


class PetPicDetail(APIView):
    serializer_class = PetPicSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            petpic = PetPic.objects.get(pk=pk)
            self.check_object_permissions(self.request, petpic)
            return petpic
        except PetPic.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        petpic = self.get_object(pk)
        serializer = PetPicSerializer(
            petpic, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        petpic = self.get_object(pk)
        serializer = PetPicSerializer(
            petpic, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        petpic = self.get_object(pk)
        petpic.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )