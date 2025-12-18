from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from decimal import Decimal

from .models import Booking
from .serializers import BookingSerializer
from stations.models import ChargingStation, Charger


# ---------------------------------------
# CHECK SLOT AVAILABILITY
# ---------------------------------------
def is_slot_available(charger, date, start_time, end_time):
    overlapping_bookings = Booking.objects.filter(
        charger=charger,
        date=date,
        status="CONFIRMED",
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    return not overlapping_bookings.exists()


# ---------------------------------------
# CREATE BOOKING (DYNAMIC TIME)
# ---------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    data = request.data

    station_id = data.get("station")
    charger_id = data.get("charger")
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # Convert time
    start_time_obj = datetime.strptime(start_time, "%H:%M").time()
    end_time_obj = datetime.strptime(end_time, "%H:%M").time()

    if start_time_obj >= end_time_obj:
        return Response({"error": "End time must be after start time"}, status=400)

    try:
        station = ChargingStation.objects.get(id=station_id)
        charger = Charger.objects.get(id=charger_id)
    except:
        return Response({"error": "Invalid station or charger"}, status=400)

    # Check availability
    if not is_slot_available(charger, date, start_time_obj, end_time_obj):
        return Response({"error": "Selected time slot not available"}, status=409)

    # Calculate hours
    duration_hours = (
        datetime.combine(datetime.today(), end_time_obj) -
        datetime.combine(datetime.today(), start_time_obj)
    ).seconds / 3600

    total_cost = Decimal(duration_hours) * charger.price_per_hour

    booking = Booking.objects.create(
        user=request.user,
        station=station,
        charger=charger,
        date=date,
        start_time=start_time_obj,
        end_time=end_time_obj,
        total_cost=total_cost,
        status="CONFIRMED"
    )

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=201)


# ---------------------------------------
# USER BOOKING HISTORY
# ---------------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


# ---------------------------------------
# CANCEL BOOKING
# ---------------------------------------
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    booking.status = "CANCELLED"
    booking.save()

    return Response({"message": "Booking cancelled successfully"})
