from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Event, NewsArticle


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "programs",
            "research",
            "education",
            "sustainability",
            "reports",
            "news-events",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
