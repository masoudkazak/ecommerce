from django.contrib.auth.models import User
from item.models import Item, Comment
from rest_framework import generics, status
from .serializers import (ItemSerializerdetail,
                          ItemSerializerlist,
                          CommentCreateSerializer,
                          UserRetrieveUpdateSerializer,
)
from rest_framework.response import Response
from .serializers import UserCreationSerializer
    

class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerlist


class ItemRetrieveAPIView(generics.RetrieveDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail


class ItemUpdateAPIView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
