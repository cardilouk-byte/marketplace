from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def home(request):
    return render(request, 'site/home.html', {
        'categories': Category.objects.all()[:6],
        'products': Product.objects.filter(is_active=True, old_price__isnull=False)[:4],
        'new_products': Product.objects.filter(is_active=True)[:8],
    })


def product_list(request):
    q = request.GET.get('q', '').strip()
    cat_slug = request.GET.get('categorie', '')
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    active_cat = None
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat_slug:
        active_cat = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=active_cat)
    return render(request, 'site/shop.html', {
        'products': products, 'categories': categories, 'query': q, 'active_cat': active_cat,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'site/product_detail.html', {
        'product': product,
        'related': Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4],
    })


def category_view(request, slug):
    return product_list(request)
