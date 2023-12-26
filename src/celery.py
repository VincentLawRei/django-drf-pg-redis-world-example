import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("shipments")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# заносим таски в очередь (можно и через cron)
app.conf.beat_schedule = {
    'every_three_minutes': {
        'task': 'api.v1.shipments.tasks.repeat_shipments_price_setting',
        'schedule': timedelta(seconds=60 * 5),
    },
    'cache_exchange_rate': {
        'task': 'api.v1.shipments.tasks.cache_exchange_rate',
        'schedule': timedelta(seconds=60 * 3),
    },
}
