from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('/login/')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно обновлен.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удалён.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль.')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('login')  # Перенаправление на страницу входа

