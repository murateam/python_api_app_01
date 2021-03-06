# Generated by Django 3.0.5 on 2020-04-14 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_status', models.CharField(choices=[('requires approval', 'Требуется согласование'), ('requires payment', 'Требуется доплата'), ('done', 'Выполнен')], default='requires approval', max_length=30)),
                ('description', models.CharField(max_length=128)),
                ('result', models.CharField(blank=True, max_length=128)),
                ('final_check', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('claim_data_detection', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('passport', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClientOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_num', models.CharField(max_length=10, unique=True)),
                ('state', models.CharField(choices=[('draft', 'Черновик'), ('published', 'Отправлен')], default='draft', max_length=10)),
                ('status', models.CharField(choices=[('calculate', 'Обработка'), ('in work', 'В работе'), ('in stock (check)', 'На складе (проверка)'), ('awaiting delivery/assembly', 'Ожидает доставки/сборки'), ('done', 'Выполнен'), ('claim', 'Претензия')], default='calculate', max_length=50)),
                ('payment_status', models.CharField(choices=[('waiting for payment', 'Ждем оплаты'), ('partially paid', 'Оплачен частично'), ('extra charge required', 'Требуется доплата'), ('paid', 'Оплачен')], default='waiting for payment', max_length=25)),
                ('when_published', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('eur_rate', models.FloatField(default=0, max_length=10)),
                ('price', models.FloatField(max_length=20)),
                ('total_payment', models.FloatField(default=0, max_length=20)),
                ('designer', models.CharField(blank=True, max_length=20)),
                ('d_percent', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='FactoryCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_made', models.BooleanField(default=True, verbose_name='Производится')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fabric', to='orders.Factory')),
            ],
        ),
        migrations.CreateModel(
            name='FactoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalogue_num', models.CharField(max_length=24, unique=True)),
                ('description_rus', models.CharField(max_length=256)),
                ('description_de', models.CharField(max_length=256)),
                ('fac_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factory_items', to='orders.FactoryCollection')),
            ],
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_choices', models.CharField(choices=[('waiting for processing', 'Ждет обработки'), ('processed', 'Обработан'), ('in order', 'В заказе'), ('at exhibition', 'На выставке'), ('in stock', 'На складе'), ('sell', 'Продан'), ('cancel', 'Отмена')], default='waiting for processing', max_length=30)),
                ('items_amount', models.IntegerField(default=0)),
                ('last_price', models.FloatField(default=0)),
                ('current_price', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('record_history', models.TextField(blank=True)),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.ClientOrder')),
                ('factory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='orders.FactoryItem')),
            ],
        ),
        migrations.CreateModel(
            name='ImportItem',
            fields=[
                ('stock_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='import_item', serialize=False, to='orders.StockItem')),
                ('correct_stock_item', models.CharField(max_length=32)),
                ('ordered', models.BooleanField(default=False, verbose_name='Заказан')),
                ('last_price', models.FloatField(default=0)),
                ('current_price', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('container_number', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payment_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_value', models.FloatField(max_length=10)),
                ('comment', models.TextField(blank=True, max_length=128)),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.ClientOrder')),
            ],
        ),
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('file', models.ImageField(upload_to='order_images')),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_images', to='orders.ClientOrder')),
            ],
        ),
        migrations.CreateModel(
            name='ImportOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('processing', 'Обработка'), ('waiting for payment', 'Ждем предоплаты'), ('order to factory', 'Заказ изготовителю'), ('wait for ab', 'Ждем AB'), ('description for vaitek', 'Описание для VAITEK'), ('waiting payment from vitek', 'Ждем платежки от VAITEK'), ('in germany', 'В Германии'), ('in stock', 'У нас на складе'), ('ready to delivery', 'Готов к доставке'), ('delivery agreed', 'Доставка клиенту согласована'), ('awaiting assembly', 'Ожидает сборки'), ('act uploaded', 'Акт загружен'), ('done', 'Выполнен'), ('claim', 'Рекламация')], default='processing', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('KW', models.DateField(auto_now_add=True)),
                ('delivery_to_client', models.DateField(auto_now_add=True)),
                ('AB_file', models.CharField(blank=True, max_length=128)),
                ('VAITEKfile', models.CharField(blank=True, max_length=128)),
                ('client_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='import_orders', to='orders.ClientOrder')),
                ('import_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='import_orders', to=settings.AUTH_USER_MODEL)),
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
        migrations.CreateModel(
            name='ClaimImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('file', models.ImageField(upload_to='claim_images')),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claim_images', to='orders.Claim')),
            ],
        ),
        migrations.AddField(
            model_name='claim',
            name='client_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='orders.ClientOrder'),
        ),
        migrations.CreateModel(
            name='AgreementImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('file', models.ImageField(upload_to='agreement_images')),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreement_images', to='orders.AgreementExtra')),
            ],
        ),
        migrations.AddField(
            model_name='agreementextra',
            name='component_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_agreement', to='orders.ClientOrder'),
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
                ('owner_old', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='orders.ClientOrder')),
                ('import_old', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='orders.ImportItem')),
            ],
        ),
        migrations.AddField(
            model_name='importitem',
            name='import_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='import_items', to='orders.ImportOrder'),
        ),
    ]
