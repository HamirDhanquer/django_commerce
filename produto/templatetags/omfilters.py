from atexit import register
from django.template import Library
from utils import helpers


register = Library()

@register.filter
def formata_preco(val):
    return helpers.formata_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    return helpers.cart_total_qtd(carrinho)