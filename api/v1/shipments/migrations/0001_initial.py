# Generated by Django 4.2.8 on 2023-12-26 08:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


def create_shipment_types(apps, schema_editor):
    ShipmentType = apps.get_model('shipments', 'ShipmentType')
    ShipmentType.objects.create(name='Electronic')
    ShipmentType.objects.create(name='Cloth')
    ShipmentType.objects.create(name='Other')


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ShipmentType',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'shipment_types',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_in_dollars', models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    'delivery_cost_in_roubles',
                    models.DecimalField(decimal_places=2, max_digits=14, null=True),
                ),
                (
                    'type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='shipments.shipmenttype'
                    ),
                ),
            ],
            options={
                'db_table': 'shipments',
            },
        ),
        migrations.RunPython(create_shipment_types),
    ]