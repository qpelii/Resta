from django.contrib import admin
from .models import Category, Color, Product, ProductImage, Wishlist, Review, Coupon

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount_percent", "stock", "is_active", "is_best_seller")
    list_filter = ("category", "is_active", "is_best_seller", "is_new")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Coupon)