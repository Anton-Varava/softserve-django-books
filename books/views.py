from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.db.models import Q

from .models import Book, BookReview, ReviewComment
from .forms import BookUpdateForm, BookCreateForm


# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('book-search')
        ordering = '-popularity_rank'
        if query:
            queryset = Book.objects.filter(
                Q(title__icontains=query) | Q(isbn13=query)).prefetch_related('authors').order_by(ordering)
        else:
            queryset = Book.objects.prefetch_related('authors').order_by(ordering)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_search'] = self.request.GET.get('book-search')
        return context


class BookDetailView(DetailView):
    model = Book
    prefetch_related = ['authors']
    context_object_name = 'book'


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookUpdateForm
    success_message = 'Book updated successfully.'
    template_name = 'books/book_form.html'
    context_object_name = 'book'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('books:detail-book', kwargs={'pk': pk})


class BookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm

    def get_success_url(self):
        return reverse('books:detail-book', args=(self.object.id, ))







