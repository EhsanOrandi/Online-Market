from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from .models import ShopProduct, Product, Image, Category, Comment, ProductMeta
from accounts.models import Shop
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
        context['info'] = ProductMeta.objects.filter(product=product)
        context['comments'] = Comment.objects.filter(product=product)
        context['shops'] = ShopProduct.objects.filter(product=product)
        return context

class ProductsList(ListView):
    model = Product
    slug_url_kwargs = 'slug'
    template_name = 'components/category-products.html'

    def get_queryset(self):
        slug = self.kwargs.get(self.slug_url_kwargs)
        return Product.objects.filter(category__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = list()
        for product in context['product_list']:
            brands.append(product.brand)
        print(brands)
        context['brands'] = set(brands)
        return context


@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(
            product_id=data['product_id'], text=data['comment'], rate=5, user=user)
        response = {"comment_id": comment.id, "text": comment.text, "rate":comment.rate, "full_name": user.get_full_name()}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": 'error'}
        return HttpResponse(json.dumps(response), status=400)
    

class ShopDetails(DetailView):
    model = Shop
    template_name = 'components/shop-single.html'

    def get_context_data(self, **kwargs):
        context = super(ShopDetails, self).get_context_data(**kwargs)
        shop = context.get('shop', None)
        context["products"] = ShopProduct.objects.filter(shop=shop) 
        return context
    
