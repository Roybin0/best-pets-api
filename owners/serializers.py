from rest_framework import serializers
from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Owner
        fields = [
            'id', 'owner', 'name', 'created_at', 'updated_at',
            'image', 'about',
        ]