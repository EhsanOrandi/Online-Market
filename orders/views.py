from .models import Order, OrderItem
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from products.models import ShopProduct

# Create your views here.

class CartDetails(DetailView):
    model = Order
    pk_field = 'pk'
    template_name = 'components/cart.html'
    
    # def get_queryset(self):
    #     return Order.objects.all().first()
        # return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartDetails, self).get_context_data(**kwargs)
        order = context.get('order', None)
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

# def add_to_cart(request):
#     if request.method == 'POST' :
#         order = Order.objects.create(user=request.user)
  
@csrf_exempt       
def add_to_order(request):
    data = json.loads(request.body)
    order = Order.objects.get(user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    shop_product = ShopProduct.objects.filter(product__id=data['product_name']).first()
    if not order:
        order = Order.objects.create(user=request.user)
    try:
        for item in order_items:
            if item.shop_product.product == shop_product.product:
                item.count = item.count+1
                return HttpResponse(json.dumps(data), status=201)
        order_item = OrderItem.objects.create(
            order=order, shop_product_id=data['shop_name'], count=1, price=data['product_price']
        )
        response = {'shop_name':order_item.shop_product_id, "count":order_item.count, "price":order_item.price, 'order':order_item.order.id}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": 'error'}
        return HttpResponse(json.dumps(response), status=400)

class DeleteItem(DeleteView):
    model = OrderItem
    def get_success_url(self):
        return reverse('cart', args = (self.object.order.id,))

    # For Deleteview with post requests (not get requests)
    # In post requests, no confirmation template is needed (in contrast to get requests)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
