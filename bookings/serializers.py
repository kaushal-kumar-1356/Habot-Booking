from rest_framework import serializers
from .models import Parent, LSA_Profile, Booking_Request, Payment

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class LSASerializer(serializers.ModelSerializer):
    class Meta:
        model = LSA_Profile
        fields = '__all__'


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Request
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'amount',
            'status',
            'transaction_id'
        ]
        read_only_fields = [
            'id',
            'status',
            'transaction_id'
        ]