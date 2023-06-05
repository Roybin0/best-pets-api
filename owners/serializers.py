from rest_framework import serializers
from .models import Owner
from followers.models import OwnerFollower


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    pets_count = serializers.SerializerMethodField()
    pettales_count = serializers.SerializerMethodField()
    petpics_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count_owners = serializers.SerializerMethodField()
    following_count_pets = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = OwnerFollower.objects.filter(
                owner=user, followed_owner=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_pets_count(self, obj):
        return obj.owner.pet_set.count()

    def get_pettales_count(self, obj):
        return obj.owner.pettale_set.count()

    def get_petpics_count(self, obj):
        return obj.owner.petpic_set.count()
    
    def get_followers_count(self, obj):
        return obj.owner.followed_owner.count()
    
    def get_following_count_owners(self, obj):
        return obj.owner.owner_following.count()
    
    def get_following_count_pets(self, obj):
        return obj.owner.pet_following.count()
    

    class Meta:
        model = Owner
        fields = [
            'id', 'owner', 'name', 'created_at', 'updated_at',
            'image', 'about', 'is_owner', 'following_id',
            'pets_count', 'pettales_count', 'petpics_count', 
            'followers_count', 'following_count_owners', 'following_count_pets',
        ]