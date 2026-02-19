from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'vehicle_model', 'category', 'price', 'discount_price', 'stock_quantity', 'image', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RX100 Piston Kit'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. PK-RX100-01'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Yamaha RX100'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
