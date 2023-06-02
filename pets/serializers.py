from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Pet
from likes.models import Like
from comments.models import Comment


class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2mb! Too big, try a different image.'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px. Too wide, try a different \
                     image.'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px. Too tall, try a different \
                     image.'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return Comment.objects.filter(pet=obj).count()
    
    class Meta:
        model = Pet
        fields = [
            'id', 'owner', 'name', 'pet_type', 'created_at',
            'updated_at', 'image', 'about', 'is_owner', 'owner_id',
            'owner_profile_image', 'likes_count', 'comments_count',
        ] 