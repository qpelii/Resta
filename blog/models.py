from django.db import models
from django.urls import reverse

from accounts.models import User


class Post(models.Model):
    # majale
    
    title = models.CharField(verbose_name="عنوان", max_length=250)
    slug = models.SlugField(verbose_name="اسلاگ", max_length=270, unique=True)
    excerpt = models.CharField(verbose_name="خلاصه", max_length=300)
    content = models.TextField(verbose_name="متن")
    image = models.ImageField(verbose_name="تصویر", upload_to="blog/", blank=True, null=True)
    author = models.ForeignKey(
        User,
        verbose_name="نویسنده",
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    published_at = models.DateTimeField(verbose_name="تاریخ انتشار", auto_now=True)

    class Meta:
        verbose_name = "پست مجله"
        verbose_name_plural = "پست‌های مجله"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])
