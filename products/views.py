from django.shortcuts import render
from .models import ShopProduct, Product, Image
from django.views.generic import ListView, DetailView
# Create your views here.

class ProductSingle(DetailView):
    model = Product
    template_name = 'components/product-single.html'

    def get_context_data(self, **kwargs):
        context = super(ProductSingle, self).get_context_data(**kwargs)
        product = context.get('product', None)
        context['seller'] = ShopProduct.objects.filter(product=product).first()
        context['images'] = Image.objects.filter(product=product)
        print(context['images'])
        return context
    