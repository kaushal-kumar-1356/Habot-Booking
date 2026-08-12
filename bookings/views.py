from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Booking_Request, LSA_Profile, Payment
from .serializers import BookingRequestSerializer, LSASerializer, PaymentSerializer

# Create your views here.

@api_view(['POST'])
def create_booking(request):
    serializer = BookingRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    lsa = serializer.validated_data['lsa']
    start_time = serializer.validated_data['start_time']
    end_time = serializer.validated_data['end_time']

    if start_time >= end_time:
        return Response(
            {'error' : 'End time must be after start time.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    overlapping_booking = Booking_Request.objects.filter(
        lsa = lsa,
        start_time__lt = end_time,
        end_time__gt = start_time
    ).exists()

    if overlapping_booking:
        return Response(
            {'error' : 'LSA is already booked for this time.'},
            status=status.HTTP_409_CONFLICT
        )
    booking = serializer.save()

    return Response(
        BookingRequestSerializer(booking).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def booking_list(request):

    bookings = Booking_Request.objects.select_related("parent", "lsa")

    serializer = BookingRequestSerializer(bookings, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def booking_detail(request, booking_id):

    try:
        booking = Booking_Request.objects.select_related('parent', 'lsa').get(id=booking_id)
    except Booking_Request.DoesNotExist:
        return Response(
            {'error' : 'Booking not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookingRequestSerializer(booking)
    return Response(serializer.data)











@api_view(['GET'])
def search_lsa(request):

    skill = request.query_params.get('skill')

    lsas = LSA_Profile.objects.all()

    if skill:
        lsas = lsas.filter(skills__icontains=skill)

    serializer = LSASerializer(lsas, many=True)

    return Response(serializer.data)
    

@api_view(['POST'])
def create_payment(request):

    serializer = PaymentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    payment = serializer.save(
        status='SUCCESS',
        transaction_id=f"TXN-{serializer.validated_data['booking'].id}"

    )

    return Response(
        PaymentSerializer(payment).data,
        status=status.HTTP_201_CREATED
    )



@api_view(['POST'])
def payment_webhook(request):

    booking_id = request.data.get("booking_id")
    payment_status = request.data.get("status")

    if not booking_id:
        return Response(
            {'error' : 'booking id is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        booking = Booking_Request.objects.get(id=booking_id)

    except Booking_Request.DoesNotExist:
        return Response(
            {'error' : 'Booking not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if payment_status == 'SUCCESS':
        booking.status = 'CONFIRMED'
        booking.save()

        return Response({'message' : 'Booking confirmed successfully'})

    booking.status = 'PENDING'
    booking.save()

    return Response({'message' : 'Payment was not successful.'})
