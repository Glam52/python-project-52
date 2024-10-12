from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status
from tasks.models import Task

User = get_user_model()


class StatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.status = Status.objects.create(name="Test Status")

    def test_status_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Status")

    def test_status_create_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("statuses:create"), {"name": "New Status"})
        self.assertEqual(Status.objects.count(), 2)
        self.assertRedirects(response, reverse("statuses:list"))

    def test_status_update_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("statuses:update", args=[self.status.pk]),
            {"name": "Updated Status"},
        )
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")
        self.assertRedirects(response, reverse("statuses:list"))

    def test_status_delete_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("statuses:delete", args=[self.status.pk]))
        self.assertEqual(Status.objects.count(), 0)
        self.assertRedirects(response, reverse("statuses:list"))

    def test_status_delete_with_tasks(self):
        # Создаем задачу с указанным автором и статусом
        Task.objects.create(name="Test Task", status=self.status, author=self.user)

        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("statuses:delete", args=[self.status.pk]))

        # Проверяем, что произошла переадресация
        self.assertRedirects(response, reverse("statuses:list"))
        # Проверяем, что статус не был удален
        self.assertEqual(Status.objects.count(), 1)
