from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import ClientOrder
from orders.models import Factory, FactoryCollection, FactoryItem
from orders.models import StockItem

from orders.api.item_serializers import FactorySerializer, FactoryCollectionSerializer
from orders.api.item_serializers import ListFactoryItemSerializer, FactoryItemSerializer
from orders.api.item_serializers import StockItemSerializer, ListStockItemSerializer


class FactoryView(ListCreateAPIView):
	queryset = Factory.objects.all()
	serializer_class = FactorySerializer

class SingleFactoryView(RetrieveUpdateDestroyAPIView):
	queryset = Factory.objects.all()
	serializer_class = FactorySerializer

class FactoryCollectionView(ListCreateAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = FactoryCollectionSerializer

class SingleFactoryCollectionView(RetrieveUpdateDestroyAPIView):
	queryset = FactoryCollection.objects.all()
	serializer_class = FactoryCollectionSerializer

class ListFactoryItemView(ListCreateAPIView):
	queryset = FactoryItem.objects.all()
	serializer_class = ListFactoryItemSerializer

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

@api_view(['POST'])
def save_stock_items_from_client_order(request):
	"""
		save existed and new stock items coming from client order
	"""
	data = JSONParser().parse(request)
	client_order_id = data[0]['value']
	list_items_to_save = data[1]['value']
	list_items_to_delete = data[2]['value']

	def cut_exist_item(item):
		client_order = item['client_order']['id']
		factory_item = item['factory_item']['id']
		item['client_order'] = client_order
		item['factory_item'] = factory_item
		return item

	def check_for_exist_item_factory(item):
		# print(item['factory_item'])
		catalogue_number = item['factory_item']['catalogue_number']
		factory_collection = item['factory_item']['factory_collection']['name']
		factory = item['factory_item']['factory_collection']['factory']['name']

		# factory_item = FactoryItem.objects.filter(catalogue_number=item['factory_item']['catalogue_number']).first()
		
		# print(factory_item.factory_collection.factory)

	check_for_exist_item_factory(list_items_to_save[2])

	
	# for item in list_items_to_save:
	# 	if item['client_order']['id'] != None: 
	# 		serializer = StockItemSerializer(data=item)
	# 		serializer.is_valid()
	# 		print(serializer.errors)
		# else:
		# 	print("don't have ID")

	# print(list_items_to_save[0]['client_order']['id'])

	return Response(status=status.HTTP_200_OK)