from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _     # for making app multilingual
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.urls import reverse
User = get_user_model()

# Create your models here.
class Category (models.Model) :
    name = models.CharField(_("Name"), max_length=125)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    details = models.TextField(_("Details"), null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to='category/image', blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True, related_name='children', related_query_name='children')
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Brand (models.Model) :
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    details = models.TextField(_("Details"), null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="brand/image", blank=True, null=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.slug


class Product (models.Model) :
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    details = models.TextField(_("Details"), null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="product/main_image", blank=True, null=True)
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"), on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    

    def __str__(self):
        return self.name

class ProductMeta(models.Model):
    label = models.CharField(_("Label"), max_length=100)
    value = models.CharField(_("Value"), max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))

    def __str__(self):
        return self.label


class ShopProduct (models.Model) :
    price = models.IntegerField(_("Price"))
    quantity = models.IntegerField(_("Quantity"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey('accounts.Shop', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Shop Product")
        verbose_name_plural = _("Shop Products")
        unique_together = [('shop', 'product')]

    def __str__(self):
        return str(self.shop)


class Image (models.Model) :
    image = models.ImageField(_("Image"), upload_to="product/image")
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return str(self.product)



class Comment (models.Model) :
    text = models.TextField(_("Text"))
    rate = models.IntegerField(_("Rate"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("product"), related_name='comments', related_query_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text

    # @property
    # def like_count(self):
    #     return Comment_like.objects.filter(comment=self, status=True).count()

    # @property
    # def dislike_count(self):
    #     return Comment_like.objects.filter(comment=self, status=False).count()