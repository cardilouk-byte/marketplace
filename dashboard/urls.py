from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),

    # Pwodwi
    path('products/', views.products_list, name='products_list'),
    path('products/add/', views.product_form, name='product_add'),
    path('products/<int:pk>/edit/', views.product_form, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Kategori
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.categories_list, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Komand
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # Peman
    path('payments/', views.payments_list, name='payments_list'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('payments/<int:pk>/confirm/', views.payment_confirm, name='payment_confirm'),

    # Konfigirasyon
    path('config/general/', views.config_general, name='config_general'),
    path('config/identity/', views.config_identity, name='config_identity'),
    path('config/logos/', views.config_logos, name='config_logos'),
    path('config/logos/<int:pk>/delete/', views.logo_delete, name='logo_delete'),
    path('config/colors/', views.config_colors, name='config_colors'),
    path('config/fonts/', views.config_fonts, name='config_fonts'),
    path('config/animations/', views.config_animations, name='config_animations'),
    path('config/themes/', views.config_themes, name='config_themes'),
    path('config/themes/<int:pk>/delete/', views.theme_delete, name='theme_delete'),
    path('config/models/', views.config_models, name='config_models'),
    path('config/header/', views.config_header, name='config_header'),
    path('config/footer/', views.config_footer, name='config_footer'),
    path('config/sidebar/', views.config_sidebar, name='config_sidebar'),
    path('config/homepage/', views.config_homepage, name='config_homepage'),
    path('config/sections/add/', views.section_add, name='section_add'),
    path('config/sections/<int:pk>/edit/', views.section_edit, name='section_edit'),
    path('config/sections/<int:pk>/delete/', views.section_delete, name='section_delete'),
    path('config/hero/', views.config_hero, name='config_hero'),
    path('config/slider/', views.config_slider, name='config_slider'),
    path('config/slider/<int:pk>/edit/', views.slide_edit, name='slide_edit'),
    path('config/slider/<int:pk>/delete/', views.slide_delete, name='slide_delete'),
    path('config/sections/', views.config_sections, name='config_sections'),
    path('config/buttons/', views.config_buttons, name='config_buttons'),
    path('config/buttons/<int:pk>/edit/', views.button_edit, name='button_edit'),
    path('config/buttons/<int:pk>/delete/', views.button_delete, name='button_delete'),
    path('config/cards/', views.config_cards, name='config_cards'),
    path('config/cards/<int:pk>/delete/', views.card_delete, name='card_delete'),
    path('config/menus/', views.config_menus, name='config_menus'),
    path('config/menus/<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('config/menus/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
    path('config/pages/', views.config_pages, name='config_pages'),
    path('config/pages/<int:pk>/edit/', views.page_edit, name='page_edit'),
    path('config/pages/<int:pk>/delete/', views.page_delete, name='page_delete'),
    path('config/media/', views.config_media, name='config_media'),
    path('config/media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    path('config/editor/', views.config_editor, name='config_editor'),
    path('config/preview/', views.config_preview, name='config_preview'),
    path('config/save/', views.config_save, name='config_save'),
    path('config/publish/', views.config_publish, name='config_publish'),
    path('config/history/', views.config_history, name='config_history'),
    path('config/history/<int:pk>/restore/', views.version_restore, name='version_restore'),

    # Notifikasyon
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/delete/', views.notification_delete, name='notification_delete'),

    # Itilizate
    path('users/', views.users_list, name='users_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Rapo
    path('reports/', views.reports, name='reports'),

    # Backup
    path('backups/', views.backups, name='backups'),
]
