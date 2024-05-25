from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, label="Имя")
    middle_name = forms.CharField(max_length=50, label="Отчество")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    phone_number =
    address = forms.CharField(max_length=255, blank=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "address",
        )


class CustomUserAdminEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "address",
        )


class UserUpdateForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "balance",
            "address",
        )
        labels = {
            "balance": "Баланс",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "last_name": "Фамилия",
            "email": "Адрес электронной почты",
            "address": "Адрес проживания",
        }
