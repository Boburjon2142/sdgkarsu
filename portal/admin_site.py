from django.contrib.admin import AdminSite
from django.db.models import Count
from django.urls import reverse


class SDGAdminSite(AdminSite):
    site_header = "SDG yangiliklar boshqaruvi"
    site_title = "SDG Admin"
    index_title = "SDG bo'yicha yangiliklar"
    index_template = "admin/sdg_index.html"
    enable_nav_sidebar = False

    def index(self, request, extra_context=None):
        from .models import NewsArticle

        news_admin = self._registry[NewsArticle]
        context = dict(extra_context or {})
        can_view = news_admin.has_view_or_change_permission(request)
        can_add = news_admin.has_add_permission(request)
        context["can_view_news"] = can_view
        context["can_add_news"] = can_add
        if can_view or can_add:
            counts = {}
            if can_view:
                counts = dict(
                    news_admin.get_queryset(request)
                    .values("sdg_goal")
                    .annotate(total=Count("pk"))
                    .values_list("sdg_goal", "total")
                )
            context["news_list_url"] = reverse("admin:portal_newsarticle_changelist")
            context["news_add_url"] = reverse("admin:portal_newsarticle_add")
            context["sdg_news_goals"] = [
                {"number": number, "count": counts.get(number, 0)}
                for number, label in NewsArticle.SDG_CHOICES
            ]
        return super().index(request, extra_context=context)
