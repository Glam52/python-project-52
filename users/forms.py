from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput, max_length=128, required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, max_length=128, required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")  # Исправлено здесь

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data
