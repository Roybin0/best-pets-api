from django.urls import path
from owners import views


urlpatterns = [
    path('owners/', views.OwnerList.as_view()),
    path('owners/<int:pk>', views.OwnerDetail.as_view()),
]