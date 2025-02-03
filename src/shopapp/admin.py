from django.contrib import admin

# Register your models here.

from .models import Inventory, Address, Transaction, TransactionDetail, Cart

admin.site.register(Inventory)
admin.site.register(Address)
admin.site.register(Transaction)
admin.site.register(TransactionDetail)
admin.site.register(Cart)