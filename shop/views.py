from django.shortcuts import render
from .models import Product, Category


def home(request):
    """صفحه اصلی سایت رستا"""

    categories = Category.objects.filter(
        is_active=True,
        parent=None,
    ).order_by("order")

    best_sellers = Product.objects.filter(
        is_active=True,
        is_best_seller=True,
    ).select_related("category")[:3]

    context = {
        "categories": categories,
        "best_sellers": best_sellers,
    }
    return render(request, "shop/home.html", context)

def about(request):
    return render(request, "shop/about.html")

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "shop/category_detail.html", context)

def product_detail(request, slug):
    """
    صفحه‌ی جزئیات محصول.
    - گالری تصاویر
    - رنگ‌های موجود
    - محصولات مشابه (همون دسته)
    - نظرات
    """
    product = get_object_or_404(
        Product.objects
            .select_related("category")
            .prefetch_related("images", "colors", "reviews__user"),
        slug=slug,
        is_active=True,
    )
    
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True,
    ).exclude(pk=product.pk)[:4]
    
    reviews = product.reviews.all()
    rating_stats = reviews.aggregate(
        avg=Avg("rating"),
        count=Count("id"),
    )
    
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = product.wishlisted_by.filter(user=request.user).exists()
    
    context = {
        "product": product,
        "similar_products": similar_products,
        "reviews": reviews,
        "avg_rating": rating_stats["avg"] or 0,
        "review_count": rating_stats["count"],
        "user_review": user_review,
        "in_wishlist": in_wishlist,
    }
    return render(request, "shop/product_detail.html", context)
