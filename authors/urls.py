from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='list-authors'),
    path('<int:pk>', views.AuthorDetailView.as_view(), name='detail-author'),
    path('search', views.AuthorListView.as_view(), name='search-authors'),
    path('create', views.AuthorCreateView.as_view(), name='create-author'),
    path('<int:pk>/edit', views.AuthorUpdateView.as_view(), name='update-author')
]
