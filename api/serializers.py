from django.contrib.auth.models import User
from rest_framework import serializers
from item.models import Item, Comment
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from rest_framework.serializers import ValidationError


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['item','id']


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
        fields = ['text','item', 'user']
        extra_kwargs = {
            'user': {'read_only':True}
        }


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]
    
    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError("Enter more than 8 characters")
        return data
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]
    
    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError("Enter more than 8 characters")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.save()
        return instance