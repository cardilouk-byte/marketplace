from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import SignUpForm, ProfileForm
from orders.models import Order
from payments.models import Payment


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('products:home')
    return render(request, 'accounts/signup.html', {'form': form})


def _client_stats(user, orders):
    total_spent = (Payment.objects.filter(status='completed', order__client=user)
                   .aggregate(t=Sum('amount'))['t'] or 0)
    return {
        'recent_orders': orders,
        'total_orders': Order.objects.filter(client=user).count(),
        'total_spent': total_spent,
        'total_favorites': 0,
    }


@login_required
def account_dashboard(request):
    return render(request, 'accounts/dashboard.html',
                  _client_stats(request.user, Order.objects.filter(client=request.user)[:5]))


@login_required
def my_orders(request):
    return render(request, 'accounts/dashboard.html',
                  _client_stats(request.user, Order.objects.filter(client=request.user)))


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})
