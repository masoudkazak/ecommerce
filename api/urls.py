from django.urls import path
from .views import *


app_name = 'api'


urlpatterns = [
    path('', ItemListAPIView.as_view(), name='itemlist'),
    path('item/create/', ItemCreateAPIView.as_view(), name='itemcreate'),
    path('detail/<int:pk>/', ItemRetrieveAPIView.as_view(), name='itemdetaildelete'),
    path('detail/<int:pk>/update/', ItemUpdateAPIView.as_view(), name='itemupdate'),
    path("item/comment/create", CommentCreateAPIView.as_view(), name="commnetcreate"),
    path("account/create/", UserCreationAPIView.as_view(), name="accountcreation"),
    path("account/<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="accountretrieveupdate"),
]
