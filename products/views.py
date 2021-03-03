from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
        context['categories'] = Category.objects.filter(parent__isnull=True)
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
        filter_value = self.request.GET.get('filter', 'Nothing')
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        self.kwargs['category'] = category
        return category.get_products(filter_value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = list()
        for product in context['product_list']:
            brands.append(product.brand)
        context['brands'] = set(brands)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context


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
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context

def search_page(request):
    srh = request.GET['search']
    products = Product.objects.filter(Q(name__icontains=srh) | Q(category__name__icontains=srh) | Q(category__parent__name__icontains=srh))
    brands = set()
    for product in products:
            brands.add(product.brand)
    params = {'products': products, 'search':srh, 'brands':brands}
    return render(request, 'components/search-page.html', params)
