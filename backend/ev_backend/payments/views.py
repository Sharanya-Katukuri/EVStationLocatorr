import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from bookings.models import Booking


# -----------------------------------
# MAKE PAYMENT (DEMO)
# -----------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def make_payment(request):
    data = request.data

    booking_id = data.get("booking")
    method = data.get("method")

    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    if hasattr(booking, "payment"):
        return Response({"error": "Payment already done"}, status=400)

    payment = Payment.objects.create(
        booking=booking,
        method=method,
        status="SUCCESS",
        transaction_id=str(uuid.uuid4())
    )

    booking.status = "CONFIRMED"
    booking.save()

    serializer = PaymentSerializer(payment)
    return Response(serializer.data, status=201)


# -----------------------------------
# VIEW PAYMENT DETAILS
# -----------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_detail(request, booking_id):
    try:
        payment = Payment.objects.get(booking__id=booking_id, booking__user=request.user)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    serializer = PaymentSerializer(payment)
    return Response(serializer.data)
