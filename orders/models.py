from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _     # for making app multilingual
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
User = get_user_model()

# Create your models here.

class Order(models.Model) :
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_("Create At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update At"), auto_now=True)
    description = models.CharField(_("Description"), max_length=150, default="Test")

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model) :
    order = models.ForeignKey(Order, related_name='order_item', related_query_name='order_item', verbose_name=_("order"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey("products.ShopProduct", verbose_name=_("shop product"), on_delete=models.CASCADE)
    count = models.IntegerField(_("Count"))
    price = models.IntegerField(_("Price"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Basket(models.Model) :
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")


class BasketItem(models.Model) :
    basket = models.ForeignKey(Basket, verbose_name=_("Basket"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey("products.ShopProduct", verbose_name=_("Shop Product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Basket Item")
        verbose_name_plural = _("Basket Items")
    