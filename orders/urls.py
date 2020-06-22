from django.urls import path

from orders.api.views import SavedRateView, CurrentRateView
from orders.api.views import ListClientView, SingleClientView
from orders.api.views import ListClientOrderView, SingleClientOrderView, SingleListClientOrderView
from orders.api.item_views import FactoryView, SingleFactoryView
from orders.api.item_views import FactoryCollectionView, SingleFactoryCollectionView
from orders.api.item_views import ListFactoryItemView, SaveFactoryItemView, SingleFactoryItemView
from orders.api.item_views import ListStockItemView
from orders.api.item_views import ListNameFactoryView, ListNameFactoryCollectionView, ListNumberFactoryItemView
from orders.api.payment_views import ListPaymentView, SinglePaymentView
from orders.api.item_import_views import ListStockItemExpView, SingleStockItemExpView
from orders.api import views as api_views
from orders.api import item_views
from orders.api import payment_views
from orders.api.import_views import *

app_name = "orders"

urlpatterns = [
	path('current_rate/', api_views.current_rate),
	path('create_current_rate/', CurrentRateView.as_view()),
	path('saved_rate/<int:pk>', SavedRateView.as_view()),

	path('clients/', ListClientView.as_view()),
	path('clients/<int:pk>', SingleClientView.as_view()),
	path('clients/check/', api_views.check_client),
	path('clients/new', api_views.save_new_client), # save new client with convert birthDate to datetime

	path('client_orders/', ListClientOrderView.as_view()),
	path('client_orders/for_list/<int:pk>', SingleListClientOrderView.as_view()),
	path('client_orders/<int:pk>', SingleClientOrderView.as_view()),
	path('client_order/add/', api_views.client_order_add),
	path('client_order/to_import', api_views.client_order_to_import),

	path('factories/', FactoryView.as_view()),
	path('factories/<int:pk>', SingleFactoryView.as_view()),
	path('factories/list_names/', ListNameFactoryView.as_view()),

	path('factories/collections/', FactoryCollectionView.as_view()),
	path('factories/collections/<int:pk>', SingleFactoryCollectionView.as_view()),
	path('factories/collections/list_names/', item_views.list_name_factory_collections),

	path('factories/items/', ListFactoryItemView.as_view()),
	path('factories/items/<int:pk>', SingleFactoryItemView.as_view()),
	# path('factories/items/save/', SaveFactoryItemView.as_view()),
	path('factories/items/list_numbers/', item_views.list_catalogue_numbers),

	path('stock_items/', ListStockItemView.as_view()),
	path('stock_items/client_order/', item_views.get_stock_items_for_client_order),
	path('stock_items/save_from_client_order/', item_views.save_stock_items_from_client_order),
	path('stock_items/import/', ListStockItemExpView.as_view()),
	path('stock_items/import/<int:pk>', SingleStockItemExpView.as_view()),
	path('stock_items/import_order/<int:pk>', get_stock_items_by_import_order),


	path('payments/', ListPaymentView.as_view()),
	path('payments/<int:pk>', SinglePaymentView.as_view()),
	path('payments_for_order/<int:pk>', payment_views.get_list_payments_for_client_order),
	path('payments/save/', payment_views.save_payment),

	path('import_orders/', ListImportOrdersView.as_view()),
	path('import_orders/<int:pk>', SingleImportOrderView.as_view()),
	path('import_orders/save_new/', save_new_import_order),
]