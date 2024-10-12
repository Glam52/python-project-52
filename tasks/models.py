from django.db import models
from django.conf import settings
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField("labels.Label")

    def __str__(self):
        return self.name
