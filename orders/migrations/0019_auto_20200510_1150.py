# Generated by Django 3.0.5 on 2020-05-10 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20200510_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='import_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.ImportOrder'),
        ),
    ]
