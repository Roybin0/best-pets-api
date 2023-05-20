from rest_framework import generics, permissions
from .models import PetTale
from .serializers import PetTaleSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetTaleList(generics.ListCreateAPIView):
    serializer_class = PetTaleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = PetTale.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetTaleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetTaleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = PetTale.objects.all()