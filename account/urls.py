from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


app_name = 'account'


urlpatterns = [
    path('create/', UserCreationView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('item:list')), name='logout'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('profile/create/<int:pk>/', ProfielCreateView.as_view(), name='profilecreate'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profileupdate'),
    path('passwordchange/', UserPasswordChangeView.as_view(), name='passwordchange'),
]
