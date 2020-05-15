from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

from orders.models import Client, ClientOrder

class ClientOrdersListView(ListView):
	queryset = ClientOrder.objects.all()
	context_object_name = "client_orders"
	template = "orders/list.html"

def json_list_client_order(request):
	orders = ClientOrder.objects.all()

	return JsonResponse({
		# "orders":[p.public_num for p in orders],
		"orders":[
		{
			"public_num": o.public_num,
			"state": o.state,
			"status": o.status,
		}
		for o in orders
		]
	}
	)



# class ClientOrdersListView(ListView):
# 	queryset = Client.objects.all()
# 	context_object_name = "client_orders"
# 	template = "orders/list.html"