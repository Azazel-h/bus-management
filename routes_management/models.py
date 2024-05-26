from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=10, max_digits=20)
    latitude = models.DecimalField(decimal_places=10, max_digits=20)


class Route(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    date = models.DateTimeField()
    arrival_time = models.DateTimeField()
    passengers_count = models.IntegerField()
