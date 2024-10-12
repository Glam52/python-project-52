from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput, max_length=128, required=True
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, max_length=128, required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password_confirm = cleaned_data.get("password_confirm")

        # Если хотя бы одно из полей заполнено
        if password1 != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data
