import uuid

from django.contrib.sessions.models import Session
from django.db import models


class Shipment(models.Model):
    class Meta:
        db_table = 'shipments'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.ForeignKey("ShipmentType", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    price_in_dollars = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost_in_roubles = models.DecimalField(max_digits=20, decimal_places=2, null=True)


class ShipmentType(models.Model):
    class Meta:
        db_table = 'shipment_types'

    name = models.CharField(max_length=255)
