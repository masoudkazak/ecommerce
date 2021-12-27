from .models import *
from django.views import generic

class PostListView(generic.ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
