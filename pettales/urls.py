from django.urls import path
from pettales import views

urlpatterns = [
    path('pettales/', views.PetTaleList.as_view()),
    path('pettales/<int:pk>/', views.PetTaleDetail.as_view()),
]