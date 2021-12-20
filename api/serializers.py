from django.db import models
from django.db.models import fields
from rest_framework import serializers
from item.models import Item, Comment
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['item',]


class ItemSerializerdetail(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = ['name', 'company', 'price', 'body', 'images','tags', 'comments', 'category']


class ItemSerializerlist(serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Item
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text','item']



