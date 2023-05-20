from rest_framework import generics
from .models import Owner
from .serializers import OwnerSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class OwnerList(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Owner.objects.all()