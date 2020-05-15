# Generated by Django 3.0.5 on 2020-05-01 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200501_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='factory_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.FactoryItem'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='import_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='import_order', to='orders.ImportOrder'),
        ),
    ]
