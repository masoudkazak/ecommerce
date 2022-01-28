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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['baskets'] = Order.objects.filter(user=self.request.user)
            return context
        context['baskets'] = None
        return context


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

        return render(request, self.template_name, self.get_context_data(**ctxt))


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'itemupdate.html'

    def get_success_url(self):
        item = self.get_object()
        return reverse_lazy("item:detail", args=(item.id,))


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'itemdelete.html'

    def get_success_url(self):
        return reverse('item:list')


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
    

class BasketView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order.html"

    def get_queryset(self):
        my_order = Order.objects.filter(user=self.request.user)
        return my_order


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
            return redirect('item:addresscreate')
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        ctxt = {}
        
        if 'choose' in request.POST:
            home_address = request.POST['fav-language']
            select_address = Address.objects.get(home_address=home_address)
            for address in self.get_object():
                if select_address == address:
                    select_address.this_address = True
                    select_address.save()
                else:
                    address.this_address = False
                    address.save()
        return render(request, self.template_name, self.get_context_data(**ctxt))


class AddressUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "addressupdate.html"
    form_class = AddressUpdateForm
    login_url = "/account/login/"
    model = Address

    def get_success_url(self):
        return reverse("item:address")


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
