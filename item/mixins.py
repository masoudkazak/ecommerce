from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from account.models import CompanyProfile

class PublishedItemMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().status == "d":
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ItemUpdateMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().company == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ItemCreateMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                cprofile = CompanyProfile.objects.get(user=request.user, confirm=True)
            except CompanyProfile.DoesNotExist:
                raise PermissionDenied
            else:
                return super().dispatch(request, *args, **kwargs)
        else:        
            return super().dispatch(request, *args, **kwargs)


class MyItemMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            messages.info(request, "محصولی وجود ندارد")
            return redirect("account:dashboard")
        return super().dispatch(request, *args, **kwargs)