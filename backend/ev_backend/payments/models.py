from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    PAYMENT_METHODS = (
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("CASH", "Cash"),
    )

    PAYMENT_STATUS = (
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.id} - {self.status}"
