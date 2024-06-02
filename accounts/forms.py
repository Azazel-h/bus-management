from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import CustomUser
from accounts.validators import validate_russian_alphabet


class CustomUserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, label="Имя", validators=[validate_russian_alphabet]
    )
    middle_name = forms.CharField(
        max_length=50,
        label="Отчество",
        required=False,
        validators=[validate_russian_alphabet],
    )
    last_name = forms.CharField(
        max_length=50, label="Фамилия", validators=[validate_russian_alphabet]
    )
    phone_number = PhoneNumberField(region="RU")

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "phone_number",
        )
        labels = {
            "phone_number": "Номер телефона",
        }


class CustomUserAdminEditForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=50, label="Имя", validators=[validate_russian_alphabet]
    )
    middle_name = forms.CharField(
        max_length=50,
        label="Отчество",
        required=False,
        validators=[validate_russian_alphabet],
    )
    last_name = forms.CharField(
        max_length=50, label="Фамилия", validators=[validate_russian_alphabet]
    )
    phone_number = PhoneNumberField(region="RU")

    class Meta:
        model = CustomUser
        fields = (
            "last_name",
            "username",
            "first_name",
            "middle_name",
            "email",
            "phone_number",
        )
        labels = {
            "phone_number": "Номер телефона",
        }
