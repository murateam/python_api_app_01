# Generated by Django 3.0.5 on 2020-06-21 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0041_remove_factoryitem_factory_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoryitem',
            name='factory_collection',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='factory_items', to='orders.FactoryCollection'),
            preserve_default=False,
        ),
    ]