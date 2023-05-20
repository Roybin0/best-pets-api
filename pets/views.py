from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetList(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Pet.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Pet.objects.all()