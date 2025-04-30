from django.contrib import admin
from autoapp.models import Stock,Supplier,Sale,EmployeeProfile,ActivityLog,SaleTransaction

# Register your models here.
admin.site.register(Stock)
admin.site.register(Supplier)
admin.site.register(Sale)
admin.site.register(EmployeeProfile)
admin.site.register(ActivityLog)
admin.site.register(SaleTransaction)



