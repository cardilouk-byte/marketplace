from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
import json

from products.models import Product, Category
from orders.models import Order
from payments.models import Payment
from notifications.models import Notification
from builder.models import (
    SiteIdentity, Logo, ColorPalette, FontSetting, AnimationSetting,
    Theme, HeaderConfig, FooterConfig, SidebarConfig, MenuItem,
    ButtonStyle, CardStyle, Page as BuilderPage, MediaFile,
    Section, SliderSlide, DesignVersion,
)

from .forms import (
    ProductForm, CategoryForm, OrderForm, PaymentForm, NotificationForm,
    SiteIdentityForm, LogoForm, ColorPaletteForm, FontSettingForm,
    AnimationSettingForm, ThemeForm, HeaderConfigForm, FooterConfigForm,
    SidebarConfigForm, MenuItemForm, ButtonStyleForm, CardStyleForm,
    BuilderPageForm, MediaFileForm, SectionForm, SliderSlideForm,
    UserCreateForm, UserEditForm,
)


def _stats():
    return {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_revenue': Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or 0,
        'pending_payments': Payment.objects.filter(status='pending').count(),
        'unread_notifications': Notification.objects.filter(is_read=False).count(),
    }


@staff_member_required
def index(request):
    return render(request, 'dashboard/index.html', {
        'stats': _stats(),
        'recent_orders': Order.objects.order_by('-created_at')[:5],
        'recent_payments': Payment.objects.order_by('-created_at')[:5],
        'active': 'dashboard',
    })


# ================= PWODWI =================
@staff_member_required
def products_list(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.all().order_by('-created_at')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    return render(request, 'dashboard/products_list.html', {
        'products': products, 'query': q, 'active': 'products', 'stats': _stats(),
    })


@staff_member_required
def product_form(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Pwodwi sove.")
        return redirect('dashboard:products_list')
    return render(request, 'dashboard/product_form.html', {
        'form': form, 'product': product, 'active': 'products', 'stats': _stats(),
    })


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Pwodwi efase.")
    return redirect('dashboard:products_list')


# ================= KATEGORI =================
@staff_member_required
def categories_list(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Kategori ajoute.")
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/categories.html', {
        'categories': Category.objects.all().order_by('name'),
        'form': form, 'active': 'categories', 'stats': _stats(),
    })


@staff_member_required
def category_edit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=cat)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Kategori modifye.")
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/categories.html', {
        'categories': Category.objects.all(),
        'form': form, 'edit_obj': cat, 'active': 'categories', 'stats': _stats(),
    })


@staff_member_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, "Kategori efase.")
    return redirect('dashboard:categories_list')


# ================= KOMAND =================
@staff_member_required
def orders_list(request):
    q = request.GET.get('q', '').strip()
    orders = Order.objects.all().order_by('-created_at')
    if q:
        orders = orders.filter(Q(id__icontains=q) | Q(customer_name__icontains=q) |
                               Q(customer_phone__icontains=q))
    return render(request, 'dashboard/orders_list.html', {
        'orders': orders, 'query': q, 'active': 'orders', 'stats': _stats(),
    })


@staff_member_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Komand modifye.")
        return redirect('dashboard:orders_list')
    return render(request, 'dashboard/order_form.html', {
        'form': form, 'order': order, 'active': 'orders', 'stats': _stats(),
    })


@staff_member_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Komand efase.")
    return redirect('dashboard:orders_list')


# ================= PEMAN =================
@staff_member_required
def payments_list(request):
    return render(request, 'dashboard/payments_list.html', {
        'payments': Payment.objects.all().order_by('-created_at'),
        'active': 'payments', 'stats': _stats(),
    })


@staff_member_required
def payment_edit(request, pk):
    p = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, request.FILES or None, instance=p)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Peman modifye.")
        return redirect('dashboard:payments_list')
    return render(request, 'dashboard/payment_form.html', {
        'form': form, 'payment': p, 'active': 'payments', 'stats': _stats(),
    })


@staff_member_required
def payment_delete(request, pk):
    p = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        p.delete()
        messages.success(request, "Peman efase.")
    return redirect('dashboard:payments_list')


@staff_member_required
def payment_confirm(request, pk):
    p = get_object_or_404(Payment, pk=pk)
    p.status = 'completed'
    p.confirmed_at = timezone.now()
    p.save()
    p.order.status = 'paid'
    p.order.save()
    messages.success(request, "Peman konfime.")
    return redirect('dashboard:payments_list')


# ================= KONFIGIRASYON =================
@staff_member_required
def config_general(request):
    obj = SiteIdentity.objects.first() or SiteIdentity()
    form = SiteIdentityForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Konfigirasyon jeneral sove.")
        return redirect('dashboard:config_general')
    return render(request, 'dashboard/config/general.html', {
        'form': form, 'active': 'config_general', 'stats': _stats(),
    })


@staff_member_required
def config_identity(request):
    return config_general(request)


@staff_member_required
def config_logos(request):
    logos = Logo.objects.all()
    form = LogoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Logo ajoute.")
        return redirect('dashboard:config_logos')
    return render(request, 'dashboard/config/logos.html', {
        'logos': logos, 'form': form, 'active': 'config_logos', 'stats': _stats(),
    })


@staff_member_required
def logo_delete(request, pk):
    obj = get_object_or_404(Logo, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Logo efase.")
    return redirect('dashboard:config_logos')


@staff_member_required
def config_colors(request):
    obj = ColorPalette.objects.filter(is_active=True).first() or ColorPalette()
    form = ColorPaletteForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Koule sove.")
        return redirect('dashboard:config_colors')
    return render(request, 'dashboard/config/colors.html', {
        'form': form, 'active': 'config_colors', 'stats': _stats(),
    })


@staff_member_required
def config_fonts(request):
    obj = FontSetting.objects.filter(is_active=True).first() or FontSetting()
    form = FontSettingForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Polis sove.")
        return redirect('dashboard:config_fonts')
    return render(request, 'dashboard/config/fonts.html', {
        'form': form, 'active': 'config_fonts', 'stats': _stats(),
    })


@staff_member_required
def config_animations(request):
    obj = AnimationSetting.objects.filter(is_active=True).first() or AnimationSetting()
    form = AnimationSettingForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Animasyon sove.")
        return redirect('dashboard:config_animations')
    return render(request, 'dashboard/config/animations.html', {
        'form': form, 'active': 'config_animations', 'stats': _stats(),
    })


@staff_member_required
def config_themes(request):
    themes = Theme.objects.all()
    form = ThemeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Tem ajoute.")
        return redirect('dashboard:config_themes')
    return render(request, 'dashboard/config/themes.html', {
        'themes': themes, 'form': form, 'active': 'config_themes', 'stats': _stats(),
    })


@staff_member_required
def theme_delete(request, pk):
    obj = get_object_or_404(Theme, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Tem efase.")
    return redirect('dashboard:config_themes')


@staff_member_required
def config_models(request):
    return render(request, 'dashboard/config/models.html', {
        'models': Theme.MODEL_CHOICES, 'active': 'config_models', 'stats': _stats(),
    })


@staff_member_required
def config_header(request):
    obj = HeaderConfig.objects.first() or HeaderConfig()
    form = HeaderConfigForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Header sove.")
        return redirect('dashboard:config_header')
    return render(request, 'dashboard/config/header_builder.html', {
        'form': form, 'active': 'config_header', 'stats': _stats(),
    })


@staff_member_required
def config_footer(request):
    obj = FooterConfig.objects.first() or FooterConfig()
    form = FooterConfigForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Footer sove.")
        return redirect('dashboard:config_footer')
    return render(request, 'dashboard/config/footer_builder.html', {
        'form': form, 'active': 'config_footer', 'stats': _stats(),
    })


@staff_member_required
def config_sidebar(request):
    obj = SidebarConfig.objects.first() or SidebarConfig()
    form = SidebarConfigForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Sidebar sove.")
        return redirect('dashboard:config_sidebar')
    return render(request, 'dashboard/config/sidebar_builder.html', {
        'form': form, 'active': 'config_sidebar', 'stats': _stats(),
    })


@staff_member_required
def config_homepage(request):
    sections = Section.objects.all().order_by('order')
    return render(request, 'dashboard/config/homepage_builder.html', {
        'sections': sections, 'active': 'config_homepage', 'stats': _stats(),
    })


@staff_member_required
def section_add(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Seksyon ajoute.")
        return redirect('dashboard:config_homepage')
    return render(request, 'dashboard/config/section_editor.html', {
        'form': form, 'active': 'config_homepage', 'stats': _stats(),
    })


@staff_member_required
def section_edit(request, pk):
    obj = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Seksyon modifye.")
        return redirect('dashboard:config_homepage')
    return render(request, 'dashboard/config/section_editor.html', {
        'form': form, 'section': obj, 'active': 'config_homepage', 'stats': _stats(),
    })


@staff_member_required
def section_delete(request, pk):
    obj = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Seksyon efase.")
    return redirect('dashboard:config_homepage')


@staff_member_required
def config_hero(request):
    return redirect('dashboard:config_sections')


@staff_member_required
def config_slider(request):
    slides = SliderSlide.objects.all().order_by('order')
    form = SliderSlideForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Slide ajoute.")
        return redirect('dashboard:config_slider')
    return render(request, 'dashboard/config/slider_builder.html', {
        'slides': slides, 'form': form, 'active': 'config_slider', 'stats': _stats(),
    })


@staff_member_required
def slide_edit(request, pk):
    obj = get_object_or_404(SliderSlide, pk=pk)
    form = SliderSlideForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Slide modifye.")
        return redirect('dashboard:config_slider')
    return render(request, 'dashboard/config/slider_form.html', {
        'form': form, 'slide': obj, 'active': 'config_slider', 'stats': _stats(),
    })


@staff_member_required
def slide_delete(request, pk):
    obj = get_object_or_404(SliderSlide, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Slide efase.")
    return redirect('dashboard:config_slider')


@staff_member_required
def config_sections(request):
    return redirect('dashboard:config_homepage')


@staff_member_required
def config_buttons(request):
    buttons = ButtonStyle.objects.all()
    form = ButtonStyleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Bouton ajoute.")
        return redirect('dashboard:config_buttons')
    return render(request, 'dashboard/config/buttons.html', {
        'buttons': buttons, 'form': form, 'active': 'config_buttons', 'stats': _stats(),
    })


@staff_member_required
def button_edit(request, pk):
    obj = get_object_or_404(ButtonStyle, pk=pk)
    form = ButtonStyleForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Bouton modifye.")
        return redirect('dashboard:config_buttons')
    return render(request, 'dashboard/config/buttons.html', {
        'buttons': ButtonStyle.objects.all(), 'form': form, 'edit_obj': obj,
        'active': 'config_buttons', 'stats': _stats(),
    })


@staff_member_required
def button_delete(request, pk):
    obj = get_object_or_404(ButtonStyle, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Bouton efase.")
    return redirect('dashboard:config_buttons')


@staff_member_required
def config_cards(request):
    cards = CardStyle.objects.all()
    form = CardStyleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Kat ajoute.")
        return redirect('dashboard:config_cards')
    return render(request, 'dashboard/config/cards.html', {
        'cards': cards, 'form': form, 'active': 'config_cards', 'stats': _stats(),
    })


@staff_member_required
def card_delete(request, pk):
    obj = get_object_or_404(CardStyle, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Kat efase.")
    return redirect('dashboard:config_cards')


@staff_member_required
def config_menus(request):
    menu_items = MenuItem.objects.all().order_by('order')
    form = MenuItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Meni ajoute.")
        return redirect('dashboard:config_menus')
    return render(request, 'dashboard/config/menus.html', {
        'menu_items': menu_items, 'form': form, 'active': 'config_menus', 'stats': _stats(),
    })


@staff_member_required
def menu_edit(request, pk):
    obj = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Meni modifye.")
        return redirect('dashboard:config_menus')
    return render(request, 'dashboard/config/menus.html', {
        'menu_items': MenuItem.objects.all(), 'form': form, 'edit_obj': obj,
        'active': 'config_menus', 'stats': _stats(),
    })


@staff_member_required
def menu_delete(request, pk):
    obj = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Meni efase.")
    return redirect('dashboard:config_menus')


@staff_member_required
def config_pages(request):
    pages = BuilderPage.objects.all().order_by('-created_at')
    form = BuilderPageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Paj kreye.")
        return redirect('dashboard:config_pages')
    return render(request, 'dashboard/config/pages.html', {
        'pages': pages, 'form': form, 'active': 'config_pages', 'stats': _stats(),
    })


@staff_member_required
def page_edit(request, pk):
    obj = get_object_or_404(BuilderPage, pk=pk)
    form = BuilderPageForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Paj modifye.")
        return redirect('dashboard:config_pages')
    return render(request, 'dashboard/config/pages.html', {
        'pages': BuilderPage.objects.all(), 'form': form, 'edit_obj': obj,
        'active': 'config_pages', 'stats': _stats(),
    })


@staff_member_required
def page_delete(request, pk):
    obj = get_object_or_404(BuilderPage, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Paj efase.")
    return redirect('dashboard:config_pages')


@staff_member_required
def config_media(request):
    files = MediaFile.objects.all().order_by('-uploaded_at')
    form = MediaFileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Fichye ajoute.")
        return redirect('dashboard:config_media')
    return render(request, 'dashboard/config/media.html', {
        'files': files, 'form': form, 'active': 'config_media', 'stats': _stats(),
    })


@staff_member_required
def media_delete(request, pk):
    obj = get_object_or_404(MediaFile, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Fichye efase.")
    return redirect('dashboard:config_media')


@staff_member_required
def config_editor(request):
    return render(request, 'dashboard/config/word_editor.html', {
        'active': 'config_editor', 'stats': _stats(),
    })


@staff_member_required
def config_preview(request):
    return render(request, 'dashboard/config/preview.html', {
        'active': 'config_preview', 'stats': _stats(),
    })


@staff_member_required
def config_save(request):
    snapshot = {
        'identity': list(SiteIdentity.objects.values()),
        'colors': list(ColorPalette.objects.values()),
        'fonts': list(FontSetting.objects.values()),
        'sections': list(Section.objects.values()),
        'header': list(HeaderConfig.objects.values()),
        'footer': list(FooterConfig.objects.values()),
    }
    DesignVersion.objects.create(
        name=f"Version {timezone.now():%d/%m/%Y %H:%M}",
        snapshot=json.dumps(snapshot, default=str),
        created_by=request.user,
    )
    messages.success(request, "Design sove.")
    return redirect('dashboard:config_save')


@staff_member_required
def config_publish(request):
    DesignVersion.objects.update(is_published=False)
    latest = DesignVersion.objects.first()
    if latest:
        latest.is_published = True
        latest.save()
        messages.success(request, "Design publie.")
    return redirect('dashboard:config_publish')


@staff_member_required
def config_history(request):
    versions = DesignVersion.objects.all()
    return render(request, 'dashboard/config/history.html', {
        'versions': versions, 'active': 'config_history', 'stats': _stats(),
    })


@staff_member_required
def version_restore(request, pk):
    obj = get_object_or_404(DesignVersion, pk=pk)
    messages.info(request, f"Version {obj.name} restore (pa enplemante net).")
    return redirect('dashboard:config_history')


# ================= NOTIFIKASYON =================
@staff_member_required
def notifications_list(request):
    return render(request, 'dashboard/notifications_list.html', {
        'notifications': Notification.objects.all().order_by('-created_at'),
        'active': 'notifications', 'stats': _stats(),
    })


@staff_member_required
def notification_delete(request, pk):
    obj = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Notifikasyon efase.")
    return redirect('dashboard:notifications_list')


# ================= ITILIZATE =================
@staff_member_required
def users_list(request):
    return render(request, 'dashboard/users_list.html', {
        'users': User.objects.all().order_by('-date_joined'),
        'active': 'users', 'stats': _stats(),
    })


@staff_member_required
def user_add(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Itilizate ajoute.")
        return redirect('dashboard:users_list')
    return render(request, 'dashboard/user_form.html', {
        'form': form, 'active': 'users', 'stats': _stats(),
    })


@staff_member_required
def user_edit(request, pk):
    obj = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Itilizate modifye.")
        return redirect('dashboard:users_list')
    return render(request, 'dashboard/user_form.html', {
        'form': form, 'user_obj': obj, 'active': 'users', 'stats': _stats(),
    })


@staff_member_required
def user_delete(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and obj != request.user:
        obj.delete()
        messages.success(request, "Itilizate efase.")
    return redirect('dashboard:users_list')


# ================= RAPO =================
@staff_member_required
def reports(request):
    sales = (Payment.objects.filter(status='completed')
             .annotate(month=TruncMonth('created_at'))
             .values('month').annotate(total=Sum('amount')).order_by('month'))
    return render(request, 'dashboard/reports.html', {
        'sales': sales, 'active': 'reports', 'stats': _stats(),
    })


# ================= BACKUP =================
@staff_member_required
def backups(request):
    return render(request, 'dashboard/backups.html', {
        'active': 'backups', 'stats': _stats(),
    })
