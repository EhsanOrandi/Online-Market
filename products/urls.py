from django.urls import path
from .views import ProductSingle, ProductsList, add_comment, ShopDetails, likeComment


urlpatterns = [
    path('categories/<slug:slug>/', ProductsList.as_view(), name="category_single"),
    path("products/add_comment/", add_comment, name="add_comment"),
    path("products/like_comment/", likeComment, name="like_comment"),
    path('products/<slug:slug>/', ProductSingle.as_view(), name="product_single"),
    path('sellers/<slug:slug>/', ShopDetails.as_view(), name="shop_single"),
]