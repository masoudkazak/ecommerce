from django.urls import path
from .views import (
    ItemListAPIView,
    ItemRetrieveAPIView,
    ItemUpdateAPIView,
    ItemCreateAPIView,
)


app_name = 'api'


urlpatterns = [
    path('', ItemListAPIView.as_view(), name='apiitemlist'),
    path('item/create/', ItemCreateAPIView.as_view(), name='apiitemcreate'),
    path('detail/<int:pk>/', ItemRetrieveAPIView.as_view(), name='apiitemdetaildelete'),
    path('detail/<int:pk>/update/', ItemUpdateAPIView.as_view(), name='apiitemupdate'),
]
