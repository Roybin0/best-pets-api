from django.db.models import Count, OuterRef, Subquery
from rest_framework import generics, permissions, filters
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from .models import PetTale
from .serializers import PetTaleSerializer
from bp_api.permissions import IsOwnerOrReadOnly
from likes.models import Like


class PetTaleList(generics.ListCreateAPIView):
    serializer_class = PetTaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        'owner__username',
        'pet__name',
        'pet__pet_type'
    ]

    filterset_fields = [
        'owner__followed_owner',
        'likes__owner',
        'owner',
        'pet',
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]

    def get_queryset(self):
        likes_subquery = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(PetTale),
            object_id=OuterRef('id')
        ).values('object_id').annotate(likes_count=Count('id')).values('likes_count')

        return PetTale.objects.annotate(
            comments_count=Count('comment', distinct=True),
            likes_count=Subquery(likes_subquery),
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetTaleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetTaleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        likes_subquery = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(PetTale),
            object_id=OuterRef('id')
        ).values('object_id').annotate(likes_count=Count('id')).values('likes_count')

        return PetTale.objects.annotate(
            comments_count=Count('comment', distinct=True),
            likes_count=Subquery(likes_subquery),
        ).order_by('-created_at')