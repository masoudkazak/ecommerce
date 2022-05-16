from termios import VINTR
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .mixins import *
from account.mixins import ProfileUpdateOwnerOrSuperuserMixin
from django.db.models import Q, F
from django.core.paginator import Paginator


class ItemListView(ListView):
    template_name = 'home.html'
    paginate_by = 6
    queryset = Item.objects.filter(status="p").order_by('-inventory', "date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(self.queryset, self.paginate_by)
        context["items"] = p.page(context['page_obj'].number)
        context["categories"] = Category.objects.all()
        context['search_form'] = ItemSearchForm()
        context['addbasketlist_form'] = AddbasketListForm()
        if self.request.user.is_authenticated:
            context['num_watchlist'] = WatchList.num_watchlist(self, self.request.user)
        else:
            context['num_watchlist'] = 0
        context['average_dict'] = Comment.get_averages_dict(self, self.queryset)
        if self.request.user.is_authenticated:
            context['are_there_watchlist'] = WatchList.are_there_watchlist(self, self.queryset, self.request.user)
            context['num_basket'] = Order.get_number_basket(self, self.request.user)
            context['items_basket'] = Order.get_items_basket(self, self.request.user)
            context['final_price'] = Order.get_final_price_order(self, self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.queryset
        context = {}
        if "search" in request.POST:
            search_form = ItemSearchForm(request.POST)
            if search_form.is_valid():
                qs = Item.objects.search(query=search_form.cleaned_data['lookup']).filter(status="p")
                ctxt = {"qs": qs}
                return render(request, "itemsearch.html", context=ctxt)
            else:
                context["search_form"] = search_form
                    
        for item in self.object_list.filter(~Q(inventory=0)):    
            if str(item) in request.POST:
                if request.user == item.company:
                    messages.error(request, "این محصول شماست نمیتوانید به سبد خود ارسال کنید")
                    return redirect("item:list")

                try:
                    update_orderitem = OrderItem.objects.get(item=item, customer=request.user)
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=item,
                                                                count=1,
                                                                customer=request.user)
                    new_orderitem.save()
                else:
                    update_orderitem.count += 1
                    update_orderitem.save()

                try:
                    update_order = Order.objects.get(user=request.user)
                except Order.DoesNotExist:
                    new_order = Order(
                        user=request.user,
                    )
                    new_order.save()
                    new_order.items.add(OrderItem.objects.get(item=item, customer=request.user))
                else:
                    update_order.items.add(OrderItem.objects.get(item=item, customer=request.user))
                messages.success(request, "به سبد اضافه شد")
                return HttpResponseRedirect(reverse('item:list'))
        return render(request, self.template_name, self.get_context_data(**context))


class ItemDetailView(PublishedItemMixin, View):
    template_name = 'itemdetail.html'

    def get_object(self):
        item = get_object_or_404(Item, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        return item

    def get_context_data(self, **kwargs):
        kwargs['item'] = self.get_object()
        kwargs['company_name'] = CompanyProfile.get_name(self, self.get_object().company)
        same_items = []
        for tag in self.get_object().tags.all():
            same_items += Item.objects.filter(tags=tag).filter(~Q(name=self.get_object().name))
        kwargs["same_items"] = same_items
        if 'orderitem_form' not in kwargs:
            kwargs['orderitem_form'] = OrderItemForm()
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = CommentForm()
        kwargs['dict_point_users'] = Comment.dict_point_users(self, self.get_object())
        if self.request.user.is_authenticated:
            kwargs['is_there_watchlist'] = WatchList.is_there_watchlist(self, self.request.user, self.get_object())
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                text = comment_form.cleaned_data['text']
                if 'rating' in request.POST:
                    point = int(request.POST['rating'])
                else:
                    point = None
                item = self.get_object()
                user = request.user
                new_comment = Comment(item=item, user=user, text=text, point=point)
                new_comment.save()
                messages.success(request, "کامت شما ثبت شد")
                return redirect('item:detail', pk=item.pk, slug=item.slug)
            else:
                context['response_form'] = CommentForm

        elif 'orderitem' in request.POST:
            orderitem_form = OrderItemForm(request.POST)
            item = self.get_object()
            if orderitem_form.is_valid():
                count = orderitem_form.cleaned_data['count']
                if count == 0:
                    messages.error(request, "هیچ تعداد محصولی انتخاب نکرده اید")
                    return redirect('item:detail', pk=item.pk, slug=item.slug)
                elif count > item.inventory:
                    messages.info(request, "بیش از حد ظرفیت موجود")
                    return redirect('item:detail', pk=item.pk, slug=item.slug)
                elif request.user == item.company:
                    messages.error(request, "این محصول شماست نمیتوانید به سبد خود ارسال کنید")
                    return redirect("item:detail", pk=item.pk, slug=item.slug)

                try:
                    update_orderitem = OrderItem.objects.get(item=item, customer=request.user, color=orderitem_form.cleaned_data['color'])
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=item,
                                                             count=count,
                                                             color=request.POST['color'],
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
                return HttpResponseRedirect(reverse('item:detail', args=[item.slug, item.id, ]))
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
            return HttpResponseRedirect(reverse("item:detail", args=[item.slug, item.id, ]))
        
        elif str(self.get_object()) + "add" in request.POST:
            watchlist = WatchList.objects.create(user=request.user, item=self.get_object())
            watchlist.save()
            messages.success(request, "به علاقه مندی ها اضافه شد")
            return HttpResponseRedirect(reverse("item:detail", args=[self.get_object().slug, self.get_object().id, ]))

        elif str(self.get_object()) + "del" in request.POST:
            watchlist = WatchList.objects.get(user=request.user, item=self.get_object())
            watchlist.delete()
            messages.success(request, "از علاقه مندی ها حذف شد")
            return HttpResponseRedirect(reverse("item:detail", args=[self.get_object().slug, self.get_object().id, ]))

        return render(request, self.template_name, self.get_context_data(**context))


class ItemUpdateView(ItemUpdateMixin, UpdateView):
    form_class = ItemForm
    template_name = 'itemupdate.html'
    context_object_name = "item"

    def get_object(self):
        item = get_object_or_404(Item, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        return item

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "محصول با موفقیت ویرایش شد")
        return reverse("account:dashboard")


class ItemCreateView(LoginRequiredMixin, ItemCreateMixin, CreateView):
    template_name = 'itemcreate.html'
    form_class = ItemForm
    login_url = "/login/"

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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


class AddressView(LoginRequiredMixin,AddressListMixin, View):
    template_name = "addresslist.html"
    login_url = "/login/"

    def get_queryset(self):
        addresses = Address.update_my_address(self, self.request.user)
        return addresses
 
    def get_context_data(self, **kwargs):
        kwargs['addresses'] = self.get_queryset()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}

        if 'choose' in request.POST:
            if 'fav-language' in request.POST:
                home_address = request.POST['fav-language']
                Address.unactive_all_addresses(self, request.user)
                select_address = Address.objects.get(home_address=home_address)
                select_address.this_address = True
                select_address.save()
                messages.success(request, "آدرس شما انتخاب شد")
                return HttpResponseRedirect(reverse('item:address'))
            messages.error(request, "آدرسی انتخاب نکردید")
            return redirect("item:address")
        return render(request, self.template_name, self.get_context_data(**context))


class AddressUpdateView(LoginRequiredMixin, ProfileUpdateOwnerOrSuperuserMixin, UpdateView):
    template_name = "addressupdate.html"
    form_class = AddressForm
    login_url = "/login/"
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
    login_url = "/login/"

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


class BasketView(LoginRequiredMixin, BasketMixin, View):
    template_name = "basket.html"
    login_url = "/login/"
    
    def get_object(self):
        return get_object_or_404(Order, user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        kwargs['order'] = self.get_object()
        kwargs['active_address'] = Address.objects.get(user=self.request.user, this_address=True)
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        item_list = self.get_object().items.all()
        for item in item_list:
            delete = "delete-" + str(item.id)
            if delete in request.POST:
                item.delete()
                messages.success(request, "محصول مورد نظر حذف گردید")
                return HttpResponseRedirect(reverse("item:basket", args=[request.user.username]))
            x = int(request.POST[str(item.id)])
            if x > item.item.inventory:
                messages.error(request, "بیش از حد ظرفیت موجود")
                return redirect("item:basket", username=request.user.username)
            item.count = x
            item.save()
        messages.success(request, "تغییرات انجام شد")
        return HttpResponseRedirect(reverse("item:basket", args=[request.user.username]))


class MyItemListView(LoginRequiredMixin, MyItemMixin, ListView):
    template_name = "my_item.html"
    context_object_name = "items"

    def get_queryset(self):
        items = Item.objects.filter(company=self.request.user).order_by("status")
        return items


class ItemListCategoryView(ItemListCategoryMixin, DetailView):
    template_name = "items-category.html"

    def get_object(self):
        category = get_object_or_404(Category, name=self.kwargs['name'])
        return category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_object()
        items = Item.objects.filter(category=self.get_object())
        context['average_dict'] = Comment.get_averages_dict(self, items)
        return context

    def post(self, request, *args, **kwargs):
        items = Item.objects.filter(category=self.get_object()).filter(~Q(inventory=0))
        context = {}
        for item in items:
            if str(item) in request.POST:
                if request.user == item.company:
                    messages.error(request, "این محصول شماست نمیتوانید به سبد خود ارسال کنید")
                    return redirect("item:list")

                try:
                    update_orderitem = OrderItem.objects.get(item=item, customer=request.user)
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=item,
                                                                count=1,
                                                                customer=request.user)
                    new_orderitem.save()
                else:
                    update_orderitem.count += 1
                    update_orderitem.save()

                try:
                    update_order = Order.objects.get(user=request.user)
                except Order.DoesNotExist:
                    new_order = Order(
                        user=request.user,
                    )
                    new_order.save()
                    new_order.items.add(OrderItem.objects.get(item=item, customer=request.user))
                else:
                    update_order.items.add(OrderItem.objects.get(item=item, customer=request.user))
                messages.success(request, "به سبد اضافه شد")
                return HttpResponseRedirect(reverse('item:watchlist'))
        return render(request, self.template_name, self.get_context_data(**context))



class WatchListView(LoginRequiredMixin, WatchListMixin, ListView):
    template_name = "watchlist.html"
    context_object_name = "watchlists"

    def get_queryset(self):
        queryset = WatchList.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(~Q(item__inventory=0))
        context = {}
        for watchlist in self.object_list:
            if str(watchlist.item) in request.POST:
                if request.user == watchlist.item.company:
                    messages.error(request, "این محصول شماست نمیتوانید به سبد خود ارسال کنید")
                    return redirect("item:list")

                try:
                    update_orderitem = OrderItem.objects.get(item=watchlist.item, customer=request.user)
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=watchlist.item,
                                                                count=1,
                                                                customer=request.user)
                    new_orderitem.save()
                else:
                    update_orderitem.count += 1
                    update_orderitem.save()

                try:
                    update_order = Order.objects.get(user=request.user)
                except Order.DoesNotExist:
                    new_order = Order(
                        user=request.user,
                    )
                    new_order.save()
                    new_order.items.add(OrderItem.objects.get(item=watchlist.item, customer=request.user))
                else:
                    update_order.items.add(OrderItem.objects.get(item=watchlist.item, customer=request.user))
                messages.success(request, "به سبد اضافه شد")
                return HttpResponseRedirect(reverse('item:watchlist'))
        return render(request, self.template_name, self.get_context_data(**context))


class AddWatchlist(View):
    def get(self, request, *args, **kwargs):
        item_id = request.GET['item_id']
        item = Item.objects.get(id=item_id)
        w = WatchList(item=item, user=request.user)
        w.save()
        return HttpResponse("Success")


class RemoveWatchlist(View):
    def get(self, request, *args, **kwargs):
        item_id = request.GET['item_id']
        item = Item.objects.get(id=item_id)
        w = WatchList.objects.get(item=item, user=request.user)
        w.delete()
        return HttpResponse("Success")
