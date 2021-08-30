from django.urls import reverse
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

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
        ordering = 'last_name'
        pref_related = 'books'
        if search_query:
            queryset = Author.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)).order_by(ordering).\
                prefetch_related(pref_related)
        else:
            queryset = Author.objects.all().order_by(ordering).prefetch_related(pref_related)
        return queryset

    def get_context_data(self, *args, **kwargs):
        """ Add search_query to context for using in template. """
        context = super().get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('authors-search')
        return context


class AuthorDetailView(DetailView):
    context_object_name = 'author'

    def get_object(self, queryset=None):
        try:
            author = Author.objects.select_related('user').get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise Http404('The Author does not exist or has been deleted.')
        return author


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.user = current_user
        try:
            current_user.groups.add(Group.objects.get(name='Authors'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Failed to create a new author.')
            return reverse('users:profile-user', kwargs={'pk': current_user.id})

        return super(AuthorCreateView, self).form_valid(form)


class AuthorUpdateView(PermissionRequiredMixin, IsOwnerOrStaff, UpdateView):
    permission_required = 'authors.change_author'
    model = Author
    form_class = AuthorForm

