from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task
from users.models import User
from statuses.models import Status
from labels.models import Label
from .forms import TaskForm
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from typing import Any, Dict


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        status_id = self.request.GET.get("status")
        executor_id = self.request.GET.get("executor")
        label_id = self.request.GET.get("label")

        if status_id:
            context["tasks"] = context["tasks"].filter(status_id=status_id)
        if executor_id:
            context["tasks"] = context["tasks"].filter(executor_id=executor_id)
        if label_id:  # Фильтрация по меткам
            context["tasks"] = context["tasks"].filter(labels__id=label_id)
        if self.request.GET.get("self_tasks"):
            context["tasks"] = context["tasks"].filter(author=self.request.user)

        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context

    def form_valid(self, form: TaskForm) -> HttpResponse:
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context

    def form_valid(self, form: TaskForm) -> HttpResponse:
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()

        if self.request.user != self.object.author:
            messages.error(self.request, "Задачу может удалить только ее автор.")
            return redirect("task_list")  # Перенаправление на список задач

        # Если автор совпадает, удаляем задачу
        self.object.delete()
        messages.success(self.request, "Задача успешно удалена")
        return redirect(self.success_url)  # Перенаправление на список задач

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()

        # Проверка авторства
        if self.request.user != self.object.author:
            messages.error(self.request,
                           "Задачу может удалить только ее автор."
                           )
            return redirect("task_list")  # Перенаправление на список задач

        return super().get(
            request, *args, **kwargs
        )  # Позволяем отобразить страницу подтверждения удаления

    def get_object(self, queryset: Any = None) -> Task:
        return super().get_object(queryset)


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["labels"] = self.object.labels.all()
        return context
