from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Owner
from .serializers import OwnerSerializer
from bp_api.permissions import IsOwnerOrReadOnly


class OwnerList(APIView):
    def get (self, request):
        owners = Owner.objects.all()
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data)


class OwnerDetail(APIView):
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