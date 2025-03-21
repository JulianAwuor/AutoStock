from django.contrib import admin
from autoapp.models import Stock,Supplier,Sale

# Register your models here.
admin.site.register(Stock)
admin.site.register(Supplier)
admin.site.register(Sale)

