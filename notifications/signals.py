from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from payments.models import Payment
from .services import notify_user


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created and instance.client:
        notify_user(
            instance.client,
            "Komand resevwa",
            f"Komand #{instance.order_number} anrejistre. Total: {instance.total_amount} HTG.",
            'order',
            email=True,
        )


@receiver(post_save, sender=Payment)
def payment_updated(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed' and instance.order.client:
        notify_user(
            instance.order.client,
            "Peman konfime",
            f"Peman #{instance.pk} pou komand #{instance.order.order_number} konfime.",
            'payment',
            email=True,
        )
