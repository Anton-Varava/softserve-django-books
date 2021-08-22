from django import forms

from books.models import Book, BookReview, ReviewComment


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn13', 'description', 'authors']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn13', 'description', 'authors']


class BookReviewCreateForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['body']


class BookReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['body']


class ReviewCommentCreateForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['body']


class ReviewCommentUpdateForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['body']



