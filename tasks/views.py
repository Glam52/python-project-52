from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task
from users.models import User
from statuses.models import Status
from labels.models import Label
from .forms import TaskForm


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        status_id = self.request.GET.get('status')
        executor_id = self.request.GET.get('executor')
        label_id = self.request.GET.get('label')

        if status_id:
            context['tasks'] = context['tasks'].filter(status_id=status_id)
        if executor_id:
            context['tasks'] = context['tasks'].filter(executor_id=executor_id)
        if label_id:  # Фильтрация по меткам
            context['tasks'] = context['tasks'].filter(labels__id=label_id)
        if self.request.GET.get('self_tasks'):
            context['tasks'] = context['tasks'].filter(author=self.request.user)

        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.author:
            messages.error(self.request, "Задачу может удалить только ее автор.")
            # Redirect to the task list
            self.success_url = reverse_lazy('task_list')
        return obj


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.object.labels.all()
        return context
