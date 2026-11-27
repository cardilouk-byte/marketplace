from django.contrib import admin
from .models import FAQ, BlogPost, ContactMessage

admin.site.register(FAQ)
admin.site.register(BlogPost)
admin.site.register(ContactMessage)
