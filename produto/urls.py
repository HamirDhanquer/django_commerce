from django.urls import path
from . import views

app_name = 'produto'

urlspatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProdutos.as_view(), name='detalhe'),
    path('adicionarcarrinho', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
]