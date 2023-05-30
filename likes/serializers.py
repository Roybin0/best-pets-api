from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from likes.models import Like 
from pets.models import Pet
# from pets.serializers import PetSerializer
from pettales.models import PetTale
# from pettales.serializers import PetTaleSerializer
from petpics.models import PetPic
# from petpics.serializers import PetPicSerializer

class ContentTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [
            ('pet', 'pet'),
            ('pettale', 'pettale'),
            ('petpic', 'petpic')
        ]
        super().__init__(choices, **kwargs)

    def to_representation(self, value):
        return value.model

    def to_internal_value(self, data):
        try:
            return ContentType.objects.get(model=data.lower()).model
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type.")

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    content_type = ContentTypeField()
    object_id = serializers.IntegerField(required=False, allow_null=True)
    like_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Like
        fields = ['owner', 'content_type', 'object_id', 'like_id', 'created_at']

    def validate_object_id(self, value):
        content_type = self.initial_data.get('content_type')

        if content_type == 'pet':
            if not Pet.objects.filter(pk=value).exists():
                raise serializers.ValidationError("Invalid pet object id.")
        elif content_type == 'pettale':
            if not PetTale.objects.filter(pk=value).exists():
                raise serializers.ValidationError("Invalid pet tale object id.")
        elif content_type == 'petpic':
            if not PetPic.objects.filter(pk=value).exists():
                raise serializers.ValidationError("Invalid pet pic object id.")
        else:
            raise serializers.ValidationError("Invalid content type.")

        return value

    def create(self, validated_data):
        owner = self.context['request'].user
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']

        # Convert the string content_type to the actual ContentType model
        content_type_model = ContentType.objects.get(model=content_type)

        try:
            # Check if the like already exists
            Like.objects.get(owner=owner, content_type=content_type_model, object_id=object_id)
            raise serializers.ValidationError("Like already exists for the provided object_id.")
        except Like.DoesNotExist:
            # Create a new like if it doesn't exist
            like = Like.objects.create(owner=owner, content_type=content_type_model, object_id=object_id)

        return like