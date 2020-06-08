from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import ImportOrder
from orders.api.import_serializers import ImportOrderSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from rest_framework.parsers import JSONParser

class ListImportOrdersView(ListCreateAPIView):
	queryset = ImportOrder.objects.all()
	serializer_class = ImportOrderSerializer

class SingleImportOrderView(RetrieveUpdateDestroyAPIView):
	queryset = ImportOrder.objects.all()
	serializer_class = ImportOrderSerializer