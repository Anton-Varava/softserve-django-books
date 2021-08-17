from django.urls import path

from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='list-book'),
    path('<int:pk>', views.BookDetailView.as_view(), name='detail-book')
]