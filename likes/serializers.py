from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Like
from pettales.models import PetTale
from petpics.models import PetPic
from pets.models import Pet
from pettales.serializers import PetTaleSerializer
from petpics.serializers import PetPicSerializer
from pets.serializers import PetSerializer

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pet = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    pet_tale = serializers.PrimaryKeyRelatedField(
        queryset=PetTale.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    pet_pic = serializers.PrimaryKeyRelatedField(
        queryset=PetPic.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    pet_id = serializers.SerializerMethodField(read_only=True)
    pet_tale_id = serializers.SerializerMethodField(read_only=True)
    pet_pic_id = serializers.SerializerMethodField(read_only=True)

    def get_pet_id(self, obj):
        if obj.content_type.model_class() == Pet:
            return obj.object_id
        return None

    def get_pet_tale_id(self, obj):
        if obj.content_type.model_class() == PetTale:
            return obj.object_id
        return None

    def get_pet_pic_id(self, obj):
        if obj.content_type.model_class() == PetPic:
            return obj.object_id
        return None

    def validate(self, attrs):
        pet = attrs.get('pet')
        pet_tale = attrs.get('pet_tale')
        pet_pic = attrs.get('pet_pic')
        

        if pet and pet_pic:
            raise serializers.ValidationError("Cannot like both Pet and Pet Pic. Choose one.")
        
        if pet and pet_tale:
            raise serializers.ValidationError("Cannot like both Pet and Pet Tale. Choose one.")
        
        if pet_tale and pet_pic:
            raise serializers.ValidationError("Cannot like both Pet Tale and Pet Pic. Choose one.")
        
        if pet and pet_tale and pet_pic:
            raise serializers.ValidationError("Cannot like all three at once! Choose one.")

        return attrs

    def create(self, validated_data):
        pet = validated_data.pop('pet', None)
        pet_tale = validated_data.pop('pet_tale', None)
        pet_pic = validated_data.pop('pet_pic', None)

        like = Like(**validated_data)

        # Check if object is pet, tale or pic 
        if pet:
            like.content_type = ContentType.objects.get_for_model(Pet)
            like.object_id = pet.id
        elif pet_tale:
            like.content_type = ContentType.objects.get_for_model(PetTale)
            like.object_id = pet_tale.id
        elif pet_pic:
            like.content_type = ContentType.objects.get_for_model(PetPic)
            like.object_id = pet_pic.id

        try:
            like.save()
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Possible duplicate'
            })
        return like
    
    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'pet', 'pet_tale', 'pet_pic', 'created_at',
            'pet_id', 'pet_tale_id', 'pet_pic_id',
        ]