# filters_tags.py
import markdown2

from django import template
from django.utils.safestring import mark_safe


@register.filter('markdown')
def markdown_format(text):
    """Devuelve el texto markdown en HTML.

    Args:
        text str: Texto markdown
    Returns:
        str El markdown convertido en HTML.
    """
    return mark_safe(markdown2.markdown(text))