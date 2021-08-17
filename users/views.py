from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth.models import User


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_message = 'User created successfully.'
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse('users:profile-user', args=(self.object.id, ))


class UserEditView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_message = 'User updated successfully.'
    template_name = 'users/user_form.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:profile-user', kwargs={'pk': pk})


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'


