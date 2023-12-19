from django.db import models


class Vendor(models.Model):
    """
    Model for storing essential information about each vendor and their performance metrics.
    """
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True, help_text="Represents average response time in minutes")
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Vendor with id: {self.id} and name: {self.name}"
