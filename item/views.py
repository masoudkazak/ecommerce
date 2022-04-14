from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from account.models import CompanyProfile


class ItemListView(ListView):
    template_name = 'home.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Item.objects.filter(status="p")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context['search_form'] = ItemSearchForm()
        return context

    def post(self, request, *args, **kwargs):
        if "search" in request.POST:
            search_form = ItemSearchForm(request.POST)
            if search_form.is_valid():
                qs = Item.objects.search(query=search_form.cleaned_data['lookup']).filter(status="p")
                ctxt = {"qs": qs}
                return render(request, "itemsearch.html", context=ctxt)
            return redirect("item:list")


class ItemDetailView(View):
    template_name = 'itemdetail.html'

    def get_object(self):
        item = get_object_or_404(Item, name=self.kwargs['name'], pk=self.kwargs['pk'])
        return item

    def get_context_data(self, **kwargs):
        kwargs['item'] = self.get_object()
        if 'orderitem_form' not in kwargs:
            kwargs['orderitem_form'] = OrderItemForm()
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = CommentForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        if self.get_object().status == "d":
            return redirect("item:list")
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                text = comment_form.cleaned_data['text']
                item = self.get_object()
                user = request.user
                new_comment = Comment(text=text, item=item, user=user)
                new_comment.save()
                messages.success(request, "کامت شما ثبت شد")
                return redirect('item:detail', pk=item.pk, name=item.name)
            else:
                context['response_form'] = CommentForm

        elif 'orderitem' in request.POST:
            orderitem_form = OrderItemForm(request.POST)
            item = self.get_object()
            if orderitem_form.is_valid():
                count = orderitem_form.cleaned_data['count']
                if count == 0:
                    messages.error(request, "هیچ تعداد محصولی انتخاب نکرده اید")
                    return redirect('item:detail', pk=item.pk, name=item.name)
                elif count > item.inventory:
                    messages.info(request, "بیش از حد ظرفیت موجود")
                    return redirect('item:detail', pk=item.pk, name=item.name)
                elif request.user == item.company:
                    messages.error(request, "این محصول شماست نمیتوانید به سبد خود ارسال کنید")
                    return redirect("item:detail", pk=item.pk, name=item.name)

                try:
                    update_orderitem = OrderItem.objects.get(item=item)
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=item,
                                                             count=count,
                                                             customer=request.user)
                    new_orderitem.save()
                else:
                    update_orderitem.count += count
                    update_orderitem.save()

                try:
                    update_order = Order.objects.get(user=request.user)
                except Order.DoesNotExist:
                    new_order = Order(
                        user=request.user,
                    )
                    new_order.save()
                    new_order.items.add(OrderItem.objects.get(item=item))
                else:
                    update_order.items.add(OrderItem.objects.get(item=item))
                messages.success(request, "به سبد اضافه شد")
                return HttpResponseRedirect(reverse('item:detail', args=[item.name, item.id, ]))
            else:
                context['response_form'] = CommentForm

        elif "deleteitem" in request.POST:
            item = self.get_object()
            item.delete()
            messages.success(request, "محصول شما حذف شد")
            return HttpResponseRedirect(reverse("item:list"))

        elif "empty" in request.POST:
            item = self.get_object()
            item.inventory = 0
            item.save()
            messages.success(request, "محصول ناموجود شد")
            return HttpResponseRedirect(reverse("item:detail", args=[item.name, item.id, ]))
        return render(request, self.template_name, self.get_context_data(**context))


class ItemUpdateView(UpdateView):
    form_class = ItemForm
    template_name = 'itemupdate.html'
    context_object_name = "item"

    def get_object(self):
        item = get_object_or_404(Item, name=self.kwargs['name'], pk=self.kwargs['pk'])
        return item

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "محصول با موفقیت ویرایش شد")
        return reverse("account:dashboard")


class ItemCreateView(CreateView):
    template_name = 'itemcreate.html'
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # def get(self, request, *args, **kwargs):
    #     if not request.user.is_superuser:
    #         try:
    #             cprofile = CompanyProfile.objects.get(user=request.user)
    #         except CompanyProfile.DoesNotExist:
    #             return redirect("item:list")
    #         else:
    #             if not cprofile.confirm:
    #                 return redirect("item:list")
    #     return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST, request=request)
        if form.is_valid():
            if not request.user.is_superuser:
                company = request.user
                status = "d"
            else:
                company = form.cleaned_data['company']
                status = form.cleaned_data['status']
            new_item = Item.objects.create(name=form.cleaned_data['name'],
                                           category=form.cleaned_data['category'],
                                           price=form.cleaned_data['price'],
                                           body=form.cleaned_data['body'],
                                           tags=form.cleaned_data['tags'],
                                           company=company,
                                           inventory=form.cleaned_data['inventory'],
                                           discount=form.cleaned_data['discount'],
                                           status=status)
            new_item.save()
            item = Item.objects.get(name=form.cleaned_data['name'],
                                    price=form.cleaned_data['price'],
                                    company=company,
                                    inventory=form.cleaned_data['inventory'],)

            for image in request.FILES.getlist("images"):
                Uploadimage.objects.create(image=image, item_id=item.id)

            for color in form.cleaned_data['color']:
                item.color.add(color)

            images_list = Uploadimage.objects.filter(item_id=item.id)

            for image in images_list:
                item.images.add(image)
            messages.success(request, "محصول شما ثبت شد. پس از تایید محصول منتشر خواهد شد")
            return HttpResponseRedirect(reverse('item:myitem'))

        return render(request, self.template_name, {'form': form})


class AddressView(LoginRequiredMixin, View):
    template_name = "addresslist.html"
    login_url = "/account/login/"

    def get_object(self):
        addresses = Address.objects.filter(user=self.request.user)
        count = 0
        # if there is bug, all addresses change to False
        for address in addresses:
            if address.this_address:
                count += 1
        if count > 1:
            for address in addresses:
                if address.this_address:
                    address.this_address = False
                    address.save()
        return addresses

    def get_context_data(self, **kwargs):
        kwargs['addresses'] = self.get_object()
        return kwargs

    def get(self, request, *args, **kwargs):
        if not self.get_object().exists():
            messages.info(request, "شما آدرسی نساخته اید")
            return redirect('item:addresscreate')
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}

        if 'choose' in request.POST:
            if 'fav-language' in request.POST:
                home_address = request.POST['fav-language']
                select_address = Address.objects.get(home_address=home_address)
                for address in self.get_object():
                    if select_address == address:
                        select_address.this_address = True
                        select_address.save()
                    else:
                        address.this_address = False
                        address.save()
                messages.success(request, "آدرس شما انتخاب شد")
                return HttpResponseRedirect(reverse('item:address'))
            messages.error(request, "آدرسی انتخاب نکردید")
            return redirect("item:address")
        return render(request, self.template_name, self.get_context_data(**context))


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "addressupdate.html"
    form_class = AddressForm
    login_url = "/account/login/"
    model = Address

    def get_form_kwargs(self):
        kwargs = super(AddressUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "آدرس شما با موفقیت ویرایش شد")
        return reverse("item:address")

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            self.get_object().delete()
            messages.success(request, "آدرش شما حذف شد")
            return HttpResponseRedirect(reverse("item:address"))
        return super().post(request, *args, **kwargs)


class AddressCreateView(LoginRequiredMixin, CreateView):
    form_class = AddressForm
    template_name = "addresscreate.html"
    model = Address

    def get_form_kwargs(self):
        kwargs = super(AddressCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST, request=request)
        if form.is_valid():
            if not request.user.is_superuser:
                user = request.user
            else:
                user = form.cleaned_data['user']
            new_address = Address.objects.create(
                zip_code=form.cleaned_data['zip_code'],
                home_address=form.cleaned_data['home_address'],
                mobile_number="09" + form.cleaned_data['mobile_number'][-9:],
                body=form.cleaned_data['body'],
                user=user,
                this_address=False,
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province']
            )
            new_address.save()
            messages.success(self.request, "آدرس جدید اضافه شد")
            return HttpResponseRedirect(reverse("item:address"))
        form = AddressForm()
        return render(request, self.template_name, {"form": form})


class BasketView(LoginRequiredMixin, View):
    template_name = "basket.html"
    login_url = "/account/login/"

    def get_object(self):
        order = Order.objects.get(user=self.request.user)
        return order

    def get_context_data(self, **kwargs):
        kwargs['order'] = self.get_object()
        kwargs['active_address'] = Address.objects.get(user=self.request.user, this_address=True)
        return kwargs

    def get(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Order.DoesNotExist:
            messages.info(request, "سبد شما خالی است")
            return redirect('account:dashboard')

        if not self.get_object().items.all().exists():
            messages.info(request, "سبد شما خالی است")
            return redirect('account:dashboard')
        try:
            self.get_context_data()['active_address']
        except Address.DoesNotExist:
            if not Address.objects.filter(user=request.user).exists():
                messages.info(request, "آدرسی نساخته اید")
                return redirect("item:addresscreate")
            messages.info(request, "آدرسی انتخاب نکرده اید")
            return redirect("item:address")
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        item_list = self.get_object().items.all()
        for item in item_list:
            delete = "delete-" + str(item.id)
            if delete in request.POST:
                item.delete()
                messages.success(request, "محصول مورد نظر حذف گردید")
                return HttpResponseRedirect(reverse("item:basket"))
            x = int(request.POST[str(item.id)])
            if x > item.item.inventory:
                messages.error(request, "بیش از حد ظرفیت موجود")
                return redirect("item:basket")
            item.count = x
            item.save()
        messages.success(request, "تغییرات انجام شد")
        return HttpResponseRedirect(reverse("item:basket"))


class MyItemListView(LoginRequiredMixin, ListView):
    template_name = "my_item.html"
    context_object_name = "items"

    def get_queryset(self):
        items = Item.objects.filter(company=self.request.user).order_by("status")
        return items

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            messages.info(request, "محصولی وجود ندارد")
            return redirect("account:dashboard")
        return super().get(request, *args, **kwargs)
