from django import forms
from .models import Item, Comment


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['date',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]