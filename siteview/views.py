from django.shortcuts import render
from django.views.generic import TemplateView
from .models import SlideShow
from products.models import Category, ShopProduct, Brand
# Create your views here.

class HomeView(TemplateView):
    template_name = 'components/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] =  SlideShow.objects.all()
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['products'] = ShopProduct.objects.filter(quantity__gte=1)
        context['brands'] = Brand.objects.exclude(image='')
        return context
