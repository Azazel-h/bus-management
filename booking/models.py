from django.contrib.auth import get_user_model
from django.db import models

from routes_management.models import Route, Station


class Application(models.Model):
    passenger = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    creation_date = models.DateField()
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_station = models.ForeignKey(Station, on_delete=models.CASCADE)
