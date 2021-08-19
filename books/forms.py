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


# class BookReviewCreateForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['text']
