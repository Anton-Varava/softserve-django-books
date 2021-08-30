from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from books.models import Book
from books.models import Author
from .serializers import BookSerializer


# Create your views here.
class APIBooksList(generics.ListAPIView):
    queryset = Book.objects.prefetch_related('authors').all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer


