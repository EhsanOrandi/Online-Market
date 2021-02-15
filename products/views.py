from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from .models import ShopProduct, Product, Image, Category, Comment, ProductMeta, Comment_like
from accounts.models import Shop
from django.views.generic import ListView, DetailView
from django.db.models import Q
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
        context['average_rate'] = product.average_rate
        context['comments_count'] = product.comments_count
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
        for item in context['product_list']:
            test = ShopProduct.objects.filter(product=item).first()
            print(test.price)
        brands = list()
        for product in context['product_list']:
            brands.append(product.brand)
        context['brands'] = set(brands)
        return context

# class ProductsListOrder(ProductsList):    
#     def get_queryset(self):
#         slug = self.kwargs.get(self.slug_url_kwargs)
#         test = set(Product.objects.filter(category__slug=slug))
#         print(test)
#         return Product.objects.filter(category__slug=slug).order_by('-shop_product__price')
    


@csrf_exempt
def likeComment(request):
    data = json.loads(request.body)
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse("No such comment found!", status=404)
    try:
        comment_like = Comment_like.objects.get(user=request.user, comment=comment)
        comment_like.status = data['status']
        comment_like.save()
    except Comment_like.DoesNotExist:
        Comment_like.objects.create(user=request.user, status=data['status'], comment=comment)

    result = {'like_count':comment.like_count}
    return HttpResponse(json.dumps(result), status=201)


@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(
            product_id=data['product_id'], text=data['comment'], rate=data['rate'], user=user)
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

def search_page(request):
    srh = request.GET['search']
    products = Product.objects.filter(Q(name__icontains=srh) | Q(category__name__icontains=srh) | Q(category__parent__name__icontains=srh))
    brands = set()
    for product in products:
            brands.add(product.brand)
    params = {'products': products, 'search':srh, 'brands':brands}
    return render(request, 'components/search-page.html', params)
