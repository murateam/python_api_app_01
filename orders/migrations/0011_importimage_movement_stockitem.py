# Generated by Django 3.0.5 on 2020-05-01 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0010_auto_20200501_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorrect_factory', models.CharField(blank=True, max_length=256)),
                ('stock_choices', models.CharField(choices=[('waiting for processing', 'Ждет обработки'), ('processed', 'Обработан'), ('in order', 'Заказан'), ('at exhibition', 'На выставке'), ('in stock', 'На складе'), ('sell', 'Продан'), ('cancel', 'Отмена')], default='waiting for processing', max_length=30)),
                ('items_amount', models.IntegerField(default=0)),
                ('last_price_ru', models.FloatField(default=0)),
                ('current_price_ru', models.FloatField(default=0)),
                ('last_prive_eur', models.FloatField(default=0)),
                ('current_price_eur', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('record_history', models.TextField(blank=True)),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.ClientOrder')),
                ('factory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.FactoryItem')),
                ('import_order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='import_order', to='orders.ImportOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner_new', models.CharField(max_length=128)),
                ('import_new', models.CharField(max_length=128)),
                ('items_amount', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=128)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to=settings.AUTH_USER_MODEL)),
                ('import_old', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='orders.ImportOrder')),
                ('owner_old', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='orders.ClientOrder')),
                ('stock_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='orders.StockItem')),
            ],
        ),
        migrations.CreateModel(
            name='ImportImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('file', models.ImageField(upload_to='import_images')),
                ('import_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='import_images', to='orders.ImportOrder')),
            ],
        ),
    ]
