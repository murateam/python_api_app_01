from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from orders.models import CurrentRate, Client, ClientOrder

from orders.api.serializers import CurrentRateSerializer
from orders.api.serializers import ClientSerializer, ListClientSerializer
from orders.api.serializers import ClientOrderSerializer, ListClientOrderSerializer

from rest_framework.views import APIView
from django.utils.dateparse import parse_date

from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime


@api_view(['POST'])
def save_new_client(request):
	data = JSONParser().parse(request)
	convert_to_date = parse_date(data['birth_date'])
	data['birth_date'] = convert_to_date
	serializer = ClientSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	else:
		return Response(serializer.errors)

	

class ListClientView(ListCreateAPIView):
	queryset = Client.objects.all()
	serializer_class = ListClientSerializer

class SingleClientView(generics.RetrieveUpdateAPIView):
	queryset = Client.objects.all()
	serializer_class = ClientSerializer

@api_view(['POST'])
def client_order_to_import(request):
	"""
		send to import client_order and its items
	"""
	data = JSONParser().parse(request)
	data['client'] = data['client']['id']
	data['author'] = data['author']['id']

	data['state'] = 'published'
	data['when_published'] = datetime.now(tz=timezone.utc)
	exist_client_order = ClientOrder.objects.get(pk=data['id'])
	
	serializer = ClientOrderSerializer(exist_client_order, data=data)
	if serializer.is_valid():
		serializer.save()

		for item in exist_client_order.stock_items.all():
			item.stock_choices = 'waiting for processing'
			item.save()
		return Response(serializer.data)
	else: 
		return Response(serializer.errors)

	# return Response(status=status.HTTP_200_OK)

class ListClientOrderView(ListCreateAPIView):
	queryset = ClientOrder.objects.all()
	serializer_class = ListClientOrderSerializer

class SingleListClientOrderView(RetrieveAPIView):
	queryset = ClientOrder.objects.all()
	serializer_class = ListClientOrderSerializer

class SingleClientOrderView(RetrieveUpdateDestroyAPIView):
	queryset = ClientOrder.objects.all()
	serializer_class = ClientOrderSerializer


''' Пробую получить клиента по фамилии со своим блэкджеком и пр'''

@api_view(['GET'])
def current_rate(request):
	"""
		GET current rate RUB per one EUR
	"""
	if request.method == 'GET':
		current_rate = CurrentRate.objects.all().last()
		serializer = CurrentRateSerializer(current_rate)
		return Response(serializer.data)

class CurrentRateView(generics.ListCreateAPIView):
	queryset = CurrentRate.objects.all()
	serializer_class= CurrentRateSerializer

class SavedRateView(RetrieveAPIView):
	queryset = CurrentRate.objects.all()
	serializer_class = CurrentRateSerializer


@api_view(['POST'])
def check_client(request):
	"""
		GET a client if the client exist
	"""
	client = (request.data['name'].split(' '))
	last_name = first_name = ''

	if client[0] == '':
		return Response(status=status.HTTP_400_BAD_REQUEST)
	elif len(client) == 1:
		found_client = Client.objects.filter(first_name=client[0].title()).first()
		if found_client == None:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		serializer = ClientSerializer(found_client)
		return Response(serializer.data)
	elif len(client) == 2:
		found_client = Client.objects.filter(first_name=client[0].title()).filter(last_name=client[1].title()).first()
		serializer = ClientSerializer(found_client)
		return Response(serializer.data)
	elif len(client) == 3:
		found_client = Client.objects.filter(first_name=client[0].title()).filter(middle_name=client[1].title()).filter(last_name=client[2].title()).first()
		serializer = ClientSerializer(found_client)
		return Response(serializer.data)
	elif len(client) > 3:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def client_order_add(request):
	"""
		first generate a uniq number for the order, then save a client order 
	"""

	def get_public_number():
		now = datetime.now()

		last_order = ClientOrder.objects.last()

		if last_order == None or int(last_order.public_num.split("-")[0]) != now.year:
			new_public_num = str(now.year) + "-" + "%04d" % (1)
			return new_public_num

		elif int(last_order.public_num.split("-")[0]) == now.year:
			new_public_num = str(now.year) + "-" + "%04d" % (int(last_order.public_num.split("-")[1])+1)
			return new_public_num

	data = JSONParser().parse(request)
	data['public_num'] = get_public_number()
	serializer = ClientOrderSerializer(data=data)
	# serializer.is_valid()
	# print(serializer.errors)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	else:
		return JsonResponse(serializer.errors, status=400)
	# print(data)

	# return Response(status=status.HTTP_200_OK)