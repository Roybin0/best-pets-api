from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import PetPic
from pets.models import Pet
from likes.models import Like


class PetPicSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())
    pet_name = serializers.ReadOnlyField(source='pet.name')
    pet_type = serializers.ReadOnlyField(source='pet.pet_type')
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.SerializerMethodField()

    # Set owner automatically based on current logged in user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request'):
            user = self.context['request'].user
            if user.is_authenticated:
                self.fields['pet_id'].queryset = Pet.objects.filter(owner=user)
            else:
                self.fields['pet_id'].queryset = Pet.objects.none()

    # Extract id from Pet object and add as pet_id to PetPic
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['pet_id'] = validated_data['pet'].id
        return super().create(validated_data)

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
    
    class Meta:
        model = PetPic
        fields = [
            'id', 'owner', 'pet', 'pet_id', 'pet_name', 'pet_type', 'created_at', 
            'updated_at', 'image', 'description', 'is_owner', 'owner_id',
            'owner_profile_image', 'comments_count', 'likes_count',
        ]