from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Like
from pettales.models import PetTale
from petpics.models import PetPic

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pet_tale_id = serializers.PrimaryKeyRelatedField(
        queryset=PetTale.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    pet_pic_id = serializers.PrimaryKeyRelatedField(
        queryset=PetPic.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'pet_tale_id', 'pet_pic_id', 'created_at'
        ]

    def validate(self, attrs):
        pet_tale_id = attrs.get('pet_tale_id')
        pet_pic_id = attrs.get('pet_pic_id')

        if pet_tale_id and pet_pic_id:
            raise serializers.ValidationError("Cannot like both Pet Tale and Pet Pic. Choose one.")

        return attrs

    def create(self, validated_data):
        pet_tale_id = validated_data.pop('pet_tale_id', None)
        pet_pic_id = validated_data.pop('pet_pic_id', None)

        like = Like(**validated_data)

        # Check if object is tale or pic 
        if pet_tale_id:
            like.content_type = ContentType.objects.get_for_model(PetTale)
            like.object_id = pet_tale_id.pk
        elif pet_pic_id:
            like.content_type = ContentType.objects.get_for_model(PetPic)
            like.object_id = pet_pic_id.pk

        try:
            like.save()
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Possible duplicate'
            })
        return like