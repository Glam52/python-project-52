from django.test import TestCase
from django.urls import reverse
from .models import User


class UserTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }
        self.user = User(
            username=self.user_data["username"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )
        self.user.set_password(self.user_data["password1"])  # Устанавливаем пароль
        self.user.save()

    def test_user_create(self):
        # Проверяем создание нового пользователя
        response = self.client.post(reverse("user_create"), self.user_data)

        # Ожидаем, что произойдет перенаправление после успешного создания
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.assertTrue(User.objects.filter(username="testuser").exists())

        # Проверяем, что перенаправление ведет на логин
        self.assertRedirects(response, reverse("login"))

        # Проверяем на случай с неверными данными (некорректный ввод)
        invalid_data = {**self.user_data, "password2": "DifferentPassword123"}
        response_invalid = self.client.post(reverse("user_create"), invalid_data)

        # Ожидаем, что будет статус 200, если форма не валидна
        self.assertEqual(response_invalid.status_code, 200)  # Ожидаем 200, если данные неверные

    def test_user_update(self):
        self.client.force_login(self.user)  # Аутентификация пользователя
        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
            "password1": "NewPassword123",
            "password2": "NewPassword123",
        }

        # Проверяем на успешное обновление
        response = self.client.post(reverse("user_update", args=[self.user.pk]), updated_data)

        # Ожидаем перенаправление после успешного обновления
        self.assertEqual(response.status_code, 302)  # Ожидаем 302 после успешного обновления

        # Проверяем, что пользователь обновлён
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

        # Проверяем, что перенаправление ведет на список пользователей
        self.assertRedirects(response, reverse("user_list"))

        # Дополнительно проверяем на 200 для невалидных данных
        invalid_data = {
            "first_name": "",  # Неправильные данные
            "last_name": "User",
            "password1": "NewPassword123",
            "password2": "DifferentPassword123",
        }
        response_invalid = self.client.post(reverse("user_update",
                                                    args=[self.user.pk]), invalid_data)

        # Ожидаем 200, если данные неверные
        self.assertEqual(response_invalid.status_code, 200)

    def test_user_delete(self):
        self.client.force_login(self.user)  # Аутентификация пользователя
        response = self.client.post(reverse("user_delete", args=[self.user.pk]))

        # Ожидаем перенаправление после успешного удаления
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

        # Проверяем, что перенаправление ведет на user_list
        self.assertRedirects(response, reverse("user_list"))
