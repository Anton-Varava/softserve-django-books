from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView

from authors.models import Author


# Create your views here.
class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('authors-search')
        if search_query:
            queryset = Author.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)).order_by('last_name')
        else:
            queryset = Author.objects.all().order_by('last_name').prefetch_related('books')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('authors-search')
        return context


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'

