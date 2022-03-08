from django.contrib.auth.models import User
from item.models import Item, Comment
from blog.models import Post

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters

from .serializers import *


# list Item api views
class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.filter(status="p")
    serializer_class = ItemListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class ItemRetrieveAPIView(generics.RetrieveDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class ItemUpdateAPIView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerUpdate


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list Account api views
class UserCreationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class UserRetrieveUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer


class UserChangePasswordAPIView(generics.UpdateAPIView):
        serializer_class = UserPasswordChangeSerializer
        model = User

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                if serializer.data.get('password1') != serializer.data.get('password2'):
                    return Response({"passwords": ["Not same"]}, status=status.HTTP_400_BAD_REQUEST)

                self.object.set_password(serializer.data.get("password1"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password Change Done',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list Blog api views
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class PostCreateAPIView(generics.CreateAPIView):
    pass