from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def notify_user(user, title, message, ntype='info', email=False):
    """Kreye yon notifikasyon nan app la epi voye imel si nesesè."""
    if user is None:
        return None
    notif = Notification.objects.create(user=user, title=title, message=message, type=ntype)
    if email and user.email:
        try:
            send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email],
                      fail_silently=True)
        except Exception:
            pass
    return notif


def notify_admins(title, message, ntype='info'):
    """Voye notifikasyon bay tout admin yo."""
    from django.contrib.auth.models import User
    for u in User.objects.filter(is_staff=True):
        notify_user(u, title, message, ntype)
