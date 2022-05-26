from django.urls import path
from .views import *


app_name = 'api'

urlpatterns = [
    path('home', ItemListAPIView.as_view(), name='item-list'),
    path('item/create/', ItemCreateAPIView.as_view(), name='item-create'),
    path('item/<slug:slug>/<int:pk>/', ItemRetrieveAPIView.as_view(), name='item-ddu'),
    path("item/comment/create", CommentCreateAPIView.as_view(), name="comment-create"),
    path("address/create/", AddressCreateView.as_view(), name="address-create"),
    path("addresses/", AddressListAPIView.as_view(), name="address-list"),
    path("addresses/<int:pk>/", AddressUpdateAPIView.as_view(), name="address-update"),
    path("basket/<int:pk>/", BasketView.as_view(), name="basket"),
    path("myitems/", MyItemListView.as_view(), name="my-items"),
    path("order/<str:username>/<int:pk>/", OrderitemRetrieveDestroyAPIView.as_view(), name="orderitem-delete"),

    path("account/create/", UserCreationAPIView.as_view(), name="account-creation"),
    path("account/<str:username>/", UserRetrieveUpdateAPIView.as_view(), name="account-retrieveupdate"),
    path("account/passwordchange/", UserChangePasswordAPIView.as_view(), name="account-changepassword"),
    path("profile/<str:username>/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-update"),
    path("companyprofile/create/", CompanyProfileCreateAPIView.as_view(), name="companyprofile-create"),
    path("companyprofile/update/<str:username>/", CompanyProfileRetrieveUpdateAPIView.as_view(), name="companyprofile-update"),
]
