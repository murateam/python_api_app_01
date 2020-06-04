from rest_framework import serializers
from orders.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = [
			'id',
			'created',
			'client_order',
			'payment_date',
			'payment_value',
			'comment',
		]
