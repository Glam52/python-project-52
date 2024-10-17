from django_filters import FilterSet, ModelChoiceFilter
from .models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), field_name="status")
    executor = ModelChoiceFilter(queryset=User.objects.all(), field_name="executor")
    label = ModelChoiceFilter(queryset=Label.objects.all(), field_name="labels")

    class Meta:
        model = Task
        fields = []
