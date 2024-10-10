from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from .forms import LabelForm
from django.urls import reverse_lazy
from django.contrib import messages


class LabelListView(ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'  # Добавлено для улучшения читаемости шаблона

class LabelCreateView(CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана')
        return super().form_valid(form)

class LabelUpdateView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)

class LabelDeleteView(DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels:label_list')

    def post(self, request, *args, **kwargs):
        # Сначала, возможно, сохраните метку
        self.object = self.get_object()
        messages.success(request, 'Метка успешно удалена')
        return self.delete(request, *args, **kwargs)
