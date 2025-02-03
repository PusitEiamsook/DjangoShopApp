from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Inventory(models.Model):
    productName = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    productImage = models.ImageField(default='product-placeholder.png', upload_to='productImages/')
    def __str__(self):
        return self.productName
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    def __str__(self):
        return str(self.id)

class Transaction(models.Model):
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shippingAddress = models.ForeignKey(Address, on_delete=models.CASCADE, default=None, blank=True, null=True)
    proofOfPayment = models.ImageField(default=None, blank=True, null=True, upload_to='proofOfPayment/')
    def __str__(self):
        return str(self.id)

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.user.username