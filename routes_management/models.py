from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Route(models.Model):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"

    PART_OF_DAY_CHOICES = [
        (MORNING, "Утро"),
        (AFTERNOON, "День"),
        (EVENING, "Вечер"),
    ]

    date = models.DateField(blank=True, null=True)
    part_of_day = models.CharField(
        max_length=10,
        choices=PART_OF_DAY_CHOICES,
        default=MORNING,
    )
    duration = models.TimeField()
    distance = models.FloatField()
    passengers_count = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    driver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("route-detail", kwargs={"pk": self.pk})

    def distance_kilometers(self):
        return round(self.distance / 1000, 2)

    def update(self, commit=False, **kwargs) -> None:
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        if commit:
            self.save()
