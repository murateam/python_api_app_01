from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Payment, ClientOrder
from orders.api.payment_serializers import PaymentSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view


class ListPaymentView(ListCreateAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

class SinglePaymentView(RetrieveUpdateDestroyAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

@api_view(['GET'])
def get_list_payments_for_client_order(request, pk):
	client_order = ClientOrder.objects.get(pk=pk)
	payments = client_order.payments.all()

	serializer = PaymentSerializer(payments, many=True)
	return Response(serializer.data)