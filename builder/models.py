from django.db import models
from django.conf import settings


class SiteIdentity(models.Model):
    name = models.CharField(max_length=100, default='AgroShop')
    tagline = models.CharField(max_length=200, default='Achetez mieux, vivez mieux !')
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Identite sit'


class Logo(models.Model):
    TYPE_CHOICES = (('main', 'Prensipal'), ('favicon', 'Favicon'), ('footer', 'Footer'))
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='main')
    image = models.ImageField(upload_to='logos/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ColorPalette(models.Model):
    name = models.CharField(max_length=100, default='AgroShop Blue')
    primary = models.CharField(max_length=7, default='#1e40af')
    secondary = models.CharField(max_length=7, default='#f97316')
    accent = models.CharField(max_length=7, default='#fbbf24')
    background = models.CharField(max_length=7, default='#f5f7fb')
    text = models.CharField(max_length=7, default='#111111')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FontSetting(models.Model):
    name = models.CharField(max_length=100, default='Inter')
    font_family = models.CharField(max_length=100, default='Inter, system-ui, sans-serif')
    heading_font = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AnimationSetting(models.Model):
    name = models.CharField(max_length=100, default='Defo')
    animation_type = models.CharField(max_length=50, default='fade')
    duration = models.PositiveIntegerField(default=300)
    enable_animations = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    MODEL_CHOICES = (
        ('home', 'Paj Akey'),
        ('shop', 'Boutique'),
        ('product', 'Paj Pwodwi'),
        ('cart', 'Panier'),
        ('checkout', 'Checkout'),
        ('contact', 'Kontak'),
        ('faq', 'FAQ'),
        ('blog', 'Blog'),
    )
    name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=30, choices=MODEL_CHOICES, default='home')
    image = models.ImageField(upload_to='themes/', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class HeaderConfig(models.Model):
    sticky = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_cart = models.BooleanField(default=True)
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#1e40af')

    def __str__(self):
        return 'Header'

    class Meta:
        verbose_name_plural = 'Header config'


class FooterConfig(models.Model):
    about_text = models.TextField(blank=True)
    background_color = models.CharField(max_length=7, default='#1e293b')
    text_color = models.CharField(max_length=7, default='#ffffff')
    show_social = models.BooleanField(default=True)

    def __str__(self):
        return 'Footer'

    class Meta:
        verbose_name_plural = 'Footer config'


class SidebarConfig(models.Model):
    POSITION_CHOICES = (('left', 'Goch'), ('right', 'Dwat'), ('none', 'Pa gen'))
    show = models.BooleanField(default=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='left')

    def __str__(self):
        return 'Sidebar'


class MenuItem(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='children')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ButtonStyle(models.Model):
    name = models.CharField(max_length=100)
    bg_color = models.CharField(max_length=7, default='#1e40af')
    text_color = models.CharField(max_length=7, default='#ffffff')
    hover_bg_color = models.CharField(max_length=7, default='#f97316')
    border_radius = models.PositiveIntegerField(default=8)

    def __str__(self):
        return self.name


class CardStyle(models.Model):
    name = models.CharField(max_length=100)
    bg_color = models.CharField(max_length=7, default='#ffffff')
    border_radius = models.PositiveIntegerField(default=12)
    shadow = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    content = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MediaFile(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='media_library/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    TYPE_CHOICES = (
        ('hero', 'Hero / Slider'),
        ('categories', 'Kategori'),
        ('promo', 'Pwodwi an Pwomosyon'),
        ('new', 'Nouvo Pwodwi'),
        ('features', 'Avantaj (Livrezon, Sekirite...)'),
        ('testimonials', 'Temwanyaj'),
        ('newsletter', 'Newsletter'),
        ('custom', 'Koustom'),
    )
    name = models.CharField(max_length=100)
    section_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='hero')
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    config_json = models.TextField(blank=True, help_text='Konfigirasyon JSON')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.section_type})"


class SliderSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class DesignVersion(models.Model):
    name = models.CharField(max_length=200)
    snapshot = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
