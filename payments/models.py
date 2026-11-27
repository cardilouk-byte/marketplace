from django.db import models
from orders.models import Order


class Payment(models.Model):
    PROVIDER_CHOICES = (
        ('moncash', 'MonCash'),
        ('natcash', 'NatCash'),
        ('card', 'Kat banke'),
        ('cash', 'Lajan kach'),
    )
    STATUS_CHOICES = (
        ('pending', 'An atant'),
        ('completed', 'Konfime'),
        ('failed', 'Echwe'),
        ('refunded', 'Rembourese'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='moncash')
    reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Peman #{self.pk} - {self.order.order_number} - {self.amount} HTG"
