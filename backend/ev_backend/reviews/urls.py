from django.urls import path
from .views import add_review, station_reviews

urlpatterns = [
    path("add/", add_review),
    path("station/<int:station_id>/", station_reviews),
]
