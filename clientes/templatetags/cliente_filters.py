from django import template

register = template.Library()


@register.filter
def whatsapp(value):
    """Convierte un teléfono paraguayo a formato internacional para wa.me: 0981-123456 → 595981123456"""
    digits = ''.join(c for c in str(value) if c.isdigit())
    if digits.startswith('0'):
        digits = '595' + digits[1:]
    elif not digits.startswith('595'):
        digits = '595' + digits
    return digits
