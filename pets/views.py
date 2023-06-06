from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Pet
from .serializers import PetSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class FollowersCountOrderingFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)

        if ordering:
            modified_ordering = []
            for field in ordering:
                if field == 'followers_count':
                    modified_ordering.append('followed_pet__count')
                elif field == '-followers_count':
                    modified_ordering.append('-followed_pet__count')
                else:
                    modified_ordering.append(field)
            return modified_ordering

        return ordering


class PetList(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Pet.objects.all()

    filter_backends = [
        FollowersCountOrderingFilter,
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
        'followed_pet__owner'
    ]

    ordering_fields = [
        'likes_count',
        'likes__created_at',
        'comments_count',
        'followers_count',
    ]
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # Retrieve the value of the 'owner__username' query parameter
        owner_username = self.request.query_params.get('owner__username')

        if owner_username:
            # Filter the queryset by owner username using case-insensitive matching
            queryset = queryset.filter(owner__username__iexact=owner_username)
        
        queryset = queryset.annotate(followers_count=Count('followed_pet', distinct=True))

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Pet.objects.all()