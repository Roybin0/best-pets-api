from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pet
from .serializers import PetSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class PetList(generics.ListCreateAPIView):
    """
    List all pets or add a new pet if logged in. 
    """

    serializer_class = PetSerializer
    permission_classes = [permissions.]

    def get (self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)


class PetDetail(APIView):
    serializer_class = OwnerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            owner = Owner.objects.get(pk=pk)
            self.check_object_permissions(self.request, owner)
            return owner
        except Owner.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        owner = self.get_object(pk)
        serializer = OwnerSerializer(
            owner, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        owner = self.get_object(pk)
        serializer = OwnerSerializer(
            owner, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)