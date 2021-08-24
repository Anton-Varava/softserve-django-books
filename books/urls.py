from django.urls import path

from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='list-book'),
    path('<int:pk>', views.BookDetailView.as_view(), name='detail-book'),
    path('<int:pk>/edit', views.BookUpdateView.as_view(), name='edit-book'),
    path('create', views.BookCreateView.as_view(), name='create-book'),
    path('<int:pk>/delete', views.BookDeleteView.as_view(), name='delete-book'),
    path('search', views.BookListView.as_view(), name='search-books'),
    path('<int:book_id>/review', views.BookReviewCreateView.as_view(), name='add-review'),
    path('<int:book_id>/review-edit/<int:pk>', views.BookReviewUpdateView.as_view(), name='edit-review'),
    path('<int:book_id>/review-delete/<int:pk>', views.BookReviewDeleteView.as_view(), name='delete-review'),
    path('<int:book_id>/<int:review_id>/comment_add', views.CommentReviewCreateView.as_view(), name='add-comment'),
    path('<int:book_id>/<int:review_id>/reply_comment_add/<int:reply_id>', views.CommentReviewCreateView.as_view(),
         name='add-reply-comment'),
    path('<int:book_id>/comment_edit/<int:pk>', views.CommentUpdateView.as_view(), name='edit-comment'),
    path('<int:book_id>/comment_delete/<int:pk>', views.CommentDeleteView.as_view(), name='delete-comment'),

]