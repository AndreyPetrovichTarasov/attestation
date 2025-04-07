from django import forms
from .models import NetworkNode, Product


class NetworkNodeForm(forms.ModelForm):
    class Meta:
        model = NetworkNode
        exclude = ['created_at']


class ProductForm(forms.ModelForm):
    release_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'model', 'release_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
        }
