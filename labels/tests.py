from django.test import TestCase
from django.urls import reverse
from .models import Label
from django.contrib.messages import get_messages
from tasks.models import Task
from statuses.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser",
                                            password="12345"
                                            )
        cls.status = Status.objects.create(
            name="Test Status"
        )  # Добавляем создание статуса
        cls.label = Label.objects.create(name="Test Label")

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_label_list_view(self):
        response = self.client.get(reverse("labels:label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Label")
        self.assertIn(self.label, response.context["labels"])

    def test_label_create_view(self):
        response = self.client.post(
            reverse("labels:label_create"),
            {
                "name": "New Test Label",
            },
        )
        self.assertEqual(Label.objects.count(), 2)  # Ожидаем, что новая метка создана
        self.assertRedirects(response, reverse("labels:label_list"))

        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно создана")

    def test_label_update_view(self):
        response = self.client.post(
            reverse("labels:label_update", args=[self.label.pk]),
            {
                "name": "Updated Test Label",
            },
        )
        self.label.refresh_from_db()
        self.assertEqual(
            self.label.name, "Updated Test Label"
        )  # Проверка обновленного названия
        self.assertRedirects(response, reverse("labels:label_list"))

        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно изменена")

    def test_label_delete_view(self):
        response = self.client.post(
            reverse("labels:label_delete", args=[self.label.pk])
        )
        self.assertEqual(
            Label.objects.count(), 0
        )  # Проверка, что метка успешно удалена
        self.assertRedirects(response, reverse("labels:label_list"))

        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно удалена")

    def test_label_delete_with_tasks(self):
        task = Task.objects.create(
            name="Test Task", status=self.status, author=self.user
        )  # Указываем статус
        task.labels.add(self.label)

        response = self.client.post(
            reverse("labels:label_delete", args=[self.label.pk])
        )
        self.assertEqual(Label.objects.count(), 1)  # Проверка, что метка не удалена
        self.assertRedirects(response, reverse("labels:label_list"))

        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Невозможно удалить метку, потому что она используется"
        )
