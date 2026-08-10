from django.contrib import admin
from . models import Customer, BankAccount, Transaction
admin.site.register(Customer)
admin.site.register(BankAccount)
admin.site.register(Transaction)
