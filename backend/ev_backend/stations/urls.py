from django.urls import path
from .views import (
    get_stations,
    get_station_detail,
    add_station,
    add_charger,
    get_station_chargers
)

urlpatterns = [
    path("", get_stations),
    path("<int:station_id>/", get_station_detail),
    path("add/", add_station),
    path("charger/add/", add_charger),
    path("<int:station_id>/chargers/", get_station_chargers),
]
