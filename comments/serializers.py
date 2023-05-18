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
    pet = serializers.PrimaryKeyRelatedField(read_only=True)
    pet_id = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(), write_only=True, required=False)
    pet_tale_id = serializers.PrimaryKeyRelatedField(queryset=PetTale.objects.all(), write_only=True, required=False)
    pet_pic_id = serializers.PrimaryKeyRelatedField(queryset=PetPic.objects.all(), write_only=True, required=False)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def  validate(self, attrs):
        pet_id = attrs.get('pet_id')
        pet_tale_id = attrs.get('pet_tale')
        pet_pic_id = attrs.get('pet_pic')
        
        if pet_id:
            if pet_tale_id and pet_tale_id.pet != pet_id:
                raise serializers.ValidationError("The selected pet tale does not belong to the chosen pet.")
            if pet_pic_id and pet_pic_id.pet != pet_id:
                raise serializers.ValidationError("The selected pet pic does not belong to the chosen pet.")

        return attrs
    
    def create(self, validated_data):
        pet_id = validated_data.pop('pet_id', None)
        
        comment = Comment.objects.create(**validated_data)

        if pet_id:
            try:
                pet = Pet.objects.get(pk=pet_id)
                comment.pet = pet
            except Pet.DoesNotExist:
                raise serializers.ValidationError("Invalid Pet ID")

        comment.save()

        return comment
    
    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'pet', 'pet_id', 'pet_tale_id', 'pet_pic_id',
            'created_at', 'updated_at', 'comment', 'is_owner', 'owner_id',
            'owner_profile_image',
        ]


class CommentDetailSerializer(CommentSerializer):
    pet = PetSerializer(read_only=True)
    pet_tale = PetTaleSerializer(read_only=True)
    pet_pic = PetPicSerializer(read_only=True)