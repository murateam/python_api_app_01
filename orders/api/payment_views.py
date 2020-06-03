from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Payment
from orders.api.payment_serializers import PaymentSerializer

class ListPaymentView(ListCreateAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

class SinglePaymentView(RetrieveUpdateDestroyAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer