from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User




# Create your models here.
class Stock(models.Model):
     product = models. CharField(max_length=100)
     quantity = models.IntegerField()
     price = models.DecimalField(max_digits=12, decimal_places=2)
     buyingprice = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
     name = models.CharField(max_length=100)
     date = models.DateField(auto_now_add=True)

     def __str__(self):
         return self.product


class Supplier(models.Model):
     fullname = models.CharField(max_length=100)
     email = models.EmailField()
     contact = models.CharField(max_length=50)
     productname = models.CharField(max_length=100)

     def __str__(self):
          return self.fullname



class SaleTransaction(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction #{self.id} by {self.employee.username} on {self.date.strftime('%Y-%m-%d')}"

    @property
    def total_amount(self):
        total = sum(sale.total_sale for sale in self.sales.all())
        return (total + self.tax) - self.discount




class Sale(models.Model):
    transaction = models.ForeignKey(
        SaleTransaction,
        on_delete=models.CASCADE,
        related_name='sales',
        null=True,   # allow NULL in database
        blank=True   # allow blank in forms/admin
    )
    product = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='sales')
    quantitysold = models.PositiveIntegerField()
    sellingprice = models.DecimalField(max_digits=12, decimal_places=2)
    datesold = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product} - {self.quantitysold} sold"

    @property
    def total_sale(self):
        return self.quantitysold * self.sellingprice

    @property
    def profit(self):
        if hasattr(self.product, 'buyingprice'):
            return self.quantitysold * (self.sellingprice - self.product.buyingprice)
        return Decimal(0)


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ('boss', 'Boss'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nationalid = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(default='temp@example.com')  # temp default
    phone = models.CharField(max_length=50, default='0000000000')
    password = models.CharField(max_length=100, default='password123')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')  # added role field

    def __str__(self):
        return self.user.username





class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} @ {self.timestamp}"





