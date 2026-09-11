from django.shortcuts import render


def home(request):
    """صفحه اصلی سایت رستا"""

    categories = [
        {"name": "کیف دستی", "slug": "bags"},
        {"name": "کیف پول", "slug": "wallets"},
        {"name": "کمربند", "slug": "belts"},
        {"name": "دستکش", "slug": "blah"},
    ]

    best_sellers = [
        {
            "name": "کیف زنانه مدل مینا",
            "description": "کیف کراس‌بادی زنانه مینا؛ ترکیب طراحی شیک و استایل مدرن",
            "price": 4850000,
            "discount_percent": 15,
        },
        {
            "name": "کیف پول مردانه مدل آرکا",
            "description": "کیف پول چرم طبیعی با دوخت دستی و جای کارت فراوان",
            "price": 1950000,
            "discount_percent": 0,
        },
        {
            "name": "کمربند کلاسیک مدل سالار",
            "description": "کمربند چرم گاوی با سگک برنجی ضدزنگ",
            "price": 1250000,
            "discount_percent": 10,
        },
    ]

    context = {
        "categories": categories,
        "best_sellers": best_sellers,
    }
    return render(request, "shop/home.html", context)
