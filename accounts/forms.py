from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Имя")
    middle_name = forms.CharField(max_length=50, label="Отчество", required=False)
    last_name = forms.CharField(max_length=50, label="Фамилия")
    phone_number = forms.CharField(max_length=20, label="Номер телефона")
    address = forms.CharField(max_length=255, label="Адрес")

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "address",
            "phone_number",
            "address",
        )


class CustomUserAdminEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            "last_name",
            "username",
            "first_name",
            "middle_name",
            "email",
            "address",
            "phone_number",
        )


class UserUpdateForm(ModelForm):
    first_name = forms.CharField(max_length=50, label="Имя")
    middle_name = forms.CharField(max_length=50, label="Отчество")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    phone_number = forms.CharField(max_length=20, label="Номер телефона")
    address = forms.CharField(max_length=255, label="Адрес")

    class Meta:
        model = CustomUser
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "address",
            "phone_number",
        )
