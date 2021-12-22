from django.views.generic import (
    CreateView,
)
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.urls import reverse
from django.contrib.auth.views import LoginView


class UserCreateView(CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        return reverse('item:list')


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('item:list')
