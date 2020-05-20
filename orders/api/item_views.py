from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import ClientOrder
from orders.models import Factory, FactoryCollection
from orders.models import StockItem, FactoryItem

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
def stock_items_for_client_order(request):
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
	# print(data)
	for i in data:
		print(i)
	return Response(status=status.HTTP_200_OK)