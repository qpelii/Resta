import uuid

from django.db import models

from accounts.models import Address, User
from shop.models import Coupon, Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        PAID = "paid", "پرداخت‌شده"
        PROCESSING = "processing", "در حال پردازش"
        SHIPPED = "shipped", "ارسال‌شده"
        DELIVERED = "delivered", "تحویل داده‌شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(
        User,
        verbose_name="کاربر",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    order_number = models.CharField(
        verbose_name="شماره سفارش",
        max_length=32,
        unique=True,
        editable=False,
    )
    status = models.CharField(
        verbose_name="وضعیت سفارش",
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )

    shipping_address = models.ForeignKey(
        Address,
        verbose_name="آدرس ارسال",
        on_delete=models.PROTECT,
        related_name="orders",
        null=False,
        blank=False,
    )
    coupon = models.ForeignKey(
        Coupon,
        verbose_name="کد تخفیف استفاده‌شده",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )

    total_amount = models.PositiveIntegerField(
        verbose_name="مبلغ کل", help_text="جمع قیمت آیتم‌ها پیش از تخفیف"
    )
    discount_amount = models.PositiveIntegerField(verbose_name="مبلغ تخفیف", default=0)
    shipping_cost = models.PositiveIntegerField(verbose_name="هزینه ارسال", default=0)
    final_amount = models.PositiveIntegerField(verbose_name="مبلغ نهایی")

    created_at = models.DateTimeField(verbose_name="تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"RS-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    یک ردیف از سفارش (یک محصول با تعدادش).
    """

    order = models.ForeignKey(
        Order,
        verbose_name="سفارش",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="محصول",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    product_name_snapshot = models.CharField(
        verbose_name="نام محصول (در زمان خرید)",
        max_length=200,
        editable=False,
    )
    quantity = models.PositiveIntegerField(verbose_name="تعداد", default=1)
    price_at_purchase = models.PositiveIntegerField(
        verbose_name="قیمت محصول در زمان خرید (تومان)"
    )
    final_amount = models.PositiveIntegerField(
        verbose_name="مبلغ نهایی این آیتم",
        help_text="price_at_purchase × quantity",
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.product_name_snapshot} × {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.product_name_snapshot:
            self.product_name_snapshot = self.product.name
        if not self.final_amount:
            self.final_amount = self.price_at_purchase * self.quantity
        if not self.price_at_purchase:
            self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار"
        SUCCESS = "success", "موفق"
        FAILED = "failed", "ناموفق"

    order = models.ForeignKey(
        Order,
        verbose_name="سفارش",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.PositiveIntegerField(verbose_name="مبلغ")
    tracking_code = models.CharField(
        verbose_name="شماره پیگیری", max_length=100, blank=True
    )
    status = models.CharField(
        verbose_name="وضعیت پرداخت",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    gateway = models.CharField(
        verbose_name="درگاه پرداخت",
        max_length=50,
        help_text="مثال: زرین‌پال و ...",
    )
    paid_at = models.DateTimeField(verbose_name="تاریخ پرداخت", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"پرداخت {self.order.order_number} - {self.status} - {self.amount} تومان"
