from django import forms
from django.contrib.auth.models import User
from products.models import Product, Category
from orders.models import Order, OrderItem
from payments.models import Payment
from notifications.models import Notification
from builder.models import (
    SiteIdentity, Logo, ColorPalette, FontSetting, AnimationSetting,
    Theme, HeaderConfig, FooterConfig, SidebarConfig, MenuItem,
    ButtonStyle, CardStyle, Page as BuilderPage, MediaFile,
    Section, SliderSlide, DesignVersion,
)


# ===== PWODWI =====
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock', 'image', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']


# ===== KOMAND =====
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_address', 'status', 'total_amount']
        widgets = {'customer_address': forms.Textarea(attrs={'rows': 3})}


# ===== PEMAN =====
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['provider', 'reference', 'amount', 'status', 'proof']


# ===== NOTIFIKASYON =====
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'type', 'title', 'message', 'is_read']
        widgets = {'message': forms.Textarea(attrs={'rows': 3})}


# ===== KONFIGIRASYON =====
class SiteIdentityForm(forms.ModelForm):
    class Meta:
        model = SiteIdentity
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['name', 'type', 'image', 'is_active']


class ColorPaletteForm(forms.ModelForm):
    class Meta:
        model = ColorPalette
        fields = '__all__'
        widgets = {f: forms.TextInput(attrs={'type': 'color'})
                   for f in ['primary', 'secondary', 'accent', 'background', 'text']}


class FontSettingForm(forms.ModelForm):
    class Meta:
        model = FontSetting
        fields = '__all__'


class AnimationSettingForm(forms.ModelForm):
    class Meta:
        model = AnimationSetting
        fields = '__all__'


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = '__all__'


class HeaderConfigForm(forms.ModelForm):
    class Meta:
        model = HeaderConfig
        fields = '__all__'
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
        }


class FooterConfigForm(forms.ModelForm):
    class Meta:
        model = FooterConfig
        fields = '__all__'
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
        }


class SidebarConfigForm(forms.ModelForm):
    class Meta:
        model = SidebarConfig
        fields = '__all__'


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'


class ButtonStyleForm(forms.ModelForm):
    class Meta:
        model = ButtonStyle
        fields = '__all__'
        widgets = {
            'bg_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'hover_bg_color': forms.TextInput(attrs={'type': 'color'}),
        }


class CardStyleForm(forms.ModelForm):
    class Meta:
        model = CardStyle
        fields = '__all__'
        widgets = {'bg_color': forms.TextInput(attrs={'type': 'color'})}


class BuilderPageForm(forms.ModelForm):
    class Meta:
        model = BuilderPage
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
        }


class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'subtitle': forms.Textarea(attrs={'rows': 3}),
            'config_json': forms.Textarea(attrs={'rows': 4}),
        }


class SliderSlideForm(forms.ModelForm):
    class Meta:
        model = SliderSlide
        fields = '__all__'


# ===== ITILIZATE =====
class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
