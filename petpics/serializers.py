from rest_framework import serializers
from .models import PetPic


class PetPicSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')
    pet_id = serializers.ReadOnlyField(source='owner.pet.id')
    pet_name = serializers.ReadOnlyField(source='owner.pet.name')
    pet_type = serializers.ReadOnlyField(source='owner.pet.type')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    class Meta:
        model = PetPic
        fields = [
            'id', 'owner', 'pet_id', 'pet_name', 'pet_type', 'created_at', 
            'updated_at', 'image', 'description', 'is_owner', 'owner_id',
            'owner_profile_image',
        ]