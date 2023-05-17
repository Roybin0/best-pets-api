from rest_framework import serializers
from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    class Meta:
        model = Owner
        fields = [
            'id', 'owner', 'name', 'created_at', 'updated_at',
            'image', 'about', 'is_owner',
        ]