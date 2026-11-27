from .models import Category


def site_context(request):
    """Kategori yo disponib nan tout template (nav ak footer)."""
    return {'nav_categories': Category.objects.all()[:6]}
