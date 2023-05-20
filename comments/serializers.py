from rest_framework import serializers
from .models import Comment
from pettales.models import PetTale
from petpics.models import PetPic
from pettales.serializers import PetTaleSerializer
from petpics.serializers import PetPicSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.owner.id')
    owner_profile_image = serializers.ReadOnlyField(source='owner.owner.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user

        # Check if comment is for a PetTale or PetPic
        if 'pet_tale' in validated_data:
            pet_tale = validated_data.pop('pet_tale')
            if pet_tale:
                validated_data['pet_tale_id'] = pet_tale.id
        elif 'pet_pic' in validated_data:
            pet_pic = validated_data.pop('pet_pic')
            if pet_pic:
                validated_data['pet_pic_id'] = pet_pic.id

        return Comment.objects.create(**validated_data)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'pet_tale', 'pet_pic',
            'created_at', 'updated_at', 'comment', 'is_owner', 'owner_id',
            'owner_profile_image',
        ]


class CommentDetailSerializer(CommentSerializer):
    pet_tale = PetTaleSerializer(read_only=True)
    pet_pic = PetPicSerializer(read_only=True)