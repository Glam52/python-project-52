from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


