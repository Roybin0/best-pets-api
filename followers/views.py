from rest_framework import generics, permissions
from bp_api.permissions import IsOwnerOrReadOnly
from .models import OwnerFollower, PetFollower
from .serializers import OwnerFollowerSerializer, PetFollowerSerializer


class OwnerFollowerList(generics.ListCreateAPIView):
    serializer_class = OwnerFollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return OwnerFollower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OwnerFollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = OwnerFollowerSerializer

    def get_queryset(self):
        user = self.request.user
        return OwnerFollower.objects.filter(owner=user)


class PetFollowerList(generics.ListCreateAPIView):
    serializer_class = PetFollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PetFollower.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetFollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PetFollowerSerializer

    def get_queryset(self):
        user = self.request.user
        return PetFollower.objects.filter(owner=user)