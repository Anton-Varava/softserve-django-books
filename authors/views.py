from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from books.utils import IsOwnerOrStaff
from authors.models import Author
from .forms import AuthorForm


class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        """ Return Author list with searching parameters or all objects. """
        search_query = self.request.GET.get('authors-search')
        if search_query:
            queryset = Author.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)).order_by('last_name').prefetch_related('books')
        else:
            queryset = Author.objects.all().order_by('last_name').prefetch_related('books')
        return queryset

    def get_context_data(self, *args, **kwargs):
        """ Add search_query to context for using in template. """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('authors-search')
        return context


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'authors.change_author'
    form_class = AuthorForm

    def post(self, request, *args, **kwargs):
        """ Add current user to form data before saving. """
        form = AuthorForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        """ Return to the created book details. """
        return reverse('authors:detail-author', args=(self.object.id,))


class AuthorUpdateView(PermissionRequiredMixin, IsOwnerOrStaff, UpdateView):
    permission_required = 'authors.change_author'
    model = Author
    form_class = AuthorForm

    def get_success_url(self):
        """ Return to the updated book details. """
        pk = self.kwargs['pk']
        return reverse('authors:detail-author', kwargs={'pk': pk})

