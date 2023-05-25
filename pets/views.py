from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pet
from .serializers import PetSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetList(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Pet.objects.all()

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        'name',
        'pet_type',
        'owner__username',
    ]

    filterset_fields = [
        'owner',
        'name',
        'pet_type',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Pet.objects.all()
