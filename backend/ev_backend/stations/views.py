from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ChargingStation, Charger
from .serializers import ChargingStationSerializer, ChargerSerializer


# -------------------------
# GET ALL STATIONS
# -------------------------
@api_view(["GET"])
def get_stations(request):
    stations = ChargingStation.objects.filter(is_active=True)
    serializer = ChargingStationSerializer(stations, many=True)
    return Response(serializer.data)


# -------------------------
# GET STATION DETAILS
# -------------------------
@api_view(["GET"])
def get_station_detail(request, station_id):
    try:
        station = ChargingStation.objects.get(id=station_id)
    except ChargingStation.DoesNotExist:
        return Response({"error": "Station not found"}, status=404)

    serializer = ChargingStationSerializer(station)
    return Response(serializer.data)


# -------------------------
# ADMIN: ADD NEW STATION
# (For now no admin role check — optional)
# -------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_station(request):
    serializer = ChargingStationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Station added successfully"})
    
    return Response(serializer.errors, status=400)


# -------------------------
# ADMIN: ADD NEW CHARGER
# -------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_charger(request):
    serializer = ChargerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Charger added successfully"})
    
    return Response(serializer.errors, status=400)


# -------------------------
# GET ALL CHARGERS FOR A STATION
# -------------------------
@api_view(["GET"])
def get_station_chargers(request, station_id):
    chargers = Charger.objects.filter(station_id=station_id)
    serializer = ChargerSerializer(chargers, many=True)
    return Response(serializer.data)
