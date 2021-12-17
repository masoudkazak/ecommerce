from .models import Item
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from .forms import ItemUpdateForm, CommentForm
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.http import HttpResponseForbidden


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'


class ItemDetailView(FormMixin ,DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'itemdetail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('item:detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'itemupdate.html'


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'itemdelete.html'

    def get_success_url(self):
        return reverse('item:list')


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'itemcreate.html'

    def get_success_url(self):
        return reverse('item:list')
    