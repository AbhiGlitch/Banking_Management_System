from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.full_name
class BankAccount(models.Model):
    ACCOUNT_TYPE =[
        ('savings', 'savings'),
        ('current', 'current'),
        
    ]        
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    balance =models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=10, default="0000000001")
    address = models.TextField(default="Not provided")
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
        ('credit', 'Credit'),
        ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"    

status = models.CharField(max_length=20, 
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ]
)
user = models.OneToOneField(User, on_delete=models.CASCADE)