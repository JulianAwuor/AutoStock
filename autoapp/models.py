from django.db import models
from decimal import Decimal




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



class Sale(models.Model):
    product = models.ForeignKey(
        'Stock', on_delete=models.CASCADE, related_name="sales"
    )
    quantitysold = models.PositiveIntegerField()
    sellingprice = models.DecimalField(max_digits=12, decimal_places=2)
    datesold = models.DateField(auto_now_add=True)  # Automatically set on sale

    def __str__(self):
        return f"{self.product.product} - {self.quantitysold} sold"

    @property
    def total_sale(self):
        """Calculate total revenue from this sale."""
        return self.quantitysold * self.sellingprice

    @property
    def profit(self):
        """Calculate profit for this sale."""
        if hasattr(self.product, 'buyingprice'):
            return self.quantitysold * (self.sellingprice - self.product.buyingprice)
        return Decimal(0)  # If buying price is missing, return 0