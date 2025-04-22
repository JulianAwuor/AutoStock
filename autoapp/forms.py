from django import forms
from autoapp.models import Stock,Supplier,EmployeeProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class EmployeeRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=50)
    nationalid = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create or update the EmployeeProfile
            profile, created = EmployeeProfile.objects.get_or_create(user=user)
            profile.email = self.cleaned_data['email']
            profile.phone = self.cleaned_data['phone']
            profile.nationalid = self.cleaned_data['nationalid']
            profile.save()

        return user