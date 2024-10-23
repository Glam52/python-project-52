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


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно создан"


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен"


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удален"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка, используется ли статус в задачах
        if Task.objects.filter(status=self.object).exists():
            messages.error(request, "Невозможно удалить статус, потому что он используется в задачах.")
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)
