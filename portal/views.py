from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import activate
from django.views.generic import DetailView, TemplateView

from .forms import ContactSubmissionForm
from .models import (
    CampusInitiative,
    EngagementInitiative,
    Event,
    GovernanceRole,
    InsightMetric,
    NewsArticle,
    Partner,
    ResearchItem,
    SDG,
    SiteSettings,
    SustainabilityPolicy,
    SustainabilityReport,
)
from .translation_utils import localize_collection, localize_object, translate_text


def set_portal_language(request, language_code):
    supported_languages = {code for code, _label in settings.LANGUAGES}
    if language_code not in supported_languages:
        language_code = settings.LANGUAGE_CODE

    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    response = redirect(next_url)
    activate(language_code)
    request.session[settings.LANGUAGE_COOKIE_NAME] = language_code
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    return response


class BasePortalContextMixin:
    def get_language_code(self):
        return getattr(self.request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["site_settings"] = localize_object(SiteSettings.objects.first(), language_code)
        context["primary_reports"] = localize_collection(SustainabilityReport.objects.all()[:3], language_code)
        return context


class HomeView(BasePortalContextMixin, TemplateView):
    template_name = "portal/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_sdgs"] = localize_collection(SDG.objects.filter(featured=True)[:6], language_code)
        context["latest_news"] = localize_collection(NewsArticle.objects.all()[:3], language_code)
        context["upcoming_events"] = localize_collection(Event.objects.all()[:3], language_code)
        context["home_metrics"] = localize_collection(
            InsightMetric.objects.filter(page_scope__in=["home", "both"])[:4], language_code
        )
        context["partners"] = localize_collection(Partner.objects.all()[:5], language_code)
        return context


class AboutView(BasePortalContextMixin, TemplateView):
    template_name = "portal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["governance_roles"] = localize_collection(GovernanceRole.objects.all(), language_code)
        context["policies"] = localize_collection(SustainabilityPolicy.objects.all(), language_code)
        context["reports"] = localize_collection(SustainabilityReport.objects.all()[:3], language_code)
        return context


class SDGListView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sdgs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sdgs"] = localize_collection(SDG.objects.all(), self.get_language_code())
        return context


class SDGDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/sdg_detail.html"
    context_object_name = "sdg"

    def get_object(self, queryset=None):
        sdg = SDG.objects.prefetch_related("projects").get(number=self.kwargs["number"])
        return localize_object(sdg, self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["related_news"] = localize_collection(NewsArticle.objects.filter(featured=True)[:3], language_code)
        context["related_reports"] = localize_collection(SustainabilityReport.objects.all()[:3], language_code)
        context["sdg_projects"] = localize_collection(self.object.projects.all(), language_code)
        return context


class ResearchEducationView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research_education.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        research_categories = ["project", "publication", "center", "innovation", "grant"]
        education_categories = ["course", "program", "student", "mooc"]
        language_code = self.get_language_code()
        context["research_items"] = localize_collection(
            ResearchItem.objects.filter(category__in=research_categories), language_code
        )
        context["education_items"] = localize_collection(
            ResearchItem.objects.filter(category__in=education_categories), language_code
        )
        return context


class CampusView(BasePortalContextMixin, TemplateView):
    template_name = "portal/campus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["initiatives"] = localize_collection(CampusInitiative.objects.all(), language_code)
        context["metrics"] = localize_collection(
            InsightMetric.objects.filter(page_scope__in=["home", "both"])[:4], language_code
        )
        return context


class EngagementView(BasePortalContextMixin, TemplateView):
    template_name = "portal/engagement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initiatives"] = localize_collection(EngagementInitiative.objects.all(), self.get_language_code())
        return context


class InsightsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/insights.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["metrics"] = localize_collection(
            InsightMetric.objects.filter(page_scope__in=["insights", "both"]), language_code
        )
        context["reports"] = localize_collection(SustainabilityReport.objects.all(), language_code)
        return context


class NewsEventsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/news_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["news_items"] = localize_collection(NewsArticle.objects.all(), language_code)
        context["events"] = localize_collection(Event.objects.all(), language_code)
        return context


class NewsDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/news_detail.html"
    model = NewsArticle
    context_object_name = "article"

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        return localize_object(article, self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_reports"] = localize_collection(SustainabilityReport.objects.all()[:3], self.get_language_code())
        return context


class EventDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/event_detail.html"
    model = Event
    context_object_name = "event"

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        return localize_object(event, self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_reports"] = localize_collection(SustainabilityReport.objects.all()[:3], self.get_language_code())
        return context


class ContactView(BasePortalContextMixin, TemplateView):
    template_name = "portal/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", ContactSubmissionForm(language_code=self.get_language_code()))
        return context

    def post(self, request, *args, **kwargs):
        language_code = self.get_language_code()
        form = ContactSubmissionForm(request.POST, language_code=language_code)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                translate_text("Your inquiry has been submitted to the Sustainability Office.", language_code),
            )
            return redirect("contact")
        return self.render_to_response(self.get_context_data(form=form))
