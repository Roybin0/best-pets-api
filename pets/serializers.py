from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    class Meta:
        model = Pet
        fields = [
            'id', 'owner', 'name', 'type', 'created_at',
            'updated_at', 'image', 'about', 'is_owner', 'owner_id',
            'owner_profile_image',
        ]