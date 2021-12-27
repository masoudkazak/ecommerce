from .models import *
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect
from .forms import *


class PostListView(generic.ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'


class PostDetailView(ModelFormMixin ,generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'detail.html'
    form_class = PostCommentForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            text = form.cleaned_data['text']
            post = self.get_object()
            user = request.user
            new_comment = PostComment(text=text,
                                post=post,
                                user=user)
            new_comment.save()
            return redirect('blog:detail', pk=post.pk)