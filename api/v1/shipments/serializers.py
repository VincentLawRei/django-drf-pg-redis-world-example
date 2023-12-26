from rest_framework import serializers

from .models import Shipment, ShipmentType


class ShipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentType
        fields = (
            "id",
            "name",
        )


class ShipmentReadSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Shipment
        fields = (
            "id",
            "name",
            "weight",
            "type",
            "price_in_dollars",
            "delivery_cost_in_roubles",
        )


class ShipmentWriteSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=ShipmentType.objects.all(),
        error_messages={
            'does_not_exist': 'Неверный идентификатор типа посылки.',
            'incorrect_type': 'Значение поля type должно быть корректным идентификатором.',
        },
    )

    class Meta:
        model = Shipment
        fields = (
            "id",
            "name",
            "weight",
            "type",
            "price_in_dollars",
        )
        read_only_fields = (
            "id",
            "delivery_cost_in_roubles",
        )
        extra_kwargs = {
            "name": {"write_only": True},
            "weight": {"write_only": True},
            "price_in_dollars": {"write_only": True},
        }

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Вес посылки должен быть больше нуля.")
        return value

    def validate_price_in_dollars(self, value):
        if value <= 0:
            raise serializers.ValidationError("Стоимость должна быть больше нуля.")
        return value
