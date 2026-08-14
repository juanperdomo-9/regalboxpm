# ==========================================================
# REGALBOX PM — SITEMAP
# ==========================================================

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, GiftBox


class GiftBoxSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return GiftBox.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("giftbox_detail", args=[obj.slug])


class CategorySitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.filter(active=True, coming_soon=False)

    def location(self, obj):
        return reverse("category_detail", args=[obj.slug])


class StaticViewSitemap(Sitemap):

    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)
