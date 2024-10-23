from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpRequest, HttpResponseBase
from typing import Any
from django.contrib.auth.views import LoginView, LogoutView

User = get_user_model()


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/user_form.html"
    success_message = "Пользователь успешно зарегистрирован"
    success_url = reverse_lazy("login")

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        return super().form_valid(form)

    def form_invalid(self, form: CustomUserCreationForm) -> HttpResponse:
        # Для отладки ошибок (print(form.errors))
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/user_update_form.html"
    success_message = "Пользователь успешно изменен"
    success_url = reverse_lazy("user_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        user_to_delete = self.get_object()
        if user_to_delete != request.user:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )
            return redirect("user_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        user = form.save(commit=False)
        password1 = form.cleaned_data.get("password1")
        password_confirm = form.cleaned_data.get("password2")

        if password1 and password1 == password_confirm:
            user.set_password(password1)

        user.first_name = form.cleaned_data.get("first_name")  # Обновление имени
        user.last_name = form.cleaned_data.get("last_name")  # Обновление фамилии
        user.save()

        return super().form_valid(form)

    def form_invalid(self, form: CustomUserCreationForm) -> HttpResponse:
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_message = "Пользователь успешно удален"
    success_url = reverse_lazy("user_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        user_to_delete = self.get_object()
        if user_to_delete != request.user:
            messages.error(
                request, "У вас нет прав для изменения другого пользователя."
            )
            return redirect("user_list")
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserLogin(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, введите правильные имя пользователя и пароль")
        return super().form_invalid(form)


class UserLogout(LogoutView):
    next_page = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().post(request, *args, **kwargs)
