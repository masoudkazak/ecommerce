from .models import *
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect
from .forms import *
from django.urls import reverse_lazy


class PostListView(generic.ListView):
    model = Post
    template_name = 'postlist.html'
    context_object_name = 'posts'


class PostDetailView(ModelFormMixin ,generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'postdetail.html'
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


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = 'postupdate.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('blog:detail', args=(post.id,))
    
