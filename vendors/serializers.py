from rest_framework import serializers

from vendors.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    vendor_id = serializers.ReadOnlyField(source="id")

    class Meta:
        model = Vendor
        fields = ("vendor_id", "name", "contact_details", "address", "vendor_code")
