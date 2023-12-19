from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from purchases.models import PurchaseOrder

from vendors.models import Vendor


class VendorViewSetTests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="+91-9999999999",
            address="New Delhi",
            vendor_code="12sfth"
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="u8uhh",
            vendor=self.vendor,
            expected_delivery_date="2024-12-19T13:11:00Z",
            items={},
            quantity=2,
            issue_date="2023-12-18T17:15:00Z"
        )
        self.user = User.objects.create_user(username="gaurav", email="gaurav@mail.com", password="PerformanceAssignment@1234")
        self.client.force_authenticate(user=self.user, token=self.user.auth_token)

    def test_performance_action(self):
        # Test Case for the case when we haven't calculated any of the performance metrics even once
        # self.client.force_authenticate(user=None)

        url = reverse("vendor-performance", kwargs={"pk": self.vendor.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "on_time_delivery_rate": self.vendor.on_time_delivery_rate,
                "quality_rating_avg": self.vendor.quality_rating_avg,
                "average_response_time": self.vendor.average_response_time,
                "fulfillment_rate": self.vendor.fulfillment_rate
            }
        )

        # Updating the below model fields so that the signals updates the performance metrics of the vendor model
        self.purchase_order.status = PurchaseOrder.STATUS_CHOICES[1][0]
        self.purchase_order.actual_delivery_date = datetime.now()
        self.purchase_order.quality_rating = 5
        self.purchase_order.acknowledgment_date = datetime.now()
        self.purchase_order.save(update_fields=["status", "actual_delivery_date", "quality_rating", "acknowledgment_date"])

        response = self.client.get(url)

        # Checking if every perfomance metric is updated as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Since the purchase order is delivered before the expected date, the on time delivery rate is 1.
        self.assertEqual(response.data["on_time_delivery_rate"], 1.0)
        # Since the purchase order is delivered, fulfillment_rate is also 1
        self.assertEqual(response.data["fulfillment_rate"], 1.0)
        # As expected, quality_rating_avg is the average of all the quality ratings of the purchase orders corresponding to the vendor
        self.assertEqual(response.data["quality_rating_avg"], 5)
        # As expected, the average response time is equal to the result saved in the model.
        self.assertEqual(response.data["average_response_time"], self.vendor.average_response_time)

    def test_performance_action_invalid_vendor(self):
        # Provide an invalid vendor ID

        url = reverse("vendor-performance", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
