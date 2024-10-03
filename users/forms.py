from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)  # Поле для ввода пароля с хешированием

    class Meta:
        model = User
        fields = ['username', 'full_name', 'password']
