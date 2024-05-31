from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Route(models.Model):
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    duration = models.TimeField()
    passengers_count = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    driver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("route-detail", kwargs={"pk": self.pk})
