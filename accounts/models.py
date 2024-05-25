import uuid

from django.contrib.auth.models import (
    AbstractUser,
    Group,
    PermissionsMixin,
)
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.username

    def update(self, commit=False, **kwargs) -> None:
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        if commit:
            self.save()
