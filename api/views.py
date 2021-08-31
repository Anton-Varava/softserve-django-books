from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned

from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from books.models import Book
from books.models import Author
from .serializers import BooksListSerializer, AuthorSerializer, BookSerializer
from .renderers import BooksJSONRenderer, AuthorsJSONRenderer


# Create your views here.
class BooksListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BooksListSerializer
    renderer_classes = [BooksJSONRenderer]


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    renderer_classes = [BooksJSONRenderer]


class AuthorsListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    renderer_classes = [AuthorsJSONRenderer]


class AuthorDetailAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer
    renderer_classes = [AuthorsJSONRenderer]




