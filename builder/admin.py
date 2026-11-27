from django.contrib import admin
from .models import (SiteIdentity, Logo, ColorPalette, FontSetting, AnimationSetting,
                     Theme, HeaderConfig, FooterConfig, SidebarConfig, MenuItem,
                     ButtonStyle, CardStyle, Page, MediaFile, Section, SliderSlide,
                     DesignVersion)

for m in [SiteIdentity, Logo, ColorPalette, FontSetting, AnimationSetting, Theme,
          HeaderConfig, FooterConfig, SidebarConfig, MenuItem, ButtonStyle, CardStyle,
          Page, MediaFile, Section, SliderSlide, DesignVersion]:
    admin.site.register(m)
