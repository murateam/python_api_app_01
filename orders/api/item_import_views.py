from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import StockItem
from orders.api.item_serializers import ListStockItemExpSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

class ListStockItemExpView(ListCreateAPIView):
	queryset = StockItem.objects.filter(stock_choices="waiting for processing")
	serializer_class = ListStockItemExpSerializer

class SingleStockItemExpView(RetrieveUpdateDestroyAPIView):
	queryset = StockItem.objects.all()
	serializer_class = ListStockItemExpSerializer