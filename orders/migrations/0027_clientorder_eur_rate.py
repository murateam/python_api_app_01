# Generated by Django 3.0.5 on 2020-05-26 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_auto_20200526_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientorder',
            name='eur_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eur_rate', to='orders.CurrentRate'),
        ),
    ]
