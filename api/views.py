from item.models import Item
from rest_framework import generics
from .serializers import ItemSerializer


class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemUpdateAPIView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDestroyAPIView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer