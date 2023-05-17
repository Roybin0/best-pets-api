from django.urls import path
from petpics import views

urlpatterns = [
    path('petpics/', views.PetPicList.as_view()),
    path('petpics/<int:pk>/', views.PetPicDetail.as_view()),
]