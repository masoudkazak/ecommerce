from .models import *
from django.views import generic, View
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect, render
from .forms import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


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
    

class PostCreateView(View):
    form_class = PostUpdateForm
    template_name = 'postcreate.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            body = form.cleaned_data['body']
            images = form.cleaned_data['images']
            tags = form.cleaned_data['tags']
            author = request.user
            new_post = Post.objects.create(
                title = title,
                category = category,
                body = body,
                images = images,
                tags = tags,
                author = author,
            )
            new_post.save()
            return HttpResponseRedirect(reverse('blog:list'))

        return render(request, self.template_name, {'form': form})


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "postdelete.html"
    
    def get_success_url(self):
        return reverse('blog:list')