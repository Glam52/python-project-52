from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from users.models import User
from statuses.models import Status
from .forms import TaskForm
from django.contrib import messages

@login_required
def task_list(request):
    statuses = Status.objects.all()
    executors = User.objects.all()
    tasks = Task.objects.all()  # Получение всех задач
    return render(request, 'tasks/task_list.html', {
        'statuses': statuses,
        'executors': executors,
        'tasks': tasks,  # Передача задач в контекст
    })


@login_required
def task_create(request):
    statuses = Status.objects.all()
    executors = User.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, 'Задача успешно создана')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'statuses': statuses,  # Убедитесь, что это передается
        'executors': executors,  # И это тоже
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    statuses = Status.objects.all()  # Получение всех статусов
    executors = User.objects.all()  # Получение всех исполнителей

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно изменена')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_update.html', {
        'form': form,
        'statuses': statuses,  # Передача статусов в контекст
        'executors': executors,  # Передача исполнителей в контекст
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.author:
        messages.error(request, "Задачу может удалить только ее автор.")
        return redirect('task_list')  # Перенаправляем на страницу списка задач

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Задача была успешно удалена.")
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})
