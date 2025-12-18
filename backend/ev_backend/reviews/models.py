from django.db import models
from django.contrib.auth.models import User
from stations.models import ChargingStation

class Review(models.Model):
    RATING_CHOICES = (
        (1, "Very Bad"),
        (2, "Bad"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station.name} - {self.rating}"
