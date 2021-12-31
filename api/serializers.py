from django.contrib.auth.models import User
from rest_framework import serializers
from item.models import Item, Comment
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from account.models import Profile
from blog.models import Post
from blog.models import PostComment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['item',]


class ItemDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = ['name', 'company', 'price', 'body', 'images','tags', 'comments', 'category',]


class ItemSerializerUpdate(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ['name', 'company', 'price', 'body', 'images','tags', 'category', 'company',]


class ItemListSerializer(serializers.ModelSerializer):
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


class ProfileCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user',]


class UserCreationSerializer(serializers.ModelSerializer):
    profile = ProfileCreationSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'profile']
    
    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError("Enter more than 8 characters")
        return data
    
    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileCreationSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        user = super().update(instance, validated_data)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.save()
        instance.profile.image = profile_data.get('image', instance.profile.image)
        instance.profile.phone_number = profile_data.get('phone_number', instance.profile.image)
        instance.profile.bio = profile_data.get('bio', instance.profile.bio)
        instance.profile.gender = profile_data.get('gender', instance.profile.gender)
        instance.profile.save()
        return instance


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}
    )
    password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}
    )


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        exclude = ["post",]


class PostRetrieveSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    post_comments = PostCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['author', 'title', 'category', 'body', 'images','tags',
                  'post_comments', 'created', 'updated',]


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['author', 'title', 'category', 'body', 'images','tags',
                  'created', 'updated',]