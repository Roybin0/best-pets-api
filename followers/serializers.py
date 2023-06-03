from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_owner_name = serializers.ReadOnlyField(source='followed_owner.username')
    followed_pet_name = serializers.ReadOnlyField(source='followed_pet.name')

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'created_at', 'followed_owner',
            'followed_owner_name', 'followed_pet', 'followed_pet_name',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Possible duplicate'
            })