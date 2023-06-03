from rest_framework import serializers
from .models import Owner
from followers.models import Follower


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    pets_count = serializers.SerializerMethodField()
    pettales_count = serializers.SerializerMethodField()
    petpics_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count_owners = serializers.SerializerMethodField()
    following_count_pets = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                following_owner = Follower.objects.get(owner=user, followed_owner=obj.owner)
                if following_owner:
                    return following_owner.id
                following_pet = Follower.objects.get(owner=user, followed_pet=obj)
                if following_pet:
                    return following_pet.id
            except Follower.DoesNotExist:
                pass
        return None

    def get_pets_count(self, obj):
        return obj.owner.pet_set.count()

    def get_pettales_count(self, obj):
        return obj.owner.pettale_set.count()

    def get_petpics_count(self, obj):
        return obj.owner.petpic_set.count()

    def get_followers_count(self, obj):
        return obj.owner.followedOwner.count()

    def get_following_count_owners(self, obj):
        return obj.owner.following.filter(followed_owner__isnull=False).values('followed_owner').distinct().count()

    def get_following_count_pets(self, obj):
        return obj.owner.following.filter(followed_pet__isnull=False).count()

    class Meta:
        model = Owner
        fields = [
            'id', 'owner', 'name', 'created_at', 'updated_at',
            'image', 'about', 'is_owner', 'following_id',
            'pets_count', 'pettales_count', 'petpics_count',
            'followers_count', 'following_count_owners', 
            'following_count_pets',
        ]