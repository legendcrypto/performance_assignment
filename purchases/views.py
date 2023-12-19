from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from purchases.models import PurchaseOrder
from purchases.serializers import PurchaseOrderSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Purchase Order instances.

    API Endpoints:
    - POST /api/purchase_orders/: Create a purchase order.
    - GET /api/purchase_orders/?vendor_id={vendor_id}: List all purchase orders with an option to filter by vendor.
    - GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    - PUT /api/purchase_orders/{po_id}/: Update a purchase order.
    - PATCH /api/purchase_orders/{po_id}/: Partially update a purchase order.
    - DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):

        if self.action == "list":
            vendor_id = self.request.query_params.get("vendor_id")

            if vendor_id:
                queryset = queryset.filter(vendor_id=vendor_id)

        return super(PurchaseOrderViewSet, self).filter_queryset(queryset)
