from .models import Category


def mega_menu(request):
    main_categories = Category.objects.filter(
        is_active=True,
        parent=None,
    ).prefetch_related(
        "children__products",
    )
    
    return {
        "mega_menu_categories": main_categories,
    }