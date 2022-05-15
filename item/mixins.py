import re
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from account.models import CompanyProfile
from item.models import Order, Address


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


class AddressListMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            messages.info(request, "آدرسی نساخته اید")
            return redirect("account:dashboard")
        count = 0
        for address in self.get_queryset():
            if address.user == request.user:
                count += 1
        if len(self.get_queryset()) == count or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class BasketMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            Order.objects.get(user=request.user)
        except Order.DoesNotExist:
            messages.info(request, "سبد شما خالی است")
            return redirect("account:dashboard")
        
        if self.get_object().user != request.user and not request.user.is_superuser:
            raise PermissionDenied

        if self.get_object().user == request.user or request.user.is_superuser:
            if not self.get_object().items.exists():
                messages.info(request, "سبد شما خالی است")
                return redirect("account:dashboard")
            try:
                self.get_context_data()['active_address']
            except Address.DoesNotExist:
                if not Address.objects.filter(user=request.user).exists():
                    messages.info(request, "آدرسی نساخته اید")
                    return redirect("item:address-create")
                messages.info(request, "آدرسی انتخاب نکرده اید")
                return redirect("item:address")

            return super().dispatch(request, *args, **kwargs)


class ItemListCategoryMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().items.exists():
            return super().dispatch(request, *args, **kwargs)
        messages.info(request, "محصولی وجود ندارد")
        return redirect("item:list")


class WatchListMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            return super().dispatch(request, *args, **kwargs)
        messages.info(request, "محصولی وجود ندارد")
        return redirect("item:list")
