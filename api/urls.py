from django.urls import path
from .views import *


app_name = 'api'


urlpatterns = [
    path('', ItemListAPIView.as_view(), name='itemlist'),
    path('item/create/', ItemCreateAPIView.as_view(), name='itemcreate'),
    path('item/<int:pk>/', ItemRetrieveAPIView.as_view(), name='itemdetaildeleteupdate'),
    path("item/comment/create", CommentCreateAPIView.as_view(), name="commnetcreate"),
    path("address/create/", AddressCreateView.as_view(), name="addresscreate"),
    path("addresses/", AddressListAPIView.as_view(), name="addresslist"),
    path("addresses/<int:pk>/", AddressUpdateAPIView.as_view(), name="addressupdate"),
    path("basket/", BasketView.as_view(), name="basket"),
    path("myitems/", MyItemListView.as_view(), name="myitems"),
    path("order/<int:customer>/<int:pk>/", OrderitemDeleteAPIView.as_view(), name="orderitemdelete"),

    path("account/create/", UserCreationAPIView.as_view(), name="accountcreation"),
    path("account/<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="accountretrieveupdate"),
    path("account/passwordchange/", UserChangePasswordAPIView.as_view(), name="accountchangepassword"),
    
    path("blog/", PostListAPIView.as_view(), name="bloglist"),
    path("blog/<int:pk>/", PostRetrieveDestroyAPIView.as_view(), name="blogdetaildelete"),
    path("blog/<int:pk>/update/", PostUpdateAPIView.as_view(), name="blogupdate"),

]
