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


@api_view(['POST'])
def save_new_import_order(request):
	"""
		first of all get new uniq number for import order
	"""
	def get_uniq_number():
		now = datetime.now()
		last_import_order = ImportOrder.objects.last()
		if last_import_order == None or int(last_import_order.import_number.split("-")[0]) != now.year:
			new_uniq_import_number = str(now.year) + "-" + "%04d" % (1)
			return new_uniq_import_number
		elif int(last_import_order.import_number.split("-")[0]) == now.year:
			new_uniq_import_number = str(now.year) + "-" + "%04d" % (int(last_import_order.import_number.split("-")[1])+1)
			return new_uniq_import_number

	if request.method == 'POST':
		data = JSONParser().parse(request)
		data['import_number'] = get_uniq_number()
		serializer = ImportOrderSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)
		# return Response(status=status.HTTP_200_OK)

