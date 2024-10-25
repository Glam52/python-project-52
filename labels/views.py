from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from .forms import LabelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from typing import Any


class LabelListView(ListView):
    model = Label
    template_name: str = "labels/label_list.html"
    context_object_name: str = "labels"


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name: str = "labels/label_form.html"
    success_url: str = reverse_lazy("labels:label_list")
    success_message: str = "Метка успешно создана"


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name: str = "labels/label_update.html"
    success_url: str = reverse_lazy("labels:label_list")
    success_message: str = "Метка успешно изменена"


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name: str = "labels/label_confirm_delete.html"
    success_url: str = reverse_lazy("labels:label_list")
    success_message: str = "Метка успешно удалена"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object: Any = self.get_object()

        if self.object.task_set.exists():
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)
