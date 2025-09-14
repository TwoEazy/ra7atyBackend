from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

