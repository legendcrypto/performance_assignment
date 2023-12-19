from django.urls import path, include

from rest_framework.routers import DefaultRouter

from purchases.views import PurchaseOrderViewSet

router = DefaultRouter()
router.register(r"purchase_orders", PurchaseOrderViewSet, basename="purchase_orders")

urlpatterns = [
    path("", include(router.urls)),
]
