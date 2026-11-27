from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from payments.models import Payment
from products.models import Product

DELIVERY_FEE = 500


def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'orders/cart.html', {'cart': cart, 'delivery_fee': DELIVERY_FEE})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1) or 1)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product,
                                                   defaults={'quantity': qty})
    if not created:
        item.quantity += qty
        item.save()
    messages.success(request, f"{product.name} ajoute nan panier ou.")
    return redirect('orders:cart')


def update_item(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get('quantity', 1) or 1)
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('orders:cart')


def remove_item(request, item_id):
    cart = _get_cart(request)
    get_object_or_404(CartItem, pk=item_id, cart=cart).delete()
    return redirect('orders:cart')


def checkout(request):
    cart = _get_cart(request)
    items = list(cart.items.select_related('product'))
    if not items:
        messages.info(request, "Panier ou vid.")
        return redirect('products:list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total = sum(i.subtotal for i in items) + DELIVERY_FEE
            order = form.save(commit=False)
            order.client = request.user if request.user.is_authenticated else None
            order.total_amount = total
            order.save()
            for i in items:
                OrderItem.objects.create(order=order, product=i.product,
                                         quantity=i.quantity, unit_price=i.product.price)
            Payment.objects.create(
                order=order,
                provider=form.cleaned_data['payment_method'],
                amount=total,
                status='pending',
            )
            cart.items.all().delete()
            messages.success(request, f"Komand #{order.order_number} kreye. Mesi!")
            return redirect('orders:confirmation', order.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'customer_name': request.user.get_full_name() or request.user.username,
                       'customer_email': request.user.email}
        form = CheckoutForm(initial=initial)
    return render(request, 'orders/checkout.html', {
        'cart': cart, 'items': items, 'form': form, 'delivery_fee': DELIVERY_FEE,
    })


def confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/confirmation.html', {'order': order})
