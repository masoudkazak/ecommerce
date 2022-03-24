from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.contrib.auth.models import User

from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout


class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        return redirect('account:update', username=request.user.username, )


class UserCreationView(CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "ثبت نام شما با موفقیت انجام شد")
        return reverse('account:login')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "شما وارد سایت شدید.")
        return reverse('item:list')
    

class UserUpdateView(UpdateView):
    template_name = 'update.html'
    form_class = UserUpdateForm

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user

    def get_success_url(self):
        if self.request.user != self.get_object():
            return redirect("item:list")
        messages.add_message(self.request, messages.SUCCESS, "اکانت با موفقیت ویرایش شد.")
        return reverse('account:dashboard')
    

class ProfielCreateView(View):
    template_name = 'profile-create.html'

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
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
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            phone_number = form.cleaned_data['phone_number']
            # 09123456789 or +989123456789
            phone_number = "09" + phone_number[-9:]
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
            messages.success(request, "پروفایل با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse("account:dashboard"))
        else:
            ctxt['form'] = ProfileCreateForm
        return render(request, self.template_name, self.get_context_data(**ctxt))


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'Profile-update.html'
    form_class = ProfileUpdateForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            Profile,
            user__username=self.kwargs['username']
        )

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "پروفایل با موفقیت ویرایش شد")
        return reverse('account:dashboard')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    form_class = UserPasswordChangeForm
    login_url = "account:login"
    
    def get_success_url(self):
        logout(self.request)
        messages.add_message(self.request, messages.SUCCESS, "گذرواژه با موفقیت تغییر کرد")
        return reverse('account:login')
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CompanyProfielCreateView(View):
    template_name = 'cprofile-create.html'

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
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
        form = CompanyProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            phone_number = form.cleaned_data['phone_number']
            phone_number = "09" + phone_number[-9:]
            home_phone_number = form.cleaned_data['home_phone_number']
            # 01732240742
            home_phone_number = "0" + home_phone_number[-10:]
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
                messages.success(request, "ثبت نام با موفقیت انجام شد. پس از تایید پروفایل می توایند محصول اضافه کنید.")
                return HttpResponseRedirect(reverse("account:dashboard"))
            profile.delete()
            messages.success(request, "ثبت نام با موفقیت انجام شد. پس از تایید پروفایل می توایند محصول اضافه کنید.")
            return HttpResponseRedirect(reverse("account:dashboard"))
        else:
            ctxt['form'] = CompanyProfileCreateForm

        return render(request, self.template_name, self.get_context_data(**ctxt))


class CompanyProfileUpdateView(UpdateView):
    model = CompanyProfile
    template_name  = "cprofile-update.html"
    form_class = CompanyProfileUpdateForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            CompanyProfile,
            user__username=self.kwargs['username']
        )
    

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "پروفایل با موفقیت ویرایش شد")
        return reverse('account:dashboard')