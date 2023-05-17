from django.urls import path
from pettales import views

urlpatterns = [
    path('pettales/', views.PetTaleList.as_view()),
]