from .models import Comment, Item
from django.views.generic import *
from .forms import ItemUpdateForm, CommentForm
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect


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
    
  