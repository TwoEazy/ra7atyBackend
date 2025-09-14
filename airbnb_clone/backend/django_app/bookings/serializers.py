from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Booking._meta.get_field('listing').related_model.objects.all(), source='listing', write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'listing_id', 'guest', 'start_date', 'end_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'guest', 'listing', 'status', 'created_at', 'updated_at']

