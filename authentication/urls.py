from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserRetrieveUpdateAPIView.as_view(), name='edit-user'),
    path('users/signup', views.UserRegistrationAPIView.as_view(), name='create-user'),
    path('users/login', views.UserLoginAPIView.as_view(), name='login')
]
