from rest_framework import serializers

from books.models import Book
from authors.models import Author


class BooksListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'isbn13', 'title', 'authors']


class BookSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(allow_blank=True)

    class Meta:
        model = Book
        fields = ['id', 'isbn13', 'title', 'authors', 'description']
        # fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']
