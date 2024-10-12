from django import forms
from .models import Task
from statuses.models import Status
from labels.models import Label  # Импортируйте модель Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels",
        ]  # Добавьте 'labels' в список полей

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["status"].queryset = Status.objects.all()
        self.fields["executor"].queryset = User.objects.all()
        self.fields[
            "labels"
        ].queryset = Label.objects.all()  # Установите queryset для меток
        self.fields[
            "labels"
        ].required = False  # Сделайте поле меток необязательным (если нужно)
