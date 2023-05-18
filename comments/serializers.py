from rest_framework import serializers
from .models import Comment
from pets.models import Pet
from pettales.models import PetTale
from petpics.models import PetPic
from pets.serializers import PetSerializer
from pettales.serializers import PetTaleSerializer
from petpics.serializers import PetPicSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')
    pet_id = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(), write_only=True, required=False)
    pet_tale_id = serializers.PrimaryKeyRelatedField(queryset=PetTale.objects.all(), write_only=True, required=False)
    pet_pic_id = serializers.PrimaryKeyRelatedField(queryset=PetPic.objects.all(), write_only=True, required=False)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    class Meta:
        model = Pet
        fields = [
            'id', 'owner', 'pet_id', 'pet_tale_id', 'pet_pic_id',
            'created_at', 'updated_at', 'comment', 'is_owner', 'owner_id',
            'owner_profile_image',
        ]


class CommentDetailSerializer(CommentSerializer):
    pet = PetSerializer(read_only=True)
    pet_tale = PetTaleSerializer(read_only=True)
    pet_pic = PetPicSerializer(read_only=True)