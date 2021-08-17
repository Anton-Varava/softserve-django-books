from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='list-authors'),
    path('<int:pk>', views.AuthorDetailView.as_view(), name='detail-authors')
]
