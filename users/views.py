from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.http import Http404
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from books.utils import IsOwnerOrStaff
from users.models import User
from authors.models import Author


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'


class UserEditView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_message = 'Profile was changed successfully.'

    def get_object(self, queryset=None):
        try:
            obj = super(UserEditView, self).get_object(queryset)
        except ObjectDoesNotExist:
            raise Http404('User does not exist or has been deleted.')
        if self.request.user == obj or self.request.user.is_staff:
            return obj
        raise PermissionDenied('You don\'t have permission to edit this profile')

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs.get('pk')
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        try:
            author = Author.objects.get(user=self.kwargs['pk'])
        except Author.DoesNotExist:
            author = None
        context['author'] = author

        return context


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/change-password.html'
    success_message = 'Your Password was changed successfully.'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:profile-user', kwargs={'pk': pk})


