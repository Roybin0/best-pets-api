from rest_framework import serializers
from .models import Pet
from likes.models import Like
from django.contrib.contenttypes.models import ContentType


class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()

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
    
    def get_like_id(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        if user:
            like = Like.objects.filter(
                owner=user, content_type=ContentType.objects.get_for_model(Pet), object_id=obj.id
            ).first()
            return like.id if like else None
        return None
    
    class Meta:
        model = Pet
        fields = [
            'id', 'owner', 'name', 'pet_type', 'created_at',
            'updated_at', 'image', 'about', 'is_owner', 'owner_id',
            'owner_profile_image', 'like_id', 'likes_count',
        ] 