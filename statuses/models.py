from django.db import models
from django.db.models import CharField, DateTimeField


class Status(models.Model):
    name: CharField = models.CharField(max_length=255)
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
