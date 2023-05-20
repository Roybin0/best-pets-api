from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Owner
from .serializers import OwnerSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class OwnerList(generics.ListAPIView):
    queryset = Owner.objects.annotate(
        pets_count = Count('owner__pet', distinct=True),
        pettales_count = Count('owner__pettale', distinct=True),
        petpics_count = Count('owner__petpic', distinct=True),
        followers_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = OwnerSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__owner',
        'owner__followed__owner__owner',
    ]
    ordering_fields = [
        'pets_count',
        'pettales_count',
        'petpics_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at', 
    ]


class OwnerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Owner.objects.all()