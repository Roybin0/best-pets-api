from django.urls import path
from petstories import views

urlpatterns = [
    path('petstories/', views.PetStoryList.as_view()),
]