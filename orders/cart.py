from shop.models import Product

CART_SESSION_KEY = "cart"

def get_cart(request):
    raw_cart = request.session.get(CART_SESSION_KEY, {})
    items = []
    total = 0
    
    for product_id, quantity in raw_cart.items():
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            continue
        
        subtotal = product.final_price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal
    
    return {"items": items, "total": total}


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True