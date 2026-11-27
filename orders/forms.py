from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ('moncash', 'MonCash'),
        ('natcash', 'NatCash'),
        ('card', 'Kat banke'),
        ('cash', 'Peman adisyon livrezon'),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect,
                                       initial='moncash', label='Metod peman')

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address']
        widgets = {
            'customer_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'customer_name': 'Non konple',
            'customer_phone': 'Teles',
            'customer_email': 'Imel',
            'customer_address': 'Adres livrezon',
        }
