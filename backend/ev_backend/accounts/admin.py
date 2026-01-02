from django.contrib import admin

# Register your models here.
# ev_booking/admin.py
from django.contrib import admin
from .models import ChargingStation

@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'connector', 'speed', 'is_available', 'open_now']
    list_editable = ['is_available']  # You can toggle directly in list
