from rest_framework import serializers
from .models import Owner
from followers.models import Follower


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    pets_count = serializers.ReadOnlyField()
    pettales_count = serializers.ReadOnlyField()
    petpics_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()


    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Owner
        fields = [
            'id', 'owner', 'name', 'created_at', 'updated_at',
            'image', 'about', 'is_owner', 'following_id',
            'pets_count', 'pettales_count', 'petpics_count',
            'followers_count', 'following_count',
        ]