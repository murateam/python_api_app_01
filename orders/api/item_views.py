from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict

from orders.models import ClientOrder
from orders.models import Factory, FactoryCollection, FactoryItem
from orders.models import StockItem

from orders.api.item_serializers import FactorySerializer, FactoryCollectionSerializer
from orders.api.item_serializers import ListFactoryItemSerializer, FactoryItemSerializer
from orders.api.item_serializers import StockItemSerializer, ListStockItemSerializer
from orders.api.item_serializers import ListNameFactorySerializer, ListNameFactoryCollectionSerializer, ListNumberFactoryItemSerializer


class FactoryView(ListCreateAPIView):
	queryset = Factory.objects.all()
	serializer_class = FactorySerializer

class ListNameFactoryView(ListCreateAPIView):
	queryset = Factory.objects.all()
	serializer_class = ListNameFactorySerializer

class SingleFactoryView(RetrieveUpdateDestroyAPIView):
	queryset = Factory.objects.all()
	serializer_class = FactorySerializer


class FactoryCollectionView(ListCreateAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = FactoryCollectionSerializer

class ListNameFactoryCollectionView(ListCreateAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = ListNameFactoryCollectionSerializer

@api_view(['POST'])
def list_name_factory_collections(request):
	"""
		GET factory collection by factory name
	"""
	data = JSONParser().parse(request)
	factory = Factory.objects.filter(name=data[0]['value']).first()
	factory_collections = factory.collections.all()
	serializer = ListNameFactoryCollectionSerializer(factory_collections, many=True)
	return Response(serializer.data)
	# return Response(status=status.HTTP_200_OK)


class SingleFactoryCollectionView(RetrieveUpdateDestroyAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = FactoryCollectionSerializer


class ListFactoryItemView(ListCreateAPIView):
	queryset = FactoryItem.objects.all()
	serializer_class = ListFactoryItemSerializer

class ListNumberFactoryItemView(ListCreateAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = ListNumberFactoryItemSerializer

@api_view(['POST'])
def list_catalogue_numbers(request):
	"""
		GET catalogue numbers by factory collection
	"""
	data = JSONParser().parse(request)
	factory_collections = FactoryCollection.objects.filter(name=data[0]['value']).first()
	factory_items = factory_collections.factory_items.all()
	serializer = ListNumberFactoryItemSerializer(factory_items, many=True)
	return Response(serializer.data)


class SingleFactoryItemView(RetrieveUpdateDestroyAPIView):
	queryset = FactoryItem.objects.all()
	serializer_class = FactoryItemSerializer
	

class ListStockItemView(ListCreateAPIView):
	queryset = StockItem.objects.all()
	serializer_class = ListStockItemSerializer


@api_view(['POST'])
def get_stock_items_for_client_order(request):
	"""
		get StockItems by CLientOrder ID
	"""
	data = JSONParser().parse(request)
	client_order = ClientOrder.objects.get(id=data['client_order'])
	stock_items = client_order.stock_items.all()

	serializer = ListStockItemSerializer(stock_items, many=True)
	return Response(serializer.data)


def save_item(item, client_order_id):
	"""
		The function is checking and save items

		  If item have field 'incorrect_factory',
		this item is saved and haven't changes so it doesn't need to save again
		  It saves item in four scenarios:
		  1) as exist and correct
		  2) as exist and incorrect
		  3) as new and correct
		  4) as new and incorrect
	"""

	def item_is_correct(item):
		if item['factory_item']:
			catalogue_number = item['factory_item']['catalogue_number']
			factory_collection = item['factory_item']['factory_collection']['name']
			factory = item['factory_item']['factory_collection']['factory']['name']

			found_factory_item = FactoryItem.objects.filter(catalogue_number=item['factory_item']['catalogue_number']).first()

			if found_factory_item:
				found_catalogue_number = found_factory_item.catalogue_number
				found_factory_collection = found_factory_item.factory_collection.name
				found_factory = found_factory_item.factory_collection.factory.name

				if catalogue_number == found_catalogue_number and factory_collection == found_factory_collection and factory == found_factory:
					return found_factory_item
		return 'incorrect'

	def save_exist_correct_item(item, correct_item):
		exist_item = StockItem.objects.get(pk=item['id'])
		client_order = item['client_order']['id']
		factory_item = correct_item.id
		item['client_order'] = client_order
		item['factory_item'] = factory_item
		item['is_correct'] = True
		serializer = StockItemSerializer(exist_item, data=item)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)

	def save_exist_incorrect_item(item):
		exist_item = StockItem.objects.get(pk=item['id'])
		client_order = item['client_order']['id']
		item['client_order'] = client_order
		item['incorrect_factory'] = f"{item['factory_item']['factory_collection']['factory']['name']}&{item['factory_item']['factory_collection']['name']}&{item['factory_item']['catalogue_number']}"
		item['factory_item'] = None
		item['is_correct'] = False
		serializer = StockItemSerializer(exist_item, data=item)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)	

	def save_new_correct_item(item):
		item['client_order'] = client_order_id	
		item['is_correct'] = True
		serializer = StockItemSerializer(data=item)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)


	def save_new_incorrect_item(item):
		item['client_order'] = client_order_id
		item['incorrect_factory'] = f"{item['factory_item']['factory_collection']['factory']['name']}&{item['factory_item']['factory_collection']['name']}&{item['factory_item']['catalogue_number']}"
		item['factory_item'] = None
		item['is_correct'] = False
		serializer = StockItemSerializer(data=item)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)

	if len(item['incorrect_factory']) == 0:

		if item['id']:
			correct_item = item_is_correct(item)
			if correct_item != 'incorrect':
				print('exist correct')
				save_exist_correct_item(item, correct_item)
			else:
				print('exist incorrect')
				save_exist_incorrect_item(item)
		else:
			if item_is_correct(item) == 'correct':
				print('don\'t exist correct')
				save_new_correct_item(item)
			else:
				print('don\'t exist incorrect')
				save_new_incorrect_item(item)
		


def delete_exist_item(item):
	if item['id']:
		obj = StockItem.objects.filter(id=item['id']).delete()
		print(obj)

@api_view(['POST'])
def save_stock_items_from_client_order(request):
	"""
		save existed and new stock items coming from client order
	"""
	data = JSONParser().parse(request)
	client_order_id = data[0]['value']
	list_items_to_save = data[1]['value']
	list_items_to_delete = data[2]['value']

	
	for item in list_items_to_save:
			save_item(item, client_order_id)

	for item in list_items_to_delete:
		delete_exist_item(item)

	client_order = ClientOrder.objects.get(id=client_order_id)
	stock_items = client_order.stock_items.all()

	serializer = ListStockItemSerializer(stock_items, many=True)
	return Response(serializer.data)

	# return Response(status=status.HTTP_200_OK)