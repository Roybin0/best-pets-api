from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Owner
from pets.models import Pet
from pettales.models import PetTale
from petpics.models import PetPic
from followers.models import Follower
from .serializers import OwnerSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class OwnerList(generics.ListAPIView):
    """
    List all owners.
    No create view as owner creation is handled by django signals.
    """
    # queryset = Owner.objects.annotate(
    #     pets_count=Count('owner__pet', distinct=True),
    #     pettales_count=Count('owner__pettale', distinct=True),
    #     petpics_count=Count('owner__petpic', distinct=True),
    #     followers_count=Count('owner__followed_owner', distinct=True),
    #     following_count_owners=Count('owner__following', distinct=True),
    #     following_count_pets=Count('owner__followed_pet', distinct=True),
    # )
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed_owner__owner',
        'owner__following__followed_pet__owner',
        # 'owner__followed__owner__owner',
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
        queryset = queryset.annotate(
            pets_count=Count('owner__pet', distinct=True),
            pettales_count=Count('owner__pettale', distinct=True),
            petpics_count=Count('owner__petpic', distinct=True),
            followers_count=Count('owner__followedOwner', distinct=True),
            following_count_owners=Count('owner__following', distinct=True),
            following_count_pets=Count('owner__pet__followedPet', distinct=True),
        )
        return queryset




class OwnerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Owner.objects.all()