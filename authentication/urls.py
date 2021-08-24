from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserRetrieveUpdateAPIView.as_view()),
    path('users/', views.UserRegistrationAPIView.as_view()),
    path('users/login', views.UserLoginAPIView.as_view())
]
