from django import forms
from autoapp.models import Stock,Supplier


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

