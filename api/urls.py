from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.BooksListAPIView.as_view(), name='list-books'),
    path('books/<int:pk>', views.BookDetailAPIView.as_view(), name='detail-book'),
    path('authors/', views.AuthorsListAPIView.as_view()),
    path('authors/<int:pk>', views.AuthorDetailAPIView.as_view())
]
