from django.urls import path
from .views import *


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name="list"),
    path('<int:pk>/', PostDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name="update"),
    path('create/', PostCreateView.as_view(), name='create')
]

