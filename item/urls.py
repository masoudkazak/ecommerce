from django.urls import path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemUpdateView,
    ItemDeleteView,
    ItemCreateView,
)

app_name = 'item'


urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('item/create/', ItemCreateView.as_view(), name='create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='delete'),
    
]
