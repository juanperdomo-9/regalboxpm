from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from core import views
from core.admin import admin_site
from core.sitemaps import CategorySitemap, GiftBoxSitemap, StaticViewSitemap

sitemaps = {
    "boxes": GiftBoxSitemap,
    "categorias": CategorySitemap,
    "paginas": StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin_site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)