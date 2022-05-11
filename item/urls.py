from django.urls import path
from .views import *

app_name = 'item'


urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('item/create/', ItemCreateView.as_view(), name='create'),
    path('item/<slug:slug>/<int:pk>', ItemDetailView.as_view(), name='detail'),
    path('item/<slug:slug>/<int:pk>/update/', ItemUpdateView.as_view(), name='update'),
    path("address/", AddressView.as_view(), name="address"),
    path("address/<int:pk>/", AddressUpdateView.as_view(), name="address-update"),
    path("address/create/", AddressCreateView.as_view(), name="address-create"),
    path("<str:username>/basket/", BasketView.as_view(), name="basket"),
    path("myitem/", MyItemListView.as_view(), name="myitem"),
    path("item/category/<str:name>/", ItemListCategoryView.as_view(), name="itemscategory"),
    path("watchlist/", WatchListView.as_view(), name="watchlist"),
    path("addwatchlist/", AddWatchlist.as_view(), name="addwatchlist"),
    path("removewatchlist/", RemoveWatchlist.as_view(), name="removewatchlist"),
]
