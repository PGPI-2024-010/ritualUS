from django import template
from ritualUS.models import ProductType
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def categories_li_a():
    items = ProductType.objects.all()
    items_li_a = ""
    for i in items:
        items_li_a += f"""<li><a href="/products?category={i.id}">{i.name}</a></li>"""
    return mark_safe(items_li_a)

