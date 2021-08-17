from django.shortcuts import render
from django.views.generic import ListView, DetailView

from authors.models import Author


# Create your views here.
class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'
