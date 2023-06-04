from django.urls import path
from followers import views


urlpatterns = [
    path('followers-owners/', views.OwnerFollowerList.as_view()),
    path('followers-owners/<int:pk>', views.OwnerFollowerDetail.as_view()),
    path('followers-pets/', views.PetFollowerList.as_view()),
    path('followers-pets/<int:pk>', views.PetFollowerDetail.as_view()),
]