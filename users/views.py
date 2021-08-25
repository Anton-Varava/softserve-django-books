from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy, reverse
from .forms import UserRegistrationForm, UserUpdateForm
# from django.contrib.auth.models import Group, User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied

from users.models import User
from authors.models import Author


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse('users:profile-user', args=(self.object.id, ))


class UserEditView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_message = 'Profile was changed successfully...'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:profile-user', kwargs={'pk': pk})

    def get_object(self, queryset=None):
        obj = super(UserEditView, self).get_object(queryset)
        if self.request.user == obj or self.request.user.is_staff:
            return obj
        raise PermissionDenied


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
    success_message = 'Your Password was changed successfully...'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:profile-user', kwargs={'pk': pk})


