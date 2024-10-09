from django import forms
from .models import Task
from statuses.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
