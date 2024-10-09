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

    # Фильтрация по статусу
    status_id = request.GET.get('status')
    if status_id:
        tasks = tasks.filter(status_id=status_id)

    # Фильтрация по исполнителю
    executor_id = request.GET.get('executor')
    if executor_id:
        tasks = tasks.filter(executor_id=executor_id)

    # Фильтрация только по собственным задачам
    if request.GET.get('self_tasks'):
        tasks = tasks.filter(author=request.user)

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
    task = get_object_or_404(Task, pk=pk)  # Получаем задачу по первичному ключу
    statuses = Status.objects.all()  # Получаем все статусы
    executors = User.objects.all()  # Получаем всех пользователей

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # Заполняем форму данными существующей задачи
        if form.is_valid():
            form.save()  # Сохраняем изменения
            messages.success(request, 'Задача успешно изменена')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)  # Заполняем форму существующей задачей при GET-запросе

    return render(request, 'tasks/task_update.html', {
        'form': form,
        'statuses': statuses,
        'executors': executors,
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
