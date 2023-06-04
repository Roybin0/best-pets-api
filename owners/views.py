from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Owner
from .serializers import OwnerSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class OwnerList(generics.ListAPIView):
    """
    List all owners.
    No create view as owner creation is handled by django signals.
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__owner_following__owner',
        'owner__pet__followed_pet',
        'owner__followed_owner__owner',
    ]
    ordering_fields = [
        'pets_count',
        'pettales_count',
        'petpics_count',
        'followers_count',
        'following_count_owners',
        'following_count_pets',
        'owner__following_count_owners__created_at',
        'owner__following_count_pets__created_at',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('id')
        queryset = queryset.annotate(
            pets_count=Count('owner__pet', distinct=True),
            pettales_count=Count('owner__pettale', distinct=True),
            petpics_count=Count('owner__petpic', distinct=True),
            followers_count=Count('owner__followed_owner', distinct=True),
            following_count_owners=Count('owner__owner_following__followed_owner', distinct=True),
            following_count_pets=Count('owner__pet_following__followed_pet', distinct=True),
        )
        return queryset




class OwnerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Owner.objects.all()