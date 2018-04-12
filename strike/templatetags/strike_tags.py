from django import template


register = template.Library()


@register.simple_tag
def get_list(l):
    """
    Convert list to string.
    """
    if len(l) > 0 and l[0] is not None:
        return ', '.join(l)
    return ''
