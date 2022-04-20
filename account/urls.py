from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


app_name = 'account'


urlpatterns = [
    path('signin/', UserCreationView.as_view(), name='signin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('item:list')), name='logout'),
    path('<str:username>/update/', UserUpdateView.as_view(), name='update'),
    path('passwordchange/', UserPasswordChangeView.as_view(), name='passwordchange'),

    path('<str:username>/profile/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('<str:username>/profile/update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('<str:username>/cprofile/create/', CompanyProfileCreateView.as_view(), name='companyprofile-create'),
    path('<slug:username>/cprofile/update/', CompanyProfileUpdateView.as_view(), name='companyprofile-update'),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]

