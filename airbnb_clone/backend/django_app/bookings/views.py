from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Booking
from .serializers import BookingSerializer

# Create your views here.

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['listing__title', 'guest__username', 'status']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsBookingOwnerOrListingOwner()]
        return super().get_permissions()

class IsBookingOwnerOrListingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.guest == request.user or obj.listing.owner == request.user
