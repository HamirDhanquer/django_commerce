from distutils.command.upload import upload
from pickletools import optimize
from django.db import models
import os 
from django.conf import settings
from PIL import Image
from django.utils.text import slugify

"""
    Produto:
        Produto:
            nome - Char
            descricao_curta - Text
            descricao_longa - Text
            imagem - Image
            slug - Slug
            preco_marketing - Float
            preco_marketing_promocional - Float
            tipo - Choices
                ('V', 'Variável'),
                ('S', 'Simples'),
"""
class Produto(models.Model):

    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m',blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Promoção')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V','Variação'),
            ('S','Simples'),
        )
    )
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.',',')
    get_preco_formatado.short_description = 'Preço'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pill = Image.open(img_full_path)
        original_width, original_height = img_pill.size

        if original_width <= new_width:
            print('Largura original menor que nova largura')
            img_pill.close()
            return 
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pill.resize((new_width,new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        print("Imagem foi redimensionada")

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
            super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome



"""

        Variacao:
            nome - char
            produto - FK Produto
            preco - Float
            preco_promocional - Float
            estoque - Int
"""

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta: 
        verbose_name = "Variação"
        verbose_name_plural = "Variações"