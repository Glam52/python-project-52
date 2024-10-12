from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from django.views import View
from .forms import StatusForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from tasks.models import Task


class StatusListView(View):
    @method_decorator(login_required)
    def get(self, request):
        statuses = Status.objects.all()
        return render(request, "statuses/status_list.html",
                      {"statuses": statuses}
                      )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.")
            return redirect("login")  # Замените 'login' на имя вашего URL для входа
        return super().dispatch(request, *args, **kwargs)


class StatusCreateView(View):
    def get(self, request):
        form = StatusForm()
        return render(request, "statuses/status_form.html", {"form": form})

    def post(self, request):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно создан")
            return redirect("statuses:list")
        return render(request, "statuses/status_form.html", {"form": form})


class StatusUpdateView(View):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = StatusForm(instance=status)
        return render(request, "statuses/status_update.html", {"form": form})

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно изменен")
            return redirect("statuses:list")
        return render(request, "statuses/status_update.html", {"form": form})


class StatusDeleteView(View):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        return render(
            request, "statuses/status_confirm_delete.html", {"status": status}
        )

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)

        # Проверяем, используется ли статус в задачах
        if Task.objects.filter(status=status).exists():
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется в задачах.",
            )
            return redirect(
                "statuses:list"
            )  # Замените 'statuses:list' на ваше имя URL для списка статусов

        status.delete()
        messages.success(request, "Статус успешно удален")
        return redirect("statuses:list")
