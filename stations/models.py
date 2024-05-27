from django.db import models

from routes_management.models import Route


class Station(models.Model):
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=10, max_digits=20)
    latitude = models.DecimalField(decimal_places=10, max_digits=20)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
