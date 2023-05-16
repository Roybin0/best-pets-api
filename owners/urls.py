from django.urls import path
from owners import views


urlpatterns = [
    path('owners/', views.OwnerList.as_view()),
]