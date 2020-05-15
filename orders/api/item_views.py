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
def client_order_items(request):
	"""
		get StockItems by CLientOrder ID
	"""
	data = JSONParser().parse(request)
	print(data)
	client_order = ClientOrder.objects.get(id=data['client_order'])
	stock_items = client_order.stock_items.all()

	# stock_items = StockItem.objects.filter(client_order__pk=data['client_order'])
	# print(stock_items)

	serializer = ListStockItemSerializer(stock_items, many=True)
	return Response(serializer.data)

# class StockItemView(ListCreateAPIView):
# 	serializer_class = ListStockItemSerializer