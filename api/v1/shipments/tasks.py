import requests

from decimal import Decimal
from celery.utils.log import get_task_logger
from redis import Redis

from src.celery import app
from .models import Shipment
from .services import ShipmentService

shipment_service = ShipmentService()
logger = get_task_logger(__name__)
redis = Redis(host='redis', port=6379)
DAILY_EXCHANGE_RATE_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


@app.task
def repeat_shipments_price_setting():
    logger.info('Обновляем данные по стоимости доставки посылок в рублях')
    exchange_rate = redis.get('usd_exchange_rate')

    if not exchange_rate:
        logger.info('Не удалось получить курс валют')
        return False

    exchange_rate = Decimal(exchange_rate.decode('utf-8'))

    shipments = shipment_service.get_shipments_without_delivery_cost()
    if shipments:
        logger.info(f'Найдено {len(shipments)} посылок без стоимости доставки')
        for shipment in shipments:
            shipment.delivery_cost_in_roubles = (
                ((shipment.weight * Decimal('0.5')) + (shipment.price_in_dollars * Decimal('0.01')))
            ) * exchange_rate
        Shipment.objects.bulk_update(
            shipments,
            ['delivery_cost_in_roubles'],
        )
    else:
        logger.info('Нет посылок без стоимости доставки')
    return True


@app.task
def cache_exchange_rate():
    logger.info('Кэшируем курс валют')
    response = requests.get(DAILY_EXCHANGE_RATE_URL)
    data = response.json()
    usd_value = data['Valute']['USD']['Value']
    logger.info(f'Курс доллара на данный момент: {usd_value}')
    redis.set('usd_exchange_rate', usd_value)
    return True
