from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    TYPE_CHOICES = (
        ('order', 'Komand'),
        ('payment', 'Peman'),
        ('info', 'Enfomasyon'),
        ('stock', 'Stock'),
        ('message', 'Mesaj'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_pref')
    email_order = models.BooleanField(default=True)
    email_payment = models.BooleanField(default=True)
    email_promo = models.BooleanField(default=False)
    sms_order = models.BooleanField(default=False)
    sms_payment = models.BooleanField(default=False)

    def __str__(self):
        return f"Pref {self.user.username}"
