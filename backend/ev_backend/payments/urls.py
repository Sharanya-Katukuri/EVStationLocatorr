from django.urls import path
from .views import make_payment, payment_detail

urlpatterns = [
    path("pay/", make_payment),
    path("detail/<int:booking_id>/", payment_detail),
]
