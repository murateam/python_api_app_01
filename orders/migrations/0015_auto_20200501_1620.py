# Generated by Django 3.0.5 on 2020-05-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_stockitem_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='incorrect_factory',
            field=models.TextField(blank=True, max_length=256),
        ),
    ]
