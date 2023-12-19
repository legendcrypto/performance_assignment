from rest_framework import serializers

from purchases.models import PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = PurchaseOrder
        fields = (
            "po_id",
            "po_number",
            "vendor",
            "expected_delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgment_date"
        )
