from django.db import models
from django.conf import settings
from statuses.models import Status
from django.db.models import (
    CharField,
    DateTimeField,
    TextField,
    ManyToManyField,
    ForeignKey,
)


class Task(models.Model):
    name: CharField = models.CharField(max_length=255)
    description: TextField = models.TextField(blank=True)
    status: ForeignKey = models.ForeignKey(Status, on_delete=models.CASCADE)
    author: ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    executor: ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks",
    )
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    labels: ManyToManyField = models.ManyToManyField("labels.Label")

    def __str__(self):
        return self.name
