from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Payment, ClientOrder
from orders.api.payment_serializers import PaymentSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from rest_framework.parsers import JSONParser


class ListPaymentView(ListCreateAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

class SinglePaymentView(RetrieveUpdateDestroyAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

@api_view(['POST'])
def save_payment(request):
	data = JSONParser().parse(request)
	convert_to_date = datetime.strptime(data['payment_date'], "%Y-%m-%d").date()

	dt = datetime.combine(convert_to_date, datetime.min.time())
	data['payment_date'] = dt

	if data['id'] != None:
		exist_payment = Payment.objects.get(pk=data['id'])
		serializer = PaymentSerializer(exist_payment, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)
	else:
		serializer = PaymentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)
	# return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_list_payments_for_client_order(request, pk):
	client_order = ClientOrder.objects.get(pk=pk)
	payments = client_order.payments.all()

	serializer = PaymentSerializer(payments, many=True)
	return Response(serializer.data)