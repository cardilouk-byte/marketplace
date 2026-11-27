from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import FAQ, BlogPost, ContactMessage


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, "Mesaj ou voye. N ap reponn ou byento!")
        return redirect('cms:contact')
    return render(request, 'cms/contact.html')


def faq(request):
    return render(request, 'cms/faq.html', {'faqs': FAQ.objects.filter(is_active=True)})


def blog(request):
    return render(request, 'cms/blog.html', {'posts': BlogPost.objects.all()})


def blog_detail(request, slug):
    return render(request, 'cms/blog_detail.html', {
        'post': get_object_or_404(BlogPost, slug=slug),
    })
