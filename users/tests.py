from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.


class UserTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePassword123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data["password"])  # Устанавливаем пароль
        self.user.save()  # Сохраняем изменения в базе данных

    def test_user_create(self):
        def test_user_create(self):
            response = self.client.post(reverse("user_create"), self.user_data)

            # Если валидация не прошла, выводим ошибки формы
            if response.status_code != 302:
                print(response.
                      context["form"].errors)  # Вывод ошибок формы для отладки

            self.assertEqual(response.status_code,
                             302
                             )  # Проверка на перенаправление
            self.assertTrue(
                User.objects.filter(username="testuser").exists()
            )  # Проверка, что пользователь создан

    def test_user_update(self):
        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
            "password1": "NewPassword123",
            "password_confirm": "NewPassword123",
        }
        response = self.client.post(
            reverse("user_update", args=[self.user.pk]), updated_data
        )
        self.assertEqual(response.status_code,
                         302
                         )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_user_delete(self):
        response = self.client.post(reverse("user_delete",
                                            args=[self.user.pk])
                                    )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful deletion
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
