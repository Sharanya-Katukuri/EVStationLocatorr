from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer
from stations.models import ChargingStation


# -----------------------------------
# ADD REVIEW
# -----------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    data = request.data
    station_id = data.get("station")

    try:
        station = ChargingStation.objects.get(id=station_id)
    except ChargingStation.DoesNotExist:
        return Response({"error": "Station not found"}, status=404)

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user, station=station)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# -----------------------------------
# GET REVIEWS FOR A STATION
# -----------------------------------
@api_view(["GET"])
def station_reviews(request, station_id):
    reviews = Review.objects.filter(station_id=station_id).order_by("-created_at")
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
