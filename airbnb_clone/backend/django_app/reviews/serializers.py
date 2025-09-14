from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Review._meta.get_field('listing').related_model.objects.all(), source='listing', write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'listing', 'listing_id', 'guest', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'guest', 'listing', 'created_at']

