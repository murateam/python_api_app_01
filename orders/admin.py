from django.contrib import admin
from orders.models import *

admin.site.register(Client)
admin.site.register(Factory)
admin.site.register(FactoryCollection)
admin.site.register(ClientOrder)
admin.site.register(OrderImage)
admin.site.register(Payment)
admin.site.register(Claim)
admin.site.register(ClaimImage)
admin.site.register(ImportOrder)
admin.site.register(FactoryItem)
admin.site.register(StockItem)
admin.site.register(AgreementExtra)
admin.site.register(AgreementImage)
admin.site.register(ImportImage)
admin.site.register(Movement)
admin.site.register(CurrentRate)

# admin.site.register(ImportItem)