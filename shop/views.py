from django.shortcuts import render
from .models import Product, Category


def home(request):
    """صفحه اصلی سایت رستا"""

    categories = Category.objects

    best_sellers = Product.objects.filter(is_best_seller=True)

    context = {
        "categories": categories,
        "best_sellers": best_sellers,
    }
    return render(request, "shop/home.html", context)

def about(request):
    return render(request, "shop/about.html")
