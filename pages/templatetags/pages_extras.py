from django import template
from pages.models import PageModel

register = template.Library()

@register.simple_tag
def get_page_list():
    pages = PageModel.objects.all()
    return pages