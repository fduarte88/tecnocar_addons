from django import template

register = template.Library()


@register.filter
def guarani(value):
    """Formatea un número como Guaraní paraguayo: ₲ 1.500.000"""
    try:
        n = int(round(float(value)))
        formatted = f'{n:,}'.replace(',', '.')
        return f'₲ {formatted}'
    except (TypeError, ValueError):
        return '₲ 0'


@register.filter
def guarani_plain(value):
    """Número sin símbolo para usar en atributos JS: 1500000"""
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0
