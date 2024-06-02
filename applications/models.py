from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from routes_management.models import Route
from stations.models import Station


class Application(models.Model):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"

    PART_OF_DAY_CHOICES = [
        (MORNING, "Утро"),
        (AFTERNOON, "День"),
        (EVENING, "Вечер"),
    ]

    passenger = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    departure = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="departure"
    )
    arrival = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="arrival"
    )
    date = models.DateField()
    part_of_day = models.CharField(
        max_length=10,
        choices=PART_OF_DAY_CHOICES,
        default=MORNING,
    )
