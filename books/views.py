from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from .models import Book, BookReview, ReviewComment


# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['popularity_rank']


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'