from item.models import Item, Comment
from rest_framework import generics
from .serializers import ItemSerializerdetail, ItemSerializerlist


class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerlist


class ItemRetrieveAPIView(generics.RetrieveDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ItemUpdateAPIView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerdetail

