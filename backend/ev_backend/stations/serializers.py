from rest_framework import serializers
from .models import ChargingStation, Charger


class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = "__all__"


class ChargingStationSerializer(serializers.ModelSerializer):
    chargers = ChargerSerializer(many=True, read_only=True)

    class Meta:
        model = ChargingStation
        fields = "__all__"
