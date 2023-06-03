from django.db.models import Count, OuterRef, Subquery
from rest_framework import generics, permissions, filters
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from .models import PetPic
from .serializers import PetPicSerializer
from bp_api.permissions import IsOwnerOrReadOnly
from likes.models import Like


class PetPicList(generics.ListCreateAPIView):
    serializer_class = PetPicSerializer
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
        'owner__followedOwner__owner',
        'likes__owner',
        'owner',
        'owner__pet',
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]

    def get_queryset(self):
        likes_subquery = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(PetPic),
            object_id=OuterRef('id')
        ).values('object_id').annotate(likes_count=Count('id')).values('likes_count')

        return PetPic.objects.annotate(
            comments_count=Count('comment', distinct=True),
            likes_count=Subquery(likes_subquery),
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetPicDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetPicSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        likes_subquery = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(PetPic),
            object_id=OuterRef('id')
        ).values('object_id').annotate(likes_count=Count('id')).values('likes_count')

        return PetPic.objects.annotate(
            comments_count=Count('comment', distinct=True),
            likes_count=Subquery(likes_subquery),
        ).order_by('-created_at')