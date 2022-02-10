from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'


class ItemDetailView(View):
    template_name = 'itemdetail.html'

    def get_object(self):
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        return item

    def get_context_data(self, **kwargs):
        kwargs['item'] = self.get_object()
        if 'orderitem_form' not in kwargs:
            kwargs['orderitem_form'] = OrderItemForm()
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = CommentForm()
        return kwargs
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                text = comment_form.cleaned_data['text']
                item = self.get_object()
                user = request.user
                new_comment = Comment(text=text,
                                    item=item,
                                    user=user)
                new_comment.save()
                return redirect('item:detail', pk=item.pk)
            else:
                ctxt['response_form'] = CommentForm

        elif 'orderitem' in request.POST:
            orderitem_form = OrderItemForm(request.POST)
            item = self.get_object()
            if orderitem_form.is_valid():
                count = orderitem_form.cleaned_data['count']

                if count == 0:
                    messages.error(request, "صفر تعداد انتخاب کرده اید")
                    return redirect('item:detail', pk=item.pk)

                try:      
                    update_orderitem = OrderItem.objects.get(item=item)
                except OrderItem.DoesNotExist:
                    new_orderitem = OrderItem.objects.create(item=item,
                                        count=count,
                                        customer=request.user)
                    new_orderitem.save()
                else:
                    update_orderitem.count = update_orderitem.count + count
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

                return redirect('item:list')
            else:
                ctxt['response_form'] = CommentForm

        elif "deleteitem" in request.POST:
            item = self.get_object()
            item.delete()
            return HttpResponseRedirect(reverse("item:list"))

        return render(request, self.template_name, self.get_context_data(**ctxt))


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'itemupdate.html'
    context_object_name = "item"

    def get_success_url(self):
        item = self.get_object()
        return reverse_lazy("item:detail", args=(item.id,))
        

class ItemCreateView(View):
    form_class = ItemUpdateForm
    template_name = 'itemcreate.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            body = form.cleaned_data['body']
            images = form.cleaned_data['images']
            tags = form.cleaned_data['tags']
            company = request.user
            new_item = Item.objects.create(
                name = name,
                category = category,
                price = price,
                body = body,
                images = images,
                tags = tags,
                company = company,
            )
            new_item.save()
            return HttpResponseRedirect(reverse('item:list'))

        return render(request, self.template_name, {'form': form})

    
    def get_success_url(self):
        order = self.get_object()
        return reverse_lazy("item:basket", args=(order.id,))


class AddressView(LoginRequiredMixin ,View):
    template_name = "addresslist.html"
    login_url = "/account/login/"

    def get_object(self):
        addresses =Address.objects.filter(user=self.request.user)
        count = 0
        # if there is bug, all addresses change to False
        for address in addresses:
            if address.this_address == True:
                count += 1
        if count > 1:
            for address in addresses:
                if address.this_address == True:
                    address.this_address = False
                    address.save()
        return addresses
    
    def get_context_data(self, **kwargs):
        kwargs['addresses'] = self.get_object()
        return kwargs
    
    def get(self, request, *args, **kwargs):
        if len(self.get_object()) == 0:
            messages.info(request, "شما آدرسی نساخته اید")
            return redirect('item:addresscreate')
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        
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
                return HttpResponseRedirect(reverse('item:list'))
            else:
                messages.info(request, "آدرسی انتخاب نکردید")
                return redirect("item:address")
        return render(request, self.template_name, self.get_context_data(**ctxt))


class AddressUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "addressupdate.html"
    form_class = AddressUpdateForm
    login_url = "/account/login/"
    model = Address

    def get_success_url(self):
        return reverse("item:address")
    
    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            address = self.get_object()
            address.delete()
            return HttpResponseRedirect(reverse("item:address"))
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return redirect("item:list")
        return super().get(request, *args, **kwargs)


class AddressCreateView(LoginRequiredMixin, View):
    form_class = AddressUpdateForm
    template_name = "addresscreate.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, requset, *args, **kwargs):
        form = AddressUpdateForm(requset.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            home_address = form.cleaned_data['home_address']
            mobile_number = form.cleaned_data['mobile_number']
            body = form.cleaned_data['body']
            user = requset.user
            new_address = Address.objects.create(
                zip_code = zip_code,
                home_address = home_address,
                mobile_number = mobile_number,
                body = body,
                user = user,
                this_address = False,
            )
            new_address.save()
            return HttpResponseRedirect(reverse("item:address"))
            
        return render(requset, self.template_name, {"form":form})


class BasketView(LoginRequiredMixin ,View):
    template_name = "basket.html"
    login_url = "/account/login/"

    def get_object(self):
        order =Order.objects.get(user=self.request.user)
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
            return redirect('item:list')

        if not self.get_object().items.all().exists():
            messages.info(request, "سبد شما خالی است")
            return redirect('item:list')

        try:
            self.get_context_data()['active_address']
        except Address.DoesNotExist:
            if len(Address.objects.filter(user=request.user)) == 0:
                messages.info(request, "آدرسی نساخته اید")
                return redirect("item:addresscreate")
            messages.info(request, "آدرسی انتخاب نکرده اید")
            return redirect("item:address")

        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        item_list = self.get_object().items.all()
        print(request.POST)
        for item in item_list:
            delete = "delete-" + str(item.id)
            if delete in request.POST:
                item.delete()
                return HttpResponseRedirect(reverse("item:basket")) 
            x = int(request.POST[str(item.id)])
            item.count = x
            item.save()

        return HttpResponseRedirect(reverse("item:basket"))
            
        return render(request, self.template_name, self.get_context_data(**ctxt))