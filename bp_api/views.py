from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def root_route(request):
    return Response({
        "message": "Best Pets API - To view the user interface, visit https://bestpets.herokuapp.com"
    })