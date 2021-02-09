from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('siteview.urls')),
    path('main/', include('products.urls')),
    path('user/', include('accounts.urls')),
    path('order/', include('orders.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
