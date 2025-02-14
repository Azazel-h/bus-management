from django.db import models

from routes_management.models import Route


class Station(models.Model):
    name = models.CharField(max_length=100)
    route = models.ManyToManyField(Route, blank=True, through="StationOrder")
    longitude = models.DecimalField(decimal_places=10, max_digits=20)
    latitude = models.DecimalField(decimal_places=10, max_digits=20)

    def __str__(self):
        return self.name


class StationOrder(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.IntegerField()
    passed = models.BooleanField(default=False)
    passengers_taken = models.IntegerField(default=0)
    passed_time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = [
            "order",
        ]

    def update(self, commit=False, **kwargs) -> None:
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        if commit:
            self.save()
