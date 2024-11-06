from django.urls import path
from .views import UserCreateView, UserListView


urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),  # for creating users via POST
    path('users/list/', UserListView.as_view(), name='user-list'),  # for listing users via GET
    
]
