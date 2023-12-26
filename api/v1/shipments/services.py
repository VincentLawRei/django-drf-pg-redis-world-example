from django.db.models import QuerySet

from helpers.decorators import except_shell
from .models import Shipment, ShipmentType


class ShipmentService:
    def get_shipments(self) -> QuerySet[Shipment]:
        return Shipment.objects.all()

    @except_shell((Shipment.DoesNotExist,), raise_404=True)
    def get_shipment_by_id_and_404(self, pk: int) -> Shipment:
        return Shipment.objects.get(pk=pk)

    def get_shipments_by_ids(self, ids: list) -> QuerySet[Shipment]:
        return self.get_shipments().filter(id__in=ids)

    def get_shipments_without_delivery_cost(self) -> QuerySet[Shipment]:
        return self.get_shipments().filter(delivery_cost_in_roubles__isnull=True)


class ShipmentTypeService:
    def get_shipment_types(self) -> QuerySet[ShipmentType]:
        return ShipmentType.objects.all()
