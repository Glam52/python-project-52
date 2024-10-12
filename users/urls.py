from django.urls import path
from .views import (
    user_list,
    user_create,
    user_update,
    user_delete,
    login_view,
    logout_view,
)


urlpatterns = [
    path("", user_list, name="user_list"),
    path("create/", user_create, name="user_create"),
    path("<int:pk>/update/", user_update, name="user_update"),
    path("<int:pk>/delete/", user_delete, name="user_delete"),
    path("login/", login_view, name="login"),  # Добавлен маршрут для login
    path("logout/", logout_view, name="logout"),  # Добавлен маршрут для logout
]
