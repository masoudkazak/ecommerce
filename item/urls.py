from django.urls import path
from .views import *

app_name = 'item'


urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('item/create/', ItemCreateView.as_view(), name='create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='update'),
    path("address/", AddressView.as_view(), name="address"),
    path("address/<int:pk>/", AddressUpdateView.as_view(), name="addressupdate"),
    path("address/create/", AddressCreateView.as_view(), name="addresscreate"),
    path("basket/", BasketView.as_view(), name="basket")
]
