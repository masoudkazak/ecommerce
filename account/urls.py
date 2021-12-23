from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


app_name = 'account'


urlpatterns = [
    path('create/', UserCreationView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('item:list')), name='logout'),
]
