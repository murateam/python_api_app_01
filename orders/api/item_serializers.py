from rest_framework import serializers
from orders.models import Factory, FactoryCollection
from orders.models import StockItem, FactoryItem

from orders.api.serializers import ListClientOrderSerializer


class FactorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Factory
		fields = ['id', 'name']

class ListNameFactorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Factory
		fields = ['id', 'name']

class FactoryCollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = FactoryCollection
		fields = ['id', 'name', 'factory', 'is_made']

class ListNameFactoryCollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = FactoryCollection
		fields = ['id', 'name']

class ListFactoryCollectionSerializer(serializers.ModelSerializer):
	factory = FactorySerializer(many=False, read_only=True)
	class Meta:
		model = FactoryCollection
		fields = ['id', 'name', 'factory', 'is_made']

class FactoryItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FactoryItem
		fields = [
			'id',
			'factory_collection',
			'catalogue_number',
			'description_rus',
			'description_de',
		]

class ListFactoryItemSerializer(serializers.ModelSerializer):
	factory_collection = ListFactoryCollectionSerializer(many=False, read_only=True)
	class Meta:
		model = FactoryItem
		fields = ['id', 'factory_collection', 'catalogue_number']

class ListNumberFactoryItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FactoryItem
		fields = ['id', 'catalogue_number']

class StockItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = StockItem
		fields = [
			'id',
			'client_order',
			'factory_item',
			'import_order',
			'incorrect_factory',
			'stock_choices',
			'items_amount',
			'last_price_ru',
			'current_price_eur',
			'last_price_eur',
			'current_price_eur',
			'created',
			'comment',
			'record_history'
		]

class ListStockItemSerializer(serializers.ModelSerializer):
	factory_item = ListFactoryItemSerializer(many=False, read_only=True)
	client_order = ListClientOrderSerializer(many=False, read_only=True)
	class Meta:
		model = StockItem
		fields = [
			'id',
			'client_order',
			'factory_item',
			'import_order',
			'incorrect_factory',
			'is_correct',
			'stock_choices',
			'items_amount',
			'stock_choices',
			'current_price_eur'
		]

class ListStockItemExpSerializer(serializers.ModelSerializer):
	factory_item = ListFactoryItemSerializer(many=False, read_only=True)
	client_order = ListClientOrderSerializer(many=False, read_only=True)
	class Meta:
		model = StockItem
		fields = [
			'id',
			'client_order',
			'factory_item',
			'import_order',
			'incorrect_factory',
			'is_correct',
			'is_ordered',
			'is_shipped',
			'stock_choices',
			'items_amount',
			'last_price_ru',
			'current_price_ru',
			'last_price_eur',
			'current_price_eur',
			'created',
			'comment',
			'record_history',
			'bank_euro_rate',
			'factory_price_eur',
			'factor',
		]
