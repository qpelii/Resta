from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        "product",
        "product_name_snapshot",
        "price_at_purchase",
        "final_amount",
    )
    fields = ("product", "product_name_snapshot", "quantity", "price_at_purchase", "final_amount")


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ("amount", "tracking_code", "status", "gateway", "paid_at", "created_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "final_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__mobile", "user__email", "receiver_name")
    readonly_fields = (
        "order_number",
        "total_amount",
        "discount_amount",
        "final_amount",
        "created_at",
    )
    inlines = [OrderItemInline, PaymentInline]
    date_hierarchy = "created_at"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "status", "gateway", "paid_at")
    list_filter = ("status", "gateway")
    search_fields = ("order__order_number", "tracking_code")