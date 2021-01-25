from django.db import models
from django.utils.translation import ugettext_lazy as _ 

# Create your models here.

class SlideShow(models.Model) :
    title = models.CharField(_("Title"), max_length=150)
    text = models.TextField(_("Text"))
    image = models.ImageField(_("Image"), upload_to="slides")
    link = models.CharField(_("Link"), max_length=150, null=True, blank=True)