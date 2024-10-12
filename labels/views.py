from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from .forms import LabelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class LabelListView(ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"  # Добавлено для улучшения читаемости шаблона


class LabelCreateView(CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("labels:label_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_update.html"
    success_url = reverse_lazy("labels:label_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)


class LabelDeleteView(DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("labels:label_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка на наличие связанных задач
        if (
            self.object.task_set.exists()
        ):  # task_set используется для обратной связи через ManyToMany
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)

        # Удаляем метку, если она не используется
        messages.success(request, "Метка успешно удалена")
        return self.delete(request, *args, **kwargs)
