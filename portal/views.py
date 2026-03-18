from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from .forms import ContactSubmissionForm
from .models import (
    Achievement,
    DepartmentContact,
    EducationInitiative,
    Event,
    GovernanceRole,
    HeroStat,
    ImpactMetric,
    InstitutionalValue,
    NewsArticle,
    PageContent,
    Partner,
    PolicyDocument,
    Program,
    Report,
    ResearchProject,
    SiteSettings,
    StrategicPriority,
)
from .translation_utils import localize_collection, localize_object, translate_text


def set_portal_language(request, language_code):
    language_code = language_code if language_code in {"uz", "en"} else "en"
    request.session["portal_language"] = language_code
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    response = redirect(next_url)
    response.set_cookie("portal_language", language_code)
    return response


class BasePortalContextMixin:
    page_key = "home"

    def get_language_code(self):
        return getattr(self.request, "LANGUAGE_CODE", "en")

    def get_site_settings(self):
        return localize_object(SiteSettings.objects.first(), self.get_language_code())

    def get_page_content(self):
        return localize_object(PageContent.objects.filter(page_key=self.page_key).first(), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = self.get_site_settings()
        context["page_content"] = self.get_page_content()
        context["footer_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], self.get_language_code())
        context["footer_departments"] = localize_collection(DepartmentContact.objects.all()[:3], self.get_language_code())
        context["active_page"] = self.page_key
        context["current_language"] = self.get_language_code()
        return context


class HomeView(BasePortalContextMixin, TemplateView):
    template_name = "portal/home.html"
    page_key = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["hero_stats"] = localize_collection(HeroStat.objects.all()[:4], language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all()[:4], language_code)
        context["featured_programs"] = localize_collection(Program.objects.filter(featured=True)[:3], language_code)
        context["featured_research"] = localize_collection(ResearchProject.objects.filter(featured=True)[:2], language_code)
        context["impact_metrics"] = localize_collection(ImpactMetric.objects.filter(scope__in=["home", "both"])[:4], language_code)
        context["latest_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], language_code)
        context["latest_news"] = localize_collection(NewsArticle.objects.all()[:3], language_code)
        context["partners"] = localize_collection(Partner.objects.all()[:6], language_code)
        return context


class AboutView(BasePortalContextMixin, TemplateView):
    template_name = "portal/about.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["values"] = localize_collection(InstitutionalValue.objects.all(), language_code)
        context["governance_roles"] = localize_collection(GovernanceRole.objects.all(), language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all(), language_code)
        return context


class ProgramsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/programs.html"
    page_key = "programs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_programs"] = localize_collection(Program.objects.filter(featured=True), language_code)
        context["programs"] = localize_collection(Program.objects.all(), language_code)
        return context


class ResearchView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_projects"] = localize_collection(ResearchProject.objects.filter(featured=True), language_code)
        context["projects"] = localize_collection(ResearchProject.objects.all(), language_code)
        return context


class EducationView(BasePortalContextMixin, TemplateView):
    template_name = "portal/education.html"
    page_key = "education"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_initiatives"] = localize_collection(EducationInitiative.objects.filter(featured=True), language_code)
        context["initiatives"] = localize_collection(EducationInitiative.objects.all(), language_code)
        return context


class SustainabilityView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sustainability.html"
    page_key = "sustainability"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["policies"] = localize_collection(PolicyDocument.objects.all(), language_code)
        context["featured_policies"] = localize_collection(PolicyDocument.objects.filter(featured=True)[:3], language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all(), language_code)
        return context


class ReportsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/reports.html"
    page_key = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["metrics"] = localize_collection(ImpactMetric.objects.filter(scope__in=["reports", "both"]), language_code)
        context["reports"] = localize_collection(Report.objects.all(), language_code)
        context["featured_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], language_code)
        context["achievements"] = localize_collection(Achievement.objects.all(), language_code)
        return context


class NewsEventsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/news_events.html"
    page_key = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        featured_article = NewsArticle.objects.filter(featured=True).first() or NewsArticle.objects.first()
        context["featured_article"] = localize_object(featured_article, language_code)
        context["news_items"] = localize_collection(NewsArticle.objects.all(), language_code)
        context["events"] = localize_collection(Event.objects.all(), language_code)
        return context


class NewsDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/news_detail.html"
    model = NewsArticle
    context_object_name = "article"
    page_key = "news"

    def get_object(self, queryset=None):
        return localize_object(super().get_object(queryset), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["related_reports"] = localize_collection(Report.objects.filter(featured=True)[:2], language_code)
        context["recent_news"] = localize_collection(NewsArticle.objects.exclude(pk=self.object.pk)[:3], language_code)
        return context


class EventDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/event_detail.html"
    model = Event
    context_object_name = "event"
    page_key = "news"

    def get_object(self, queryset=None):
        return localize_object(super().get_object(queryset), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_events"] = localize_collection(Event.objects.exclude(pk=self.object.pk)[:3], self.get_language_code())
        return context


class ContactView(BasePortalContextMixin, TemplateView):
    template_name = "portal/contact.html"
    page_key = "contact"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", ContactSubmissionForm(language_code=self.get_language_code()))
        context["departments"] = localize_collection(DepartmentContact.objects.all(), self.get_language_code())
        return context

    def post(self, request, *args, **kwargs):
        form = ContactSubmissionForm(request.POST, language_code=self.get_language_code())
        if form.is_valid():
            form.save()
            messages.success(
                request,
                translate_text("Your message has been submitted to the institutional coordination office.", self.get_language_code()),
            )
            return redirect("contact")
        return self.render_to_response(self.get_context_data(form=form))


def robots_txt(_request):
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Sitemap: /sitemap.xml",
        ]
    )
    return HttpResponse(content, content_type="text/plain")
