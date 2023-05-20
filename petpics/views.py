from rest_framework import generics, permissions
from .models import PetPic
from .serializers import PetPicSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetPicList(generics.ListCreateAPIView):
    serializer_class = PetPicSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = PetPic.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetPicDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetPicSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = PetPic.objects.all()