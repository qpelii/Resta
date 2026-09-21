"""
شامل: Category، Color، Product، ProductImage، Wishlist، Review، Coupon
"""

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse

from accounts.models import User


hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="کد رنگ باید به‌صورت هگز باشه، مثلاً #3A2418",
)


class Category(models.Model):
    """
    ساختار درختی (parent) تا بشه هم دسته‌های اصلی (کیف‌ها، کیف پول، اکسسوری،
    محصولات دیگر) و هم زیردسته‌ها (کیف دستی، کیف دوشی، ...) رو با یک مدل
    پوشش داد، بدون اینکه مجبور باشیم دو مدل جدا بسازیم.

    مثال:
        کیف‌ها (parent=None)
            کیف دستی (parent=کیف‌ها)
            کیف دوشی (parent=کیف‌ها)
    """

    name = models.CharField(verbose_name="نام دسته‌بندی", max_length=150)
    slug = models.SlugField(verbose_name="اسلاگ", max_length=170, unique=True)
    parent = models.ForeignKey(
        "self",
        verbose_name="دسته والد",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    order = models.PositiveIntegerField(verbose_name="ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} › {self.name}"
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category_detail", args=[self.slug])


class Color(models.Model):
    name = models.CharField(verbose_name="نام رنگ", max_length=60)
    hex_code = models.CharField(
        verbose_name="کد هگز",
        max_length=7,
        validators=[hex_color_validator],
        help_text="مثال: #3A2418",
    )

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.hex_code})"


class Product(models.Model):
    name = models.CharField(verbose_name="نام محصول", max_length=200)
    slug = models.SlugField(verbose_name="اسلاگ", max_length=220, unique=True)
    short_description = models.CharField(
        verbose_name="توضیحات کوتاه", max_length=300
    )
    full_description = models.TextField(verbose_name="توضیحات کامل", null=True , blank=True)

    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    discount_percent = models.PositiveIntegerField(
        verbose_name="درصد تخفیف",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    stock = models.PositiveIntegerField(verbose_name="موجودی", default=0)
    is_active = models.BooleanField(verbose_name="فعال", default=True)

    category = models.ForeignKey(
        Category,
        verbose_name="دسته‌بندی",
        on_delete=models.PROTECT,
        related_name="products",
    )
    material = models.CharField(
        verbose_name="جنس محصول",
        max_length=100,
        help_text="مثال: چرم طبیعی گاوی، چرم ساخت روسیه",
    )
    colors = models.ManyToManyField(
        Color,
        verbose_name="رنگ‌ها",
        blank=True,
        related_name="products",
    )
    
    specifications = models.JSONField(
        verbose_name="مشخصات محصول",
        default=dict,
        blank=True,
        help_text="به شکل json نوشته شود."
    )

    main_image = models.ImageField(verbose_name="تصویر اصلی", upload_to="products/")

    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    is_best_seller = models.BooleanField(verbose_name="پرفروش", default=False)
    is_new = models.BooleanField(verbose_name="جدید", default=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    @property
    def final_price(self):
        if self.discount_percent:
            return round(self.price * (100 - self.discount_percent) / 100)
        return self.price

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    """
    گالری تصاویر یک محصول
    """

    product = models.ForeignKey(
        Product,
        verbose_name="محصول",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(verbose_name="تصویر", upload_to="products/gallery/")
    order = models.PositiveIntegerField(verbose_name="ترتیب نمایش", default=0)
    is_main = models.BooleanField(verbose_name="تصویر اصلی", default=False)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
        ordering = ["order"]

    def __str__(self):
        return f"تصویر {self.order} - {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # برای وقتی که یک تصویر به عنوان تصویر اصلی انتخاب می‌شه، تصویر اصلی قبلی غیرفعال می‌شه
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(
                pk=self.pk
            ).update(is_main=False)
        super().save(*args, **kwargs)


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="کاربر",
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="محصول",
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} - {self.product}"


class Review(models.Model):
    """نظر و امتیاز مشتری برای یک محصول."""

    user = models.ForeignKey(
        User,
        verbose_name="کاربر",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="محصول",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="امتیاز",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(verbose_name="تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ["-created_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating}★)"


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "درصدی"
        FIXED = "fixed", "مبلغ ثابت"

    code = models.CharField(verbose_name="کد تخفیف", max_length=50, unique=True)
    discount_type = models.CharField(
        verbose_name="نوع تخفیف",
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
    )
    discount_value = models.PositiveIntegerField(
        verbose_name="مقدار تخفیف",
        help_text="اگر درصدی  ۱ تا ۱۰۰، اگر ثابت به تومان",
    )
    min_order_amount = models.PositiveIntegerField(
        verbose_name="حداقل مبلغ سفارش",
        null=True,
        blank=True,
        help_text="خالی بگذارید یعنی بدون لیمیت (تومان)",
    )
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    usage_limit = models.PositiveIntegerField(
        verbose_name="حداکثر تعداد استفاده",
        null=True,
        blank=True,
        help_text="خالی بگذارید یعنی نامحدود",
    )
    used_count = models.PositiveIntegerField(verbose_name="تعداد استفاده‌شده", default=0)
    is_active = models.BooleanField(verbose_name="فعال", default=True)

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.code}"

    def is_valid(self, order_amount=None):
        from django.utils import timezone

        now = timezone.now()
        if not self.is_active:
            return False
        if not (self.start_date <= now <= self.end_date):
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        if order_amount is not None and order_amount < self.min_order_amount:
            return False
        return True

    def calculate_discount(self, order_amount):
        discount=0
        if self.discount_type == self.DiscountType.FIXED:
            discount = self.discount_value
        elif self.discount_type == self.DiscountType.PERCENT:
            discount = round(order_amount * self.discount_value / 100)
        return min(discount, order_amount)
