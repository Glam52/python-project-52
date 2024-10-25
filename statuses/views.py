from django.shortcuts import redirect
from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest
from typing import Any


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name: str = "statuses/status_list.html"
    context_object_name: str = "statuses"


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name: str = "statuses/status_form.html"
    success_url: str = reverse_lazy("statuses:list")
    success_message: str = "Статус успешно создан"


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name: str = "statuses/status_update.html"
    success_url: str = reverse_lazy("statuses:list")
    success_message: str = "Статус успешно изменен"


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name: str = "statuses/status_confirm_delete.html"
    success_url: str = reverse_lazy("statuses:list")
    success_message: str = "Статус успешно удален"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object: Any = self.get_object()

        if Task.objects.filter(status=self.object).exists():
            messages.error(request,
                           "Невозможно удалить статус, потому что он используется в задачах.")
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)
