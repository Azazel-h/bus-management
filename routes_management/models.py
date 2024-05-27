from django.contrib.auth import get_user_model
from django.db import models


class Route(models.Model):
    date = models.DateTimeField()
    arrival_time = models.DateTimeField()
    passengers_count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    driver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
