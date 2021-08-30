from django.urls import path
from . import views


urlpatterns = [
    # path('book', ),
    path('books/', views.APIBooksList.as_view(), name='list-books'),
    # path('author'),
    # path('authors')
]
