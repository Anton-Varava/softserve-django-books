from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group

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
    context_object_name = 'author'

    def get_object(self, queryset=None):
        author = Author.objects.filter(id=self.kwargs['pk']).select_related('user').first()
        return author


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.user = current_user
        form.save()
        try:
            current_user.groups.add(Group.objects.get(name='Authors'))
        except ObjectDoesNotExist:
            pass
        return super(AuthorCreateView, self).form_valid(form)

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

