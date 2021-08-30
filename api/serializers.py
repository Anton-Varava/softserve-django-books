from rest_framework import serializers

from books.models import Book
from authors.models import Author


class BookSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'isbn13', 'title', 'authors', 'url']
