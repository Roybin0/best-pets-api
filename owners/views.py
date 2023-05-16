from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Owner


class OwnerList(APIView):
    def get (self, request):
        owners = Owner.objects.all()
        return Response(owners)