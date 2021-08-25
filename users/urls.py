from django.urls import path
from django.shortcuts import render

from . import views


urlpatterns = [
    path('<int:pk>/edit', views.UserEditView.as_view(), name='edit-user'),
    path('<int:pk>', views.UserDetailView.as_view(), name='profile-user'),
    path('<int:pk>/password', views.UserPasswordChangeView.as_view(), name='change-password'),
]
