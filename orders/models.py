from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CurrentRate(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	current_rate = models.IntegerField()

	def __str__(self):
		return str(self.current_rate) + ' ' + 'RUB/EUR' + ' ' + str(self.created).split(' ')[0]


class Client(models.Model):
	'''клиент'''
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	birth_date = models.DateField()
	phone = models.CharField(max_length=20)
	email = models.EmailField()
	passport = models.CharField(max_length=129, unique=True)
	#adress
	address = models.CharField(max_length=128)

	def __str__(self):
		return str(self.last_name)+' '+str(self.first_name)[0]+'.'+' '+str(self.middle_name)[0]+'.'


class Factory(models.Model):
	'''Фабрика'''
	name = models.CharField(max_length=64)

	def __str__(self):
		return str(self.name)


class FactoryCollection(models.Model):
	'''Коллекция фабрики'''
	factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='collections')
	name = models.CharField(max_length=64)
	is_made = models.BooleanField("Производится", default=True)

	def __str__(self):
		return str(self.name)


class ClientOrder(models.Model):
	'''Заказ со стороны местного клиента'''
	STATUS_CHOICES = (
		('draft', 'Черновик'),
		('published', 'Отправлен'),
	)
	STATUS_ORDER = (
		('calculate', 'Обработка'),
		('in work', 'В работе'),
		('in stock (check)', 'На складе (проверка)'),
		('awaiting delivery/assembly', 'Ожидает доставки/сборки'),
		('done', 'Выполнен'),
		('claim', 'Претензия'),
	)
	STATUS_PAYMENT = (
		('waiting for payment', 'Ждем оплаты'),
		('partially paid', 'Оплачен частично'),
		('extra charge required', 'Требуется доплата'),
		('paid', 'Оплачен'),
	)

	public_num = models.CharField(max_length=10, unique=True)
	state = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	status = models.CharField(max_length=50, choices=STATUS_ORDER, default='calculate')
	payment_status = models.CharField(max_length=25, choices=STATUS_PAYMENT, default='waiting for payment')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
	when_published = models.DateTimeField(default=timezone.now, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# eur_rate = models.FloatField(max_length=10, default=0)
	eur_rate = models.ForeignKey(CurrentRate, on_delete=models.CASCADE, related_name='eur_rate', blank=True, null=True)
	price = models.FloatField(max_length=20, default=0)
	total_payment = models.FloatField(max_length=20, default=0)
	designer = models.CharField(max_length=20, blank=True)
	d_percent = models.IntegerField(default=0)
	comment = models.TextField(blank=True)

	def __str__(self):
		return str(self.public_num)+' '+str(str(self.created).split(' ')[0])+' '+str(self.client)


class OrderImage(models.Model):
	'''Документы к заказу клиента'''
	description = models.CharField(max_length=128)
	client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='order_images')
	file = models.ImageField(upload_to='order_images')

	def __str__(self):
		return str(self.client_order.public_num)


class Payment(models.Model):
	'''Платежы, привязаны к заказу определенного клиента'''
	created = models.DateTimeField(auto_now_add=True)
	client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='payments')
	payment_date = models.DateTimeField(default=timezone.now)
	payment_value = models.FloatField(max_length=10)
	comment = models.TextField(max_length=128, blank=True)

	def __str__(self):
		return str(self.client_order.public_num) + '-' + str(self.payment_value) + ' ' + str(self.client_order.client)


class Claim(models.Model):
	'''Претензия'''
	created = models.DateTimeField(auto_now_add=True)
	client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='claims')
	claim_data_detection = models.DateTimeField(default=timezone.now)
	comment = models.TextField(max_length=128)

	def __str__(self):
		return str(self.client_order) + ' -- ' + str(self.comment)

class ClaimImage(models.Model):
	'''Документы и фото к претензии'''
	description = models.CharField(max_length=128)
	claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='claim_images')
	file = models.ImageField(upload_to='claim_images')

	def __str__(self):
		return str(str(self.claim).split(' ')[0])+' '+str(self.description)


class ImportOrder(models.Model):
	'''Заказ заводу изготовителю. Привязан к заказу клиента'''
	STATUS_CHOICES = (
		('processing', 'Обработка'),
		('waiting for payment', 'Ждем предоплаты'),
		('order to factory', 'Заказ изготовителю'),
		('wait for ab', 'Ждем AB'),
		('description for vaitek', 'Описание для VAITEK'),
		('waiting payment from vitek','Ждем платежки от VAITEK'),
		('in germany','В Германии'),
		('in stock','У нас на складе'),
		('ready to delivery','Готов к доставке'),
		('delivery agreed', 'Доставка клиенту согласована'),
		('awaiting assembly','Ожидает сборки'),
		('act uploaded', 'Акт загружен'),
		('done','Выполнен'),
		('claim', 'Рекламация'),
	)
	import_number = models.CharField(max_length=10, unique=True)
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')
	import_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='import_orders')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='import_orders')
	#KW from AB неделя отгрузки
	KW = models.CharField(max_length=16, blank=True)
	delivery_to_client = models.DateField(auto_now_add=True)
	AB_num = models.CharField(max_length=32, blank=True)
	AB_file = models.ImageField(blank=True)
	VAITEK_order = models.CharField(max_length=128, blank=True)
	VAITEK_payment = models.ImageField(blank=True)
	bill = models.ImageField(blank=True)
	TTN = models.ImageField(blank=True)
	TRID = models.CharField(max_length=128, blank=True)
	count_place = models.IntegerField(default=0)
	volume = models.FloatField(default=0)
	wight = models.FloatField(default=0)
	container_num = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return str(self.import_user)+'  '+str(self.client_order.public_num) 

class FactoryItem(models.Model):
	'''Каталожный номер фабрик с немецким и русским описание. Добовляется к заказу через StockItem'''
	factory_collection = models.ForeignKey(FactoryCollection, on_delete=models.CASCADE, related_name='factory_items')
	catalogue_number = models.CharField(max_length=24)
	description_rus = models.CharField(max_length=256)
	description_de = models.CharField(max_length=256)

	def __str__(self):
		return str(self.catalogue_number) + ' ' + str(self.factory_collection.factory).upper() + ' ' + str(self.factory_collection)

class StockItem(models.Model):
	'''Складская позиция. Отслеживает положение каждой заказанной позиции'''
	STOCK_CHOICES = (
		('waiting for processing', 'Ждет обработки'),
		('processed', 'Обработан'),
		('in order', 'Заказан'),
		('at exhibition', 'На выставке'),
		('in stock', 'На складе'),
		('sell', 'Продан'),
		('cancel', 'Отмена'),

	)
	client_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='stock_items')
	factory_item = models.ForeignKey(FactoryItem, on_delete=models.CASCADE, related_name='stock_items', blank=True, null=True)
	import_order = models.ForeignKey(ImportOrder, on_delete=models.CASCADE, related_name='stock_items', blank=True, null=True)
	incorrect_factory = models.TextField(max_length=256, blank=True)
	is_correct = models.BooleanField('Корректный', default=False)
	is_ordered = models.BooleanField('Заказан', default=False)
	is_shipped = models.BooleanField('Отгружен', default=False)
	stock_choices = models.CharField(max_length=30, choices=STOCK_CHOICES, default='cancel')
	items_amount = models.IntegerField(default=0)
	#prices
	last_price_ru = models.FloatField(default=0)
	current_price_ru = models.FloatField(default=0)
	last_price_eur = models.FloatField(default=0)
	current_price_eur = models.FloatField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=250, blank=True)
	record_history = models.TextField(blank=True)

	def __str__(self):
		return str(self.client_order) + ' ' + str(self.factory_item)


# class ImportItem(models.Model):
# 	'''Прослойка для добовления корректной складской позиции в импорт заказ'''
# 	import_order = models.ForeignKey(ImportOrder, on_delete=models.CASCADE, related_name='import_items')
# 	stock_item = models.OneToOneField(StockItem, on_delete=models.CASCADE, primary_key=True, related_name='import_item')
# 	correct_stock_item = models.CharField(max_length=32)
# 	# Позиция считается заказанной если у импорт заказа в который входит проставлен контейнер
# 	ordered = models.BooleanField('Заказан', default=False)
# 	# euro
# 	last_price = models.FloatField(default=0)
# 	current_price = models.FloatField(default=0)
# 	comment = models.TextField(blank=True)
# 	# add container
# 	container_number = models.CharField(max_length=10, blank=True)
# 	# bns, колличество мест, объем


# 	def __str__(self):
# 		return str(self.import_order)+' '+str(self.correct_stock_item)


class AgreementExtra(models.Model):
	'''Дополнительное согласование. Если требуется'''
	AGREEMENT_STATUS = (
		('requires approval', 'Требуется согласование'),
		('requires payment', 'Требуется доплата'),
		('done', 'Выполнен'),
	)
	component_order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='extra_agreement')
	agreement_status = models.CharField(max_length=30, choices=AGREEMENT_STATUS, default='requires approval')
	# Описывается причина при создании
	description = models.CharField(max_length=128)
	# Результат описывает манагер и подтягивает необходимые документы
	result = models.CharField(max_length=128, blank=True)
	# Проверка результато манагера
	final_check = models.CharField(max_length=128, blank=True)

	def __str__(self):
		return 'Согласование'+' '+str(self.agreement_status)

class AgreementImage(models.Model):
	'''Документы для доп. согласований'''
	description = models.CharField(max_length=128)
	agreement = models.ForeignKey(AgreementExtra, on_delete=models.CASCADE, related_name='agreement_images')
	file = models.ImageField(upload_to='agreement_images')

	def __str__(self):
		return str(self.agreement)

class ImportImage(models.Model):
	'''документы к заказу на импорт AB, счета'''
	description = models.CharField(max_length=128)
	import_order = models.ForeignKey(ImportOrder, on_delete=models.CASCADE, related_name='import_images')
	file = models.ImageField(upload_to='import_images')

	def __str__(self):
		return str(self.import_order)

class Movement(models.Model):
	'''Объект для смены владельца складской позиции'''
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movements')
	stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='movements')
	owner_old = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='movements')
	owner_new = models.CharField(max_length=128)
	import_old = models.ForeignKey(ImportOrder, on_delete=models.CASCADE, related_name='movements')
	import_new = models.CharField(max_length=128)
	items_amount = models.IntegerField(default=0)
	comment = models.CharField(max_length=128)

	def __str__(self):
		return 'Move' + ' ' + str(self.owner_old) + ' -> ' + str(self.owner_new)