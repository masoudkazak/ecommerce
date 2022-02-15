from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.models import User
from django.views.generic.edit import ModelFormMixin

from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect


class UserCreationView(CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        return reverse('account:login')


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
    

class ProfielCreateView(View):
    # model = User
    # context_object_name = 'user'
    template_name = 'profile-create.html'
    # form_class = ProfileCreateForm
    
    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user
    
    def get_context_data(self, **kwargs):
        kwargs['user'] = self.get_object()
        if "form" not in kwargs:
            kwargs['form'] = ProfileCreateForm
        return kwargs
    
    def get(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return redirect("item:list")
        try:
            CompanyProfile.objects.get(user=request.user)
        except CompanyProfile.DoesNotExist:
            return render(request, self.template_name, self.get_context_data())
        else:
            return redirect("item:list")
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            image = form.cleaned_data['image']
            phone_number = form.cleaned_data['phone_number']
            bio = form.cleaned_data['bio']
            gender = form.cleaned_data['gender']
            user = self.get_object()
            new_profile = Profile(
                image = image,
                phone_number = phone_number,
                bio = bio,
                gender = gender,
                user = user,
            )
            new_profile.save()
            return HttpResponseRedirect(reverse("item:list"))
        else:
            ctxt['form'] = CompanyProfileCreateForm
        return render(request, self.template_name, self.get_context_data(**ctxt))


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'Profile-update.html'
    form_class = ProfileCreateForm

    def get_success_url(self):
        return reverse('item:list')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    
    def get_success_url(self):
        return reverse('account:login')


class CompanyProfielCreateView(View):
    template_name = 'cprofile-create.html'

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user
    
    def get_context_data(self, **kwargs):
        kwargs['user'] = self.get_object()
        if "form" not in kwargs:
            kwargs['form'] = CompanyProfileCreateForm()
        return kwargs
    
    def get(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return redirect("item:list")
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        form = CompanyProfileCreateForm(request.POST)
        if form.is_valid():
            image = form.cleaned_data['image']
            phone_number = form.cleaned_data['phone_number']
            home_phone_number = form.cleaned_data['home_phone_number']
            bio = form.cleaned_data['bio']
            address_company = form.cleaned_data['address_company']
            user = self.get_object()
            new_profile = CompanyProfile(user=user,
                                image=image,
                                phone_number=phone_number,
                                bio=bio,
                                address_company=address_company,
                                home_phone_number=home_phone_number)
            new_profile.save()
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                return HttpResponseRedirect(reverse("item:list"))
            profile.delete()
            return HttpResponseRedirect(reverse("item:list"))
        else:
            ctxt['form'] = CompanyProfileCreateForm

        return render(request, self.template_name, self.get_context_data(**ctxt))


class CompanyProfileUpdateView(UpdateView):
    model = CompanyProfile
    template_name  = "cprofile-update.html"
    form_class = CompanyProfileCreateForm

    def get_success_url(self):
        return reverse('item:list')