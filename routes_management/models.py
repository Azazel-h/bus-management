from django.db import models


class Route(models.Model):
    date = models.DateTimeField()
    arrival_time = models.DateTimeField()
    passengers_count = models.IntegerField()


class Station(models.Model):
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=10, max_digits=20)
    latitude = models.DecimalField(decimal_places=10, max_digits=20)
