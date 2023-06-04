from django.db import IntegrityError
from rest_framework import serializers
from .models import OwnerFollower, PetFollower


class OwnerFollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the OwnerFollower model
    Create method handles the unique constraint on 'owner' and 'followed_owner'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed_owner.username')

    class Meta:
        model = OwnerFollower
        fields = [
            'id', 'owner', 'created_at', 'followed_owner', 'followed_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Already following this owner!'})


class PetFollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the PetFollower model
    Create method handles the unique constraint on 'owner' and 'followed_pet'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_pet_name = serializers.ReadOnlyField(source='followed_pet.name')

    class Meta:
        model = PetFollower
        fields = [
            'id', 'owner', 'created_at', 'followed_pet', 'followed_pet_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Already following this pet!'})