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


SDG_CONTENT = [
    {
        "number": 1,
        "image_en": "images/goals/E_WEB_01.png",
        "image_uz": "images/goals/E_WEB_01.png",
        "title_en": "No Poverty",
        "title_uz": "Kambag'allikka barham berish",
        "description_en": "End poverty in all its forms everywhere through inclusive protection systems, access to services, and resilient livelihoods.",
        "description_uz": "Har qanday ko'rinishdagi kambag'allikka barham berish, himoya tizimlari, xizmatlar va barqaror turmush manbalari orqali aholining imkoniyatlarini kengaytirish.",
    },
    {
        "number": 2,
        "image_en": "images/goals/E_WEB_02.png",
        "image_uz": "images/goals/E_WEB_02.png",
        "title_en": "Zero Hunger",
        "title_uz": "Ochlikka barham berish",
        "description_en": "Achieve food security, improve nutrition, and promote sustainable agriculture for healthier communities.",
        "description_uz": "Oziq-ovqat xavfsizligini ta'minlash, ovqatlanish sifatini yaxshilash va barqaror qishloq xo'jaligini rivojlantirish.",
    },
    {
        "number": 3,
        "image_en": "images/goals/E_WEB_03.png",
        "image_uz": "images/goals/E_WEB_03.png",
        "title_en": "Good Health and Well-being",
        "title_uz": "Sog'lik va farovonlik",
        "description_en": "Ensure healthy lives and promote well-being for all at all ages with equitable access to health services.",
        "description_uz": "Har bir yoshdagi insonlar uchun sog'lom turmush va farovonlikni ta'minlash, tibbiy xizmatlardan teng foydalanishni kengaytirish.",
    },
    {
        "number": 4,
        "image_en": "images/goals/E_WEB_04.png",
        "image_uz": "images/goals/E_WEB_04.png",
        "title_en": "Quality Education",
        "title_uz": "Sifatli ta'lim",
        "description_en": "Deliver inclusive and equitable quality education and promote lifelong learning opportunities for all.",
        "description_uz": "Inklyuziv va adolatli sifatli ta'limni ta'minlash hamda umrbod o'qish imkoniyatlarini kengaytirish.",
    },
    {
        "number": 5,
        "image_en": "images/goals/E_WEB_05.png",
        "image_uz": "images/goals/E_WEB_05.png",
        "title_en": "Gender Equality",
        "title_uz": "Gender tenglik",
        "description_en": "Achieve gender equality and empower all women and girls in leadership, education, and economic life.",
        "description_uz": "Gender tengligini ta'minlash va barcha ayollar hamda qizlarning ta'lim, boshqaruv va iqtisodiy hayotdagi imkoniyatlarini oshirish.",
    },
    {
        "number": 6,
        "image_en": "images/goals/E_WEB_06.png",
        "image_uz": "images/goals/E_WEB_06.png",
        "title_en": "Clean Water and Sanitation",
        "title_uz": "Toza suv va sanitariya",
        "description_en": "Ensure availability and sustainable management of water and sanitation for all communities.",
        "description_uz": "Barcha uchun xavfsiz ichimlik suvi va sanitariya xizmatlaridan foydalanishni hamda ularning barqaror boshqaruvini ta'minlash.",
    },
    {
        "number": 7,
        "image_en": "images/goals/E_WEB_07.png",
        "image_uz": "images/goals/E_WEB_07.png",
        "title_en": "Affordable and Clean Energy",
        "title_uz": "Arzon va toza energiya",
        "description_en": "Ensure access to affordable, reliable, sustainable, and modern energy for all.",
        "description_uz": "Arzon, ishonchli, zamonaviy va ekologik toza energiyadan foydalanish imkonini kengaytirish.",
    },
    {
        "number": 8,
        "image_en": "images/goals/E_WEB_08.png",
        "image_uz": "images/goals/E_WEB_08.png",
        "title_en": "Decent Work and Economic Growth",
        "title_uz": "Munosib mehnat va iqtisodiy o'sish",
        "description_en": "Promote sustained, inclusive economic growth, productive employment, and decent work for all.",
        "description_uz": "Barqaror va inklyuziv iqtisodiy o'sishni, samarali bandlikni va munosib mehnat sharoitlarini rivojlantirish.",
    },
    {
        "number": 9,
        "image_en": "images/goals/E_WEB_09.png",
        "image_uz": "images/goals/E_WEB_09.png",
        "title_en": "Industry, Innovation and Infrastructure",
        "title_uz": "Sanoat, innovatsiya va infratuzilma",
        "description_en": "Build resilient infrastructure, promote inclusive industrialization, and foster innovation.",
        "description_uz": "Chidamli infratuzilmani rivojlantirish, inklyuziv sanoatlashuvni qo'llab-quvvatlash va innovatsiyalarni kuchaytirish.",
    },
    {
        "number": 10,
        "image_en": "images/goals/E_WEB_10.png",
        "image_uz": "images/goals/E_WEB_10.png",
        "title_en": "Reduced Inequalities",
        "title_uz": "Tengsizlikni qisqartirish",
        "description_en": "Reduce inequality within and among countries through inclusive policy and equal opportunity.",
        "description_uz": "Mamlakat ichida va mamlakatlar o'rtasidagi tengsizlikni kamaytirish, teng imkoniyat va inklyuziv siyosatni kuchaytirish.",
    },
    {
        "number": 11,
        "image_en": "images/goals/E_WEB_11.png",
        "image_uz": "images/goals/E_WEB_11.png",
        "title_en": "Sustainable Cities and Communities",
        "title_uz": "Barqaror shaharlar va aholi yashash joylari",
        "description_en": "Make cities and human settlements inclusive, safe, resilient, and sustainable.",
        "description_uz": "Shaharlar va aholi yashash joylarini xavfsiz, inklyuziv, chidamli va barqaror qilish.",
    },
    {
        "number": 12,
        "image_en": "images/goals/E_WEB_12.png",
        "image_uz": "images/goals/E_WEB_12.png",
        "title_en": "Responsible Consumption and Production",
        "title_uz": "Mas'uliyatli iste'mol va ishlab chiqarish",
        "description_en": "Ensure sustainable consumption and production patterns across institutions and communities.",
        "description_uz": "Muassasalar va jamoalarda barqaror iste'mol va ishlab chiqarish madaniyatini shakllantirish.",
    },
    {
        "number": 13,
        "image_en": "images/goals/E_WEB_13.png",
        "image_uz": "images/goals/E_WEB_13.png",
        "title_en": "Climate Action",
        "title_uz": "Iqlim o'zgarishiga qarshi kurashish",
        "description_en": "Take urgent action to combat climate change and its impacts through adaptation and mitigation.",
        "description_uz": "Iqlim o'zgarishi va uning oqibatlariga qarshi tezkor choralar ko'rish, moslashuv va kamaytirish strategiyalarini kuchaytirish.",
    },
    {
        "number": 14,
        "image_en": "images/goals/E_WEB_14.png",
        "image_uz": "images/goals/E_WEB_14.png",
        "title_en": "Life Below Water",
        "title_uz": "Suv osti hayoti",
        "description_en": "Conserve and sustainably use oceans, seas, and marine resources for sustainable development.",
        "description_uz": "Okeanlar, dengizlar va suv resurslarini asrash va ulardan barqaror foydalanishni rivojlantirish.",
    },
    {
        "number": 15,
        "image_en": "images/goals/E_WEB_15.png",
        "image_uz": "images/goals/E_WEB_15.png",
        "title_en": "Life on Land",
        "title_uz": "Quruqlikdagi hayot",
        "description_en": "Protect, restore, and promote sustainable use of terrestrial ecosystems and biodiversity.",
        "description_uz": "Quruqlik ekotizimlarini asrash, tiklash va biologik xilma-xillikni qo'llab-quvvatlash.",
    },
    {
        "number": 16,
        "image_en": "images/goals/E_WEB_16.png",
        "image_uz": "images/goals/E_WEB_16.png",
        "title_en": "Peace, Justice and Strong Institutions",
        "title_uz": "Tinchlik, adolat va samarali boshqaruv",
        "description_en": "Promote peaceful societies, provide access to justice, and build effective, accountable institutions.",
        "description_uz": "Tinch va inklyuziv jamiyatlarni rivojlantirish, adolatga erishishni kengaytirish va samarali, hisobdor institutlarni mustahkamlash.",
    },
    {
        "number": 17,
        "image_en": "images/goals/E_WEB_17.png",
        "image_uz": "images/goals/E_WEB_17.png",
        "title_en": "Partnerships for the Goals",
        "title_uz": "Maqsadlar yo'lida hamkorlik",
        "description_en": "Strengthen implementation and revitalize global partnerships for sustainable development.",
        "description_uz": "Barqaror rivojlanish uchun milliy va global hamkorliklarni kuchaytirish va birgalikdagi amalga oshirish mexanizmlarini rivojlantirish.",
    },
]


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
        context["sdg_goals"] = [
            {
                "number": item["number"],
                "image": item["image_uz"] if language_code == "uz" else item["image_en"],
                "title": item[f"title_{language_code}"] if language_code == "uz" else item["title_en"],
                "description": item[f"description_{language_code}"] if language_code == "uz" else item["description_en"],
            }
            for item in SDG_CONTENT
        ]
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
