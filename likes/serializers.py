from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    content_type = serializers.CharField(source='content_type.model', read_only=True)
    object_id = serializers.IntegerField(read_only=True)
    like_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Like
        fields = ['owner', 'content_type', 'object_id', 'like_id', 'created_at']

    def create(self, validated_data):
        owner = self.context['request'].user
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']
        try:
            # Check if the like already exists
            like = Like.objects.get(owner=owner, content_type=content_type, object_id=object_id)
            return like
        except Like.DoesNotExist:
            # Create a new like if it doesn't exist
            like = Like.objects.create(owner=owner, content_type=content_type, object_id=object_id)
            return like

    def destroy(self, instance):
        instance.delete()