from django.urls import path
from .views import CartDetails, add_to_order, DeleteItem

urlpatterns = [
    path('cart/<int:pk>', CartDetails.as_view(), name="cart"),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name="delete-item"),
    path('add-to-order', add_to_order, name="add_to_order"),
]
