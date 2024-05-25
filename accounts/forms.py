from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, label="Имя")
    middle_name = forms.CharField(max_length=50, label="Отчество")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    phone_number = forms.CharField(max_length=20, label="Номер телефона")
    address = forms.CharField(max_length=255, label="Адрес")

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "address",
            "phone_number",
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
            "phone_number",
        )


class UserUpdateForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "address",
            "phone_number",
        )
        labels = {
            "balance": "Баланс",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "last_name": "Фамилия",
            "email": "Адрес электронной почты",
            "address": "Адрес проживания",
            "phone_number": "Номер телефона",
        }
