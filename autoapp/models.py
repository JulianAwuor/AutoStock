from django.db import models

# Create your models here.
class Stock(models.Model):
     name = models. CharField(max_length=100)
     quantity = models.IntegerField()
     price = models.DecimalField(max_digits=12, decimal_places=2)
     product = models.CharField(max_length=100)
     date = models.DateField()

     def __str__(self):
         return self.name


class Supplier(models.Model):
     fullname = models.CharField(max_length=100)
     email = models.EmailField()
     contact = models.CharField(max_length=50)
     productname = models.CharField(max_length=100)

     def __str__(self):
          return self.fullname
