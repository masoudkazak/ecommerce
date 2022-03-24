from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


app_name = 'account'


urlpatterns = [
    path('create/', UserCreationView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('item:list')), name='logout'),
    path('<str:username>/update/', UserUpdateView.as_view(), name='update'),
    path('passwordchange/', UserPasswordChangeView.as_view(), name='passwordchange'),

    path('<str:username>/profile/create/', ProfielCreateView.as_view(), name='profilecreate'),
    path('<str:username>/profile/update/', ProfileUpdateView.as_view(), name='profileupdate'),

    path('<str:username>/cprofile/create/', CompanyProfielCreateView.as_view(), name='companyprofilecreate'),
    path('<slug:username>/cprofile/update/', CompanyProfileUpdateView.as_view(), name='companyprofileupdate'),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]

