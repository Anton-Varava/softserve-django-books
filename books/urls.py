from django.urls import path

from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='list-book'),
    path('<int:pk>', views.BookDetailView.as_view(), name='detail-book'),
    path('<int:pk>/edit', views.BookUpdateView.as_view(), name='edit-book'),
    path('create', views.BookCreateView.as_view(), name='create-book'),
    path('search', views.BookListView.as_view(), name='search-books')
]