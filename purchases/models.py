from datetime import datetime

from django.db import models

from vendors.models import Vendor


class PurchaseOrder(models.Model):
    """
    Model for capturing the details of each purchase order and is used to calculate various
    performance metrics.
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(default=dict)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(PurchaseOrder, self).__init__(*args, **kwargs)

        # Storing these fields in new variables so that at the time of saving, we can compare the previous values with the new ones
        self.initial_status = self.status
        self.initial_acknowledgment_date = self.acknowledgment_date

    def save(self, *args, **kwargs):
        if not self.items:
            self.items = {}
        
        if self.is_status_changed_to_completed:
            self.actual_delivery_date = datetime.now()

        super(PurchaseOrder, self).save(*args, **kwargs)

    @property
    def is_status_changed_to_completed(self):
        """
        Returns True if the status is changed to completed
        """
        return self.status == self.STATUS_CHOICES[1][0] and self.status != self.initial_status

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"


class HistoricalPerformance(models.Model):
    """
    Model which optionally stores historical data on vendor performance, enabling trend analysis. 
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
