from django import forms

from books.models import Book, BookReview, ReviewComment
from authors.models import Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn13', 'description', 'authors']


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['body']


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['body']



