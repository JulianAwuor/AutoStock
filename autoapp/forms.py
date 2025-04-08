from django import forms
from autoapp.models import Stock,Supplier,UserProfile


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

