# Generated by Django 3.0.5 on 2020-06-08 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_remove_importorder_delivery_to_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importorder',
            old_name='wight',
            new_name='weight',
        ),
    ]
