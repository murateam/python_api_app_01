from django.urls import path

from orders.api.views import SavedRateView, CurrentRateView
from orders.api.views import ListClientView, SingleClientView
from orders.api.views import ListClientOrderView, SingleClientOrderView, SingleListClientOrderView
from orders.api.item_views import FactoryView, SingleFactoryView, FactoryCollectionView, SingleFactoryCollectionView
from orders.api.item_views import ListFactoryItemView, SingleFactoryItemView
from orders.api.item_views import ListStockItemView#, StockItemView
from orders.api.payment_views import ListPaymentView, SinglePaymentView
from orders.api import views as api_views
from orders.api import item_views



app_name = "orders"

urlpatterns = [
	path('current_rate/', api_views.current_rate),
	path('create_current_rate/', CurrentRateView.as_view()),
	path('saved_rate/<int:pk>', SavedRateView.as_view()),

	path('clients/', ListClientView.as_view()),
	path('clients/<int:pk>', SingleClientView.as_view()),
	path('clients/check/', api_views.check_client),

	path('client_orders/', ListClientOrderView.as_view()),
	path('client_orders/for_list/<int:pk>', SingleListClientOrderView.as_view()),
	path('client_orders/<int:pk>', SingleClientOrderView.as_view()),
	path('client_order/add/', api_views.client_order_add),

	path('factories/', FactoryView.as_view()),
	path('factories/<int:pk>', SingleFactoryView.as_view()),
	path('factories/collections/', FactoryCollectionView.as_view()),
	path('factories/collections/<int:pk>', SingleFactoryCollectionView.as_view()),
	path('factories/items/', ListFactoryItemView.as_view()),
	path('factories/items/<int:pk>', SingleFactoryItemView.as_view()),

	path('stock_items/', ListStockItemView.as_view()),
	path('stock_items/client_order/', item_views.get_stock_items_for_client_order),
	path('stock_items/save_from_client_order/', item_views.save_stock_items_from_client_order),

	path('payments/', ListPaymentView.as_view()),
	path('payments/<int:pk>', SinglePaymentView.as_view()),
]