import uuid

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .pagination import CustomPageNumberPagination
from .serializers import ShipmentWriteSerializer, ShipmentTypeSerializer, ShipmentReadSerializer
from .services import ShipmentService, ShipmentTypeService
from .tasks import cache_exchange_rate, repeat_shipments_price_setting


class ShipmentViewSet(ViewSet):
    shipment_service = ShipmentService()
    shipment_types_service = ShipmentTypeService()
    pagination_class = CustomPageNumberPagination

    @extend_schema(
        tags=["shipments"],
        description="Показать все посылки в рамках сессии",
        responses=ShipmentReadSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name='type',
                description='Название типа посылки',
                type=str,
            ),
            OpenApiParameter(
                name='is_shipping_cost_set',
                description='Выставлена ли стоимость',
                type=bool,
            ),
        ],
    )
    def list(self, request):
        shipments_from_session = request.session.get('shipments', [])
        queryset = self.shipment_service.get_shipments_by_ids(shipments_from_session)

        # Фильтрация по типу
        type_filter = request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type__name__icontains=type_filter)

        # Фильтрация по выставленной стоимости доставки
        is_shipping_cost_set = request.query_params.get('is_shipping_cost_set') == 'true'
        if is_shipping_cost_set:
            queryset = queryset.filter(delivery_cost_in_roubles__isnull=False)

        paginated_queryset = self.pagination_class().paginate_queryset(queryset, request)
        serializer = ShipmentReadSerializer(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["shipments"],
        description="Получить данные по посылке",
        responses=ShipmentReadSerializer(),
    )
    def retrieve(self, request, pk):
        try:
            shipment_uuid = uuid.UUID(pk)
        except ValueError:
            return Response({"detail": "Неверный формат UUID"}, status=status.HTTP_400_BAD_REQUEST)

        shipment = self.shipment_service.get_shipment_by_id_and_404(pk)
        serializer = ShipmentReadSerializer(shipment)
        return Response(serializer.data)

    @extend_schema(
        tags=["shipments"],
        description="Создать посылку",
        responses=ShipmentWriteSerializer(),
        request=ShipmentWriteSerializer(),
    )
    def create(self, request):
        context = {
            "request": request,
        }
        serializer = ShipmentWriteSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        shipments = request.session.get('shipments', [])
        shipments.append(serializer.data['id'])
        request.session['shipments'] = shipments

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["shipments"],
        description="Получить все типы посылок",
        responses=ShipmentTypeSerializer(many=True),
    )
    @action(detail=False, methods=['get'], url_path='types')
    def get_shipment_types(self, request):
        queryset = self.shipment_types_service.get_shipment_types()
        serializer = ShipmentTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["shipments"],
        description="Реализовать выставление стоимости доставки",
    )
    @action(detail=False, methods=['post'], url_path='set-delivery-cost')
    def set_delivery_cost(self, request):
        cache_exchange_rate.delay()
        repeat_shipments_price_setting.delay()
        return Response({"detail": "Поставлено в очередь"}, status=status.HTTP_200_OK)
