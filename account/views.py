from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.models import User
from django.views.generic.edit import ModelFormMixin

from .models import Profile
from .forms import UserCreateForm, UserUpdateForm, ProfileCreateForm
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class UserCreationView(CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        return reverse('item:list')


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('item:list')
    

class UserUpdateView(UpdateView):
    model = User
    template_name = 'update.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('item:list')
    

class ProfielCreateView(ModelFormMixin ,DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'profile-create.html'
    form_class = ProfileCreateForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            image = form.cleaned_data['image']
            phone_number = form.cleaned_data['phone_number']
            bio = form.cleaned_data['bio']
            gender = form.cleaned_data['gender']
            user = self.get_object()
            new_profile = Profile(user=user,
                                image=image,
                                phone_number=phone_number,
                                bio=bio,
                                gender=gender)
            new_profile.save()
            return redirect('account:update', pk=user.pk)


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'Profile-update.html'
    form_class = ProfileCreateForm

    def get_success_url(self):
        return reverse('item:list')