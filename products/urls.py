from django.urls import path
from .views import ProductSingle


urlpatterns = [
    path('<slug:slug>', ProductSingle.as_view(), name="product_single"),
]