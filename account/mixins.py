from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


class UserCreateLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "ابتدا از حساب خود خارج شوید")
            return redirect("item:list")
        return super().dispatch(request, *args, **kwargs)


class OwnerOrSuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ProfileUpdateOwnerOrSuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied