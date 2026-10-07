from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from accounts.models import Address
from shop.models import Coupon
from .cart import get_cart, clear_cart
from .models import Order, OrderItem


@login_required
def create_order(request):
    if request.method != "POST":
        return redirect("orders:checkout")
    cart = get_cart(request)
    if not cart["items"]:
        messages.error(request, "سبد خرید خالی است.")
        return redirect("shop:home")

    address_id = request.POST.get("address_id")
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    
    coupon = None
    coupon_code = request.POST.get("coupon_code", "").strip()
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, "کد تخفیف نامعتبر است.")
            return redirect("orders:checkout")
        
        if not coupon.is_valid(order_amount=cart["total"]):
            messages.error(request, "کد تخفیف معتبر نیست یا منقضی شده.")
            coupon = None  # یا return redirect
    
    total_amount = cart["total"]
    discount_amount = 0
    if coupon:
        discount_amount = coupon.calculate_discount(total_amount)
    
    shipping_cost = 0  # TODO: بر اساس پست حساب میشه بعدا
    final_amount = total_amount - discount_amount + shipping_cost
    
    with transaction.atomic():
        for item in cart["items"]:
            product = item["product"]
            if product.stock < item["quantity"]:
                messages.error(
                    request,
                    f"موجودی «{product.name}» کافی نیست. "
                    f"موجودی فعلی: {product.stock}"
                )
                return redirect("orders:checkout")
        
        order = Order.objects.create(
            user=request.user,
            status=Order.Status.PENDING,
            
            receiver_name=address.receiver_name,
            receiver_phone=address.receiver_phone,
            province=address.province,
            city=address.city,
            full_address=address.full_address,
            postal_code=address.postal_code,
            
            coupon=coupon,
            total_amount=total_amount,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            final_amount=final_amount,
        )
        
        for item in cart["items"]:
            product = item["product"]
            quantity = item["quantity"]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=product.final_price,
                final_amount=product.final_price * quantity,
            )
            
            from django.db.models import F
            Product.objects.filter(pk=product.pk).update(
                stock=F("stock") - quantity
            )
        
        if coupon:
            Coupon.objects.filter(pk=coupon.pk).update(
                used_count=F("used_count") + 1
            )
    
    clear_cart(request)
    
    return redirect("shop:home")#TODO: انتفال به درگاه