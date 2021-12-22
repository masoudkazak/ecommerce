from django.db.models.base import Model
from django.shortcuts import render
from django.views import generic
from django.views.generic import (
    CreateView,
)
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.urls import reverse


class UserCreateView(CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        return reverse('item:list')


