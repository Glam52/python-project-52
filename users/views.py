from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Установить пароль
            user.save()  # Сохраняем пользователя в БД
            messages.success(request, 'Пользователь успешно создан')
            return redirect('/login/')
    else:
        form = UserForm()

    return render(request, 'users/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Проверка, является ли текущий пользователь владельцем аккаунта
    if request.user != user:
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        return redirect('user_list')

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # Проверка на изменение пароля
            password1 = form.cleaned_data.get('password1')
            password_confirm = form.cleaned_data.get('password_confirm')
            if password1 and password1 == password_confirm:
                user.set_password(password1)  # Устанавливаем новый пароль
            user.save()
            messages.success(request, 'Пользователь успешно обновлен')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'users/user_update_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    # Проверка, является ли текущий пользователь владельцем аккаунта
    if request.user != user:
        messages.error(request, 'У вас нет прав для удаления другого пользователя.')
        return redirect('user_list')

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удалён')
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
            messages.success(request, 'Вы залогинены')
            return redirect('index')  # Убедитесь, что это имя соответствует маршруту
        else:
            messages.error(request, 'Пожалуйста, введите правильные имя пользователя и пароль')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы разлогинены')
    return redirect('index')  # Перенаправление на страницу входа
