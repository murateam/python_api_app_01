from rest_framework import serializers
from orders.models import ImportOrder

class ImportOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = ImportOrder
		fields = [
			'id',
			'import_number',
			'created',
			'updated',
			'KW',
			'AB_num',
			'AB_file',
			'VAITEK_order',
			'VAITEK_payment',
			'bill',
			'TTN',
			'TRID',
			'amount_place',
			'volume',
			'weight',
			'container_num',
		]