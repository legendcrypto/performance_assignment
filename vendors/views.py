from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from vendors.models import Vendor
from vendors.serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Vendor instances.
    API Endpoints:
        POST /api/vendors/: Create a new vendor.
        GET /api/vendors/: List all vendors.
        GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
        PUT /api/vendors/{vendor_id}/: Update a vendor's details.
        DELETE /api/vendors/{vendor_id}/: Delete a vendor.
        GET /api/vendors/{vendor_id}/performance: Gives the performance metrics of a vendor
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        """
        Custom action to retrieve vendor performance.
        """
        vendor = self.get_object()
        performance_data = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate
        }

        return Response(performance_data)
