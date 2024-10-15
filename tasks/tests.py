from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Task
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class TaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.status = Status.objects.create(name="Test Status")
        cls.label = Label.objects.create(name="Test Label")
        cls.task = Task.objects.create(
            name="Test Task",
            status=cls.status,
            author=cls.user,
        )
        cls.task.labels.add(cls.label)

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertIn(self.task, response.context["tasks"])

    def test_task_create_view(self):
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "New Task",
                "status": self.status.id,  # Убедитесь, что статус указан
                "executor": self.user.id,
                "labels": [self.label.id],  # Передаем метку
            },
        )

        if response.status_code != 302:  # Проверяем, произошла ли переадресация
            print(response.content)  # Отладочный вывод
            if "form" in response.context:
                print(response.context["form"].errors)  # Выводим ошибки формы

        self.assertEqual(Task.objects.count(), 2)  # Ожидается создание новой задачи
        self.assertRedirects(response, reverse("task_list"))

    def test_task_update_view(self):
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "name": "Updated Task",
                "status": self.status.id,
                "executor": self.user.id,  # Необязательно
                "labels": [self.label.id],
            },
        )
        print(response.content)  # Отладочный вывод
        self.task.refresh_from_db()  # Обновляем данные задачи
        self.assertEqual(self.task.name, "Updated Task")  # Проверка обновления названия
        self.assertRedirects(response, reverse("task_list"))

    def test_task_delete_view(self):
        response = self.client.post(reverse("task_delete", args=[self.task.pk]))
        self.assertEqual(Task.objects.count(), 0)  # Проверка удаления задачи
        self.assertRedirects(response, reverse("task_list"))

    def test_task_delete_unauthorized(self):
        self.client.logout()
        self.client.login(username="unauthorized", password="12345")

        response = self.client.post(reverse("task_delete", args=[self.task.pk]))
        self.assertEqual(
            Task.objects.count(), 1
        )  # Проверка, что задача не была удалена
        self.assertRedirects(response, reverse("task_list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задачу может удалить только ее автор.")
