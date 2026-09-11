from django import template

register = template.Library()

_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"


def _to_persian_digits(value):
    return "".join(_PERSIAN_DIGITS[int(ch)] if ch.isdigit() else ch for ch in str(value))


@register.filter(name="to_persian_digits")
def to_persian_digits(value):
    """تبدیل اعداد لاتین به فارسی، مثلا 15 -> ۱۵"""
    return _to_persian_digits(value)


@register.filter(name="toman")
def toman(value):
    """قالب‌بندی قیمت با جداکننده هزارگان و اعداد فارسی، مثلا 4850000 -> ۴,۸۵۰,۰۰۰"""
    try:
        formatted = f"{int(value):,}"
    except (TypeError, ValueError):
        return value
    return _to_persian_digits(formatted)


@register.filter(name="apply_discount")
def apply_discount(value, percent):
    """محاسبه قیمت بعد از تخفیف"""
    try:
        value = int(value)
        percent = int(percent)
    except (TypeError, ValueError):
        return value
    return round(value * (100 - percent) / 100)
