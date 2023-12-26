from rest_framework.routers import DefaultRouter

from api.v1.shipments import views as shipment_views

router = DefaultRouter()
router.register(
    r"",
    shipment_views.ShipmentViewSet,
    basename="shipments",
)

urlpatterns = router.urls
