from django import forms
from .models import PostComment, Post


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("text",)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title","category", "body", "images", "tags",)