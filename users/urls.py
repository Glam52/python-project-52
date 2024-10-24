from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserLogin,
    UserLogout,
)

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
