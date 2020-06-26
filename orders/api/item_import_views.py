from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import StockItem, ImportOrder
from orders.api.item_serializers import ListStockItemExpSerializer, SingleStockItemExpSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

class ListStockItemExpView(ListCreateAPIView):
	queryset = StockItem.objects.filter(stock_choices="waiting for processing")
	serializer_class = ListStockItemExpSerializer

class SingleStockItemExpView(RetrieveUpdateDestroyAPIView):
	queryset = StockItem.objects.all()
	serializer_class = SingleStockItemExpSerializer

@api_view(['GET'])
def get_stock_items_by_import_order(request, pk):
	"""
		get StockItems by ImportOrder ID
	"""
	# data = JSONParser().parse(request)
	import_order = ImportOrder.objects.get(id=pk)
	stock_items = import_order.stock_items.all()

	serializer = ListStockItemExpSerializer(stock_items, many=True)
	return Response(serializer.data)