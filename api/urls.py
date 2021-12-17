from django.urls import path
from .views import (
    ItemListAPIView,
    ItemRetrieveAPIView,
    ItemUpdateAPIView,
    ItemDestroyAPIView,
    ItemCreateAPIView,
)


app_name = 'api'


urlpatterns = [
    path('', ItemListAPIView.as_view(), name='apiitemlist'),
    path('item/create/', ItemCreateAPIView.as_view(), name='apiitemcreate'),
    path('detail/<int:pk>/', ItemRetrieveAPIView.as_view(), name='apiitemdetail'),
    path('detail/<int:pk>/update/', ItemUpdateAPIView.as_view(), name='apiitemupdate'),
    path('detail/<int:pk>/delete/', ItemDestroyAPIView.as_view(), name='apiitemdelete'),
]
