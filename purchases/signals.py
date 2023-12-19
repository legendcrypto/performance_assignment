from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, ExpressionWrapper, fields, F

from rest_framework.authtoken.models import Token

from purchases.models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def handle_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    # Queryset of POs relating the instance's vendor
    queryset = PurchaseOrder.objects.filter(
        vendor_id=instance.vendor_id
    )
    # Count of the purchase orders which were issued to the vendor
    issued_pos = queryset.count()

    if instance.status != instance.initial_status:
        # Queryset of the Purchase orders which are marked as completed
        completed_pos_queryset = queryset.filter(
            status=PurchaseOrder.STATUS_CHOICES[1][0]
        )

        if instance.is_status_changed_to_completed:
            queryset = completed_pos_queryset
            orders_delivered = queryset.count()
            orders_delivered_on_time = queryset.filter(
                expected_delivery_date__gte=F("actual_delivery_date")
            ).count()

            # assign on_time_delivery_rate to the ratio of orders delivered on or before expected delivery date
            # to the total orders delivered.
            if orders_delivered:
                vendor.on_time_delivery_rate = orders_delivered_on_time / orders_delivered
            
            # If the quality rating is also not none then get the average of all the quality ratings
            if instance.quality_rating:
                vendor.quality_rating_avg = queryset.aggregate(quality_rating_avg=Avg("quality_rating"))["quality_rating_avg"]

        # Every time the status of PO is updated, assign fulfillment_rate to the ratio of count of completed POs
        # to the total issued POs to the vendor
        if issued_pos:
            vendor.fulfillment_rate = completed_pos_queryset.count() / issued_pos
    elif instance.acknowledgment_date and instance.initial_acknowledgment_date != instance.acknowledgment_date:
        time_difference_expression = ExpressionWrapper(
            F("acknowledgment_date") - F("issue_date"),
            output_field=fields.DurationField()
        )
        annotated_queryset = queryset.annotate(time_difference=time_difference_expression)
        # Compute the average time difference for all orders of the vendor
        average_time_difference = annotated_queryset.aggregate(avg_time=Avg("time_difference"))["avg_time"]
        vendor.average_response_time = average_time_difference.total_seconds() / 60

    # Save all the fields of the vendor which were updated above
    vendor.save(update_fields=["on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate"])


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
