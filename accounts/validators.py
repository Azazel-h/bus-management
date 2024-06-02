import re
from django.core.exceptions import ValidationError


def validate_russian_alphabet(value):
    if not re.match(r"^[А-Яа-яЁё]+$", value):
        raise ValidationError(
            "Это поле может содержать только буквы русского алфавита."
        )
