from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from .models import *
from django.contrib.auth.models import User
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'


class ItemDetailView(ModelFormMixin ,DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'itemdetail.html'
    form_class = CommentForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            text = form.cleaned_data['text']
            item = self.get_object()
            user = request.user
            new_comment = Comment(text=text,
                                item=item,
                                user=user)
            new_comment.save()
            return redirect('item:detail', pk=item.pk)
    


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
    
  
class OrderItemView(ModelFormMixin, DetailView):
    model = User
    template_name = 'orderitem.html'
    form_class = OrderItemForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            item = form.cleaned_data['item']
            count = form.cleaned_data['count']

            if count == 0:
                messages.error(request, "صفر تعداد انتخاب کرده اید")
                return redirect('item:orderitem', pk=request.user.pk)

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


class BasketView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order.html"

    def get_queryset(self):
        my_order = Order.objects.filter(user=self.request.user)
        return my_order


class AddressView(LoginRequiredMixin ,FormMixin, ListView):
    model = Address
    form_class = AddressSelectForm
    template_name = "addresslist.html"
    login_url = "/account/login/"
    context_object_name = "addresses"
    
    def get_queryset(self):
        my_address = Address.objects.filter(user=self.request.user)
        return my_address
    
    # def get_form(self):
    #      form = self.get_form()



class AddressUpdateView(LoginRequiredMixin,UpdateView):
    model = Address
    template_name = "addressupdate.html"
    form_class = AddressUpdateForm
    login_url = "/account/login/"

    def get_success_url(self):
        return reverse("item:address")
