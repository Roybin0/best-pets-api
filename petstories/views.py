from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PetStory
from .serializers import PetStorySerializer


class PetStoryList(APIView):
    def get(self, request):
        petstories = PetStory.objects.all()
        serializer = PetStorySerializer(
            petstories, many=True, context={'request': request}
        )
        return Response(serializer.data)
