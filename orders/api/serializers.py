from django.contrib.auth.models import User
from rest_framework import serializers
from orders.models import CurrentRate, Client, ClientOrder

class CurrentRateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CurrentRate
		fields = ["id", "created", "current_rate"]

class ListAuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id","username"]

class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = [
			"id",
			"last_name",
			"first_name",
			"middle_name",
			"birth_date",
			"phone",
			"email",
			"passport",
			"address",
		]

class ListClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ["id","last_name", "first_name", "middle_name"]

class ClientOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientOrder
		fields = [
		'id',
		'public_num',
		'state',
		'status',
		'payment_status',
		'author',
		'client',
		'when_published',
		'created',
		'updated',
		'eur_rate',
		'price',
		'total_payment',
		'designer',
		'd_percent',
		'comment',
		]


class ListClientOrderSerializer(serializers.ModelSerializer):
	author = ListAuthorSerializer(many=False, read_only=True)
	client = ListClientSerializer(many=False, read_only=True)

	class Meta:
		model = ClientOrder
		fields = [
		'id',
		'public_num',
		'state',
		'status',
		'payment_status',
		'author',
		'client',
		'when_published',
		'created',
		'eur_rate',
		'price',
		'total_payment',
		'designer',
		'd_percent',
		'comment',
		]