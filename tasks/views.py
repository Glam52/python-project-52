from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView
from .filters import TaskFilter
from .models import Task
from users.models import User
from statuses.models import Status
from labels.models import Label
from .forms import TaskForm
from django.shortcuts import redirect
from django.http import HttpRequest
from typing import Any, Dict


class TaskListView(FilterView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = "Задача успешно создана"
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_message = "Задача успешно изменена"
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["labels"] = self.object.labels.all()
        return context


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")
    success_message = "Задача успешно удалена"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            messages.error(request, "Задачу может удалить только ее автор")
            return redirect("task_list")  # Перенаправление на список задач
        return super().dispatch(request, *args, **kwargs)
