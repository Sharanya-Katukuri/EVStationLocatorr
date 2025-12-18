from django.db import models

class ChargingStation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Charger(models.Model):
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE, related_name="chargers")
    charger_type = models.CharField(max_length=50)  # AC, DC, Fast Charger
    power = models.CharField(max_length=50)        # e.g., 22kW, 50kW
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    total_slots = models.IntegerField()

    def __str__(self):
        return f"{self.charger_type} - {self.station.name}"
