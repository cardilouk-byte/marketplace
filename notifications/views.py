from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required
def notifications_list(request):
    notifs = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/list.html', {'notifications': notifs})


@login_required
def mark_read(request, pk):
    n = Notification.objects.filter(pk=pk, user=request.user).first()
    if n:
        n.is_read = True
        n.save()
    return redirect('notifications:list')


@login_required
def unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})
