from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout, get_user_model

from .forms import *
from .models import *
from .mixins import *


User = get_user_model()


class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        return redirect('account:update', username=request.user.username, )


class UserCreationView(UserCreateLoginMixin ,CreateView):
    model = User
    template_name = 'create.html'
    form_class = UserCreateForm

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "ثبت نام شما با موفقیت انجام شد")
        return reverse('account:login')


class UserLoginView(UserCreateLoginMixin, LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "شما وارد سایت شدید.")
        return reverse('item:list')
    

class UserUpdateView(OwnerOrSuperuserMixin, UpdateView):
    template_name = 'update.html'
    form_class = UserUpdateForm

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "اکانت با موفقیت ویرایش شد.")
        return reverse('account:dashboard')
    

class ProfileCreateView(OwnerOrSuperuserMixin, CreateView):
    template_name = 'profile-create.html'
    model = Profile
    form_class = ProfileCreateForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_form_kwargs(self):
        kwargs = super(ProfileCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES, request=request)
        if form.is_valid():
            if request.user.is_superuser:
                profile = Profile.objects.create(**form.cleaned_data)
            else:
                user = request.user
                profile = Profile.objects.create(user=user, **form.cleaned_data)
            profile.save()
            messages.success(request, "پروفایل با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse("account:dashboard"))


class ProfileUpdateView(ProfileUpdateOwnerOrSuperuserMixin, UpdateView):
    model = Profile
    template_name = 'Profile-update.html'
    form_class = ProfileUpdateForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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


class CompanyProfileCreateView(OwnerOrSuperuserMixin, CreateView):
    template_name = 'cprofile-create.html'
    form_class = CompanyProfileForm

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user

    def get_form_kwargs(self):
        kwargs = super(CompanyProfileCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        form = CompanyProfileForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            home_phone_number = form.cleaned_data['home_phone_number']
            # 02134567899
            home_phone_number = "0" + home_phone_number[-10:]
            try:
                CompanyProfile.objects.get(home_phone_number=home_phone_number)
            except CompanyProfile.DoesNotExist:
                if request.user.is_superuser:
                    user = form.cleaned_data['user']
                    confirm = form.cleaned_data['confirm']
                else:
                    user = self.request.user
                    confirm = False
                new_profile = CompanyProfile.objects.create(user=user,
                                                            image=form.cleaned_data['image'],
                                                            bio=form.cleaned_data['bio'],
                                                            name=form.cleaned_data['name'],
                                                            address_company=form.cleaned_data['address_company'],
                                                            home_phone_number=home_phone_number,
                                                            confirm=confirm)
                new_profile.save()
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    messages.success(request, "ثبت نام با موفقیت انجام شد. پس از تایید پروفایل می توایند محصول اضافه کنید.")
                    return HttpResponseRedirect(reverse("account:dashboard"))
                profile.delete()
                messages.success(request, "ثبت نام با موفقیت انجام شد. پس از تایید پروفایل می توایند محصول اضافه کنید.")
                return HttpResponseRedirect(reverse("account:dashboard"))
            else:
                messages.error(request, "این شماره از قبل موجود است")
        form = CompanyProfileForm(request=request)
        return render(request, self.template_name, {"form": form})


class CompanyProfileUpdateView(ProfileUpdateOwnerOrSuperuserMixin, UpdateView):
    model = CompanyProfile
    template_name = "cprofile-update.html"
    form_class = CompanyProfileForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(CompanyProfile, user__username=self.kwargs['username'])

    def get_form_kwargs(self):
        kwargs = super(CompanyProfileUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "پروفایل با موفقیت ویرایش شد")
        return reverse('account:dashboard')
