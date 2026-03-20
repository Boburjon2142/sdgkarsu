from django.contrib import messages
from django.http import Http404, HttpResponse
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
        "gif": "images/goals/gifs/E_GIF_01.gif",
        "title_en": "No Poverty",
        "title_uz": "Kambag'allikka barham berish",
        "description_en": "End poverty in all its forms everywhere through inclusive protection systems, access to services, and resilient livelihoods.",
        "description_uz": "Har qanday ko'rinishdagi kambag'allikka barham berish, himoya tizimlari, xizmatlar va barqaror turmush manbalari orqali aholining imkoniyatlarini kengaytirish.",
    },
    {
        "number": 2,
        "image_en": "images/goals/E_WEB_02.png",
        "image_uz": "images/goals/E_WEB_02.png",
        "gif": "images/goals/gifs/E_GIF_02.gif",
        "title_en": "Zero Hunger",
        "title_uz": "Ochlikka barham berish",
        "description_en": "Achieve food security, improve nutrition, and promote sustainable agriculture for healthier communities.",
        "description_uz": "Oziq-ovqat xavfsizligini ta'minlash, ovqatlanish sifatini yaxshilash va barqaror qishloq xo'jaligini rivojlantirish.",
    },
    {
        "number": 3,
        "image_en": "images/goals/E_WEB_03.png",
        "image_uz": "images/goals/E_WEB_03.png",
        "gif": "images/goals/gifs/E_GIF_03.gif",
        "title_en": "Good Health and Well-being",
        "title_uz": "Sog'lik va farovonlik",
        "description_en": "Ensure healthy lives and promote well-being for all at all ages with equitable access to health services.",
        "description_uz": "Har bir yoshdagi insonlar uchun sog'lom turmush va farovonlikni ta'minlash, tibbiy xizmatlardan teng foydalanishni kengaytirish.",
    },
    {
        "number": 4,
        "image_en": "images/goals/E_WEB_04.png",
        "image_uz": "images/goals/E_WEB_04.png",
        "gif": "images/goals/gifs/E_GIF_04.gif",
        "title_en": "Quality Education",
        "title_uz": "Sifatli ta'lim",
        "description_en": "Deliver inclusive and equitable quality education and promote lifelong learning opportunities for all.",
        "description_uz": "Inklyuziv va adolatli sifatli ta'limni ta'minlash hamda umrbod o'qish imkoniyatlarini kengaytirish.",
    },
    {
        "number": 5,
        "image_en": "images/goals/E_WEB_05.png",
        "image_uz": "images/goals/E_WEB_05.png",
        "gif": "images/goals/gifs/E_GIF_05.gif",
        "title_en": "Gender Equality",
        "title_uz": "Gender tenglik",
        "description_en": "Achieve gender equality and empower all women and girls in leadership, education, and economic life.",
        "description_uz": "Gender tengligini ta'minlash va barcha ayollar hamda qizlarning ta'lim, boshqaruv va iqtisodiy hayotdagi imkoniyatlarini oshirish.",
    },
    {
        "number": 6,
        "image_en": "images/goals/E_WEB_06.png",
        "image_uz": "images/goals/E_WEB_06.png",
        "gif": "images/goals/gifs/E_GIF_06.gif",
        "title_en": "Clean Water and Sanitation",
        "title_uz": "Toza suv va sanitariya",
        "description_en": "Ensure availability and sustainable management of water and sanitation for all communities.",
        "description_uz": "Barcha uchun xavfsiz ichimlik suvi va sanitariya xizmatlaridan foydalanishni hamda ularning barqaror boshqaruvini ta'minlash.",
    },
    {
        "number": 7,
        "image_en": "images/goals/E_WEB_07.png",
        "image_uz": "images/goals/E_WEB_07.png",
        "gif": "images/goals/gifs/E_GIF_07.gif",
        "title_en": "Affordable and Clean Energy",
        "title_uz": "Arzon va toza energiya",
        "description_en": "Ensure access to affordable, reliable, sustainable, and modern energy for all.",
        "description_uz": "Arzon, ishonchli, zamonaviy va ekologik toza energiyadan foydalanish imkonini kengaytirish.",
    },
    {
        "number": 8,
        "image_en": "images/goals/E_WEB_08.png",
        "image_uz": "images/goals/E_WEB_08.png",
        "gif": "images/goals/gifs/E_GIF_08.gif",
        "title_en": "Decent Work and Economic Growth",
        "title_uz": "Munosib mehnat va iqtisodiy o'sish",
        "description_en": "Promote sustained, inclusive economic growth, productive employment, and decent work for all.",
        "description_uz": "Barqaror va inklyuziv iqtisodiy o'sishni, samarali bandlikni va munosib mehnat sharoitlarini rivojlantirish.",
    },
    {
        "number": 9,
        "image_en": "images/goals/E_WEB_09.png",
        "image_uz": "images/goals/E_WEB_09.png",
        "gif": "images/goals/gifs/E_GIF_09.gif",
        "title_en": "Industry, Innovation and Infrastructure",
        "title_uz": "Sanoat, innovatsiya va infratuzilma",
        "description_en": "Build resilient infrastructure, promote inclusive industrialization, and foster innovation.",
        "description_uz": "Chidamli infratuzilmani rivojlantirish, inklyuziv sanoatlashuvni qo'llab-quvvatlash va innovatsiyalarni kuchaytirish.",
    },
    {
        "number": 10,
        "image_en": "images/goals/E_WEB_10.png",
        "image_uz": "images/goals/E_WEB_10.png",
        "gif": "images/goals/gifs/E_GIF_10.gif",
        "title_en": "Reduced Inequalities",
        "title_uz": "Tengsizlikni qisqartirish",
        "description_en": "Reduce inequality within and among countries through inclusive policy and equal opportunity.",
        "description_uz": "Mamlakat ichida va mamlakatlar o'rtasidagi tengsizlikni kamaytirish, teng imkoniyat va inklyuziv siyosatni kuchaytirish.",
    },
    {
        "number": 11,
        "image_en": "images/goals/E_WEB_11.png",
        "image_uz": "images/goals/E_WEB_11.png",
        "gif": "images/goals/gifs/E_GIF_11.gif",
        "title_en": "Sustainable Cities and Communities",
        "title_uz": "Barqaror shaharlar va aholi yashash joylari",
        "description_en": "Make cities and human settlements inclusive, safe, resilient, and sustainable.",
        "description_uz": "Shaharlar va aholi yashash joylarini xavfsiz, inklyuziv, chidamli va barqaror qilish.",
    },
    {
        "number": 12,
        "image_en": "images/goals/E_WEB_12.png",
        "image_uz": "images/goals/E_WEB_12.png",
        "gif": "images/goals/gifs/E_GIF_12.gif",
        "title_en": "Responsible Consumption and Production",
        "title_uz": "Mas'uliyatli iste'mol va ishlab chiqarish",
        "description_en": "Ensure sustainable consumption and production patterns across institutions and communities.",
        "description_uz": "Muassasalar va jamoalarda barqaror iste'mol va ishlab chiqarish madaniyatini shakllantirish.",
    },
    {
        "number": 13,
        "image_en": "images/goals/E_WEB_13.png",
        "image_uz": "images/goals/E_WEB_13.png",
        "gif": "images/goals/gifs/E_GIF_13.gif",
        "title_en": "Climate Action",
        "title_uz": "Iqlim o'zgarishiga qarshi kurashish",
        "description_en": "Take urgent action to combat climate change and its impacts through adaptation and mitigation.",
        "description_uz": "Iqlim o'zgarishi va uning oqibatlariga qarshi tezkor choralar ko'rish, moslashuv va kamaytirish strategiyalarini kuchaytirish.",
    },
    {
        "number": 14,
        "image_en": "images/goals/E_WEB_14.png",
        "image_uz": "images/goals/E_WEB_14.png",
        "gif": "images/goals/gifs/E_GIF_14.gif",
        "title_en": "Life Below Water",
        "title_uz": "Suv osti hayoti",
        "description_en": "Conserve and sustainably use oceans, seas, and marine resources for sustainable development.",
        "description_uz": "Okeanlar, dengizlar va suv resurslarini asrash va ulardan barqaror foydalanishni rivojlantirish.",
    },
    {
        "number": 15,
        "image_en": "images/goals/E_WEB_15.png",
        "image_uz": "images/goals/E_WEB_15.png",
        "gif": "images/goals/gifs/E_GIF_15.gif",
        "title_en": "Life on Land",
        "title_uz": "Quruqlikdagi hayot",
        "description_en": "Protect, restore, and promote sustainable use of terrestrial ecosystems and biodiversity.",
        "description_uz": "Quruqlik ekotizimlarini asrash, tiklash va biologik xilma-xillikni qo'llab-quvvatlash.",
    },
    {
        "number": 16,
        "image_en": "images/goals/E_WEB_16.png",
        "image_uz": "images/goals/E_WEB_16.png",
        "gif": "images/goals/gifs/E_GIF_16.gif",
        "title_en": "Peace, Justice and Strong Institutions",
        "title_uz": "Tinchlik, adolat va samarali boshqaruv",
        "description_en": "Promote peaceful societies, provide access to justice, and build effective, accountable institutions.",
        "description_uz": "Tinch va inklyuziv jamiyatlarni rivojlantirish, adolatga erishishni kengaytirish va samarali, hisobdor institutlarni mustahkamlash.",
    },
    {
        "number": 17,
        "image_en": "images/goals/E_WEB_17.png",
        "image_uz": "images/goals/E_WEB_17.png",
        "gif": "images/goals/gifs/E_GIF_17.gif",
        "title_en": "Partnerships for the Goals",
        "title_uz": "Maqsadlar yo'lida hamkorlik",
        "description_en": "Strengthen implementation and revitalize global partnerships for sustainable development.",
        "description_uz": "Barqaror rivojlanish uchun milliy va global hamkorliklarni kuchaytirish va birgalikdagi amalga oshirish mexanizmlarini rivojlantirish.",
    },
]


SDG_1_DETAIL_UZ = {
    "hero_title": "O‘ta qashshoqlikka barham berish",
    "idea_title": "Asosiy g‘oya",
    "idea_text": "Butun dunyoda barcha turdagi qashshoqlikni butkul yo‘q qilish",
    "sections": [
        {
            "title": "Umumiy ma’lumot",
            "paragraphs": [
                "2015-yilda Birlashgan Millatlar Tashkiloti tomonidan belgilangan Barqaror rivojlanish maqsadlarining birinchi yo‘nalishi — qashshoqlikning barcha shakllariga barham berishdir (SDG 1).",
                "Davlatlar quyidagi prinsipni qabul qilgan: “Hech kimni ortda qoldirmaslik”.",
                "Bu maqsad oziq-ovqat yetishmovchiligi, toza ichimlik suvi muammosi va sanitariya yetishmasligi kabi muammolarni ham qamrab oladi.",
                "Shuningdek, iqlim o‘zgarishi va mojarolar keltirib chiqaradigan xavflarni ham hal qilishni talab qiladi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 1 doirasida 7 ta maqsad va 13 ta ko‘rsatkich mavjud.",
                "Natijada quyidagilar amalga oshiriladi:",
            ],
            "bullets": [
                "O‘ta qashshoqlikni yo‘q qilish",
                "Qashshoqlikni kamida 50% ga qisqartirish",
                "Ijtimoiy himoya tizimini yaratish",
                "Resurs va xizmatlarga teng kirishni ta’minlash",
                "Ofatlarga chidamlilikni oshirish",
            ],
        },
        {
            "title": "Global holat",
            "paragraphs": ["Hozirgi kunda quyidagi ko‘rsatkichlar dolzarb hisoblanadi:"],
            "bullets": [
                "Dunyo aholisining taxminan 10% qashshoqlikda yashaydi",
                "2015-yilda 736 million odam o‘ta qashshoqlikda yashagan",
                "Eng katta ulush Afrika hududiga to‘g‘ri keladi",
                "Qishloqlarda qashshoqlik darajasi 17.2%",
                "Shaharlarda qashshoqlik darajasi 5.3%",
            ],
        },
        {
            "title": "Muammolar va xavflar",
            "paragraphs": [
                "Qashshoqlikka qarshi kurashni qiyinlashtirayotgan omillar quyidagilar:",
            ],
            "bullets": [
                "iqtisodiy tengsizlik",
                "siyosiy beqarorlik",
                "iqlim o‘zgarishi",
                "urush va mojarolar",
            ],
        },
        {
            "title": "Bolalar va qashshoqlik",
            "bullets": [
                "385 millionga yaqin bola kuniga $1.90 dan kam daromad bilan yashaydi",
                "Ko‘plab mamlakatlarda bolalar qashshoqligi bo‘yicha aniq statistika yo‘q",
                "97% mamlakatda yetarli data mavjud emas",
            ],
        },
        {
            "title": "Ijobiy o‘zgarishlar",
            "paragraphs": [
                "1990–2015 oralig‘ida qashshoqlikda yashovchilar soni 1.8 milliarddan 776 milliongacha kamaydi.",
                "Ammo muammo hali to‘liq hal bo‘lmagan va erishilgan natijalarni saqlab qolish uchun izchil siyosat zarur.",
            ],
        },
        {
            "title": "Hukumatlar roli",
            "paragraphs": ["Mahalliy va global hukumatlar quyidagi yo‘nalishlarda faol ishlaydi:"],
            "bullets": [
                "kam ta’minlanganlarni qo‘llab-quvvatlash",
                "shaffof boshqaruvni ta’minlash",
                "bandlikni oshirish",
                "ta’lim va iqtisodiy imkoniyatlarni kengaytirish",
            ],
        },
    ],
}


def build_sdg_goal(item, language_code):
    use_uz = language_code == "uz"
    return {
        "number": item["number"],
        "image": item["image_uz"] if use_uz else item["image_en"],
        "gif": item["gif"],
        "title": item["title_uz"] if use_uz else item["title_en"],
        "description": item["description_uz"] if use_uz else item["description_en"],
    }


def get_sdg_goal(number, language_code):
    raw_item = next((item for item in SDG_CONTENT if item["number"] == number), None)
    if not raw_item:
        raise Http404("SDG not found")
    return build_sdg_goal(raw_item, language_code)


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
        context["sdg_goals"] = [build_sdg_goal(item, language_code) for item in SDG_CONTENT]
        return context


class SDGDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sdg_detail.html"
    page_key = "programs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        number = kwargs["number"]
        goal = get_sdg_goal(number, language_code)
        context["goal"] = goal
        context["previous_goal"] = number - 1 if number > 1 else None
        context["next_goal"] = number + 1 if number < 17 else None

        if number == 1 and language_code == "uz":
            context["detail_content"] = SDG_1_DETAIL_UZ
        else:
            context["detail_content"] = {
                "hero_title": goal["title"],
                "idea_title": "Asosiy g‘oya" if language_code == "uz" else "Core idea",
                "idea_text": goal["description"],
                "sections": [
                    {
                        "title": "Umumiy ma’lumot" if language_code == "uz" else "Overview",
                        "paragraphs": [
                            goal["description"],
                            "Mazkur maqsad universitetning ilmiy izlanishlari, ta’lim dasturlari va jamoatchilik bilan ishlash tashabbuslari orqali qo‘llab-quvvatlanadi."
                            if language_code == "uz"
                            else "This goal is supported through the university's research agenda, educational programs, and community engagement initiatives.",
                        ],
                    },
                    {
                        "title": "Asosiy yo‘nalishlar" if language_code == "uz" else "Priority directions",
                        "bullets": [
                            "ta’lim, tadqiqot va kampus boshqaruvida integratsiya"
                            if language_code == "uz"
                            else "integration across teaching, research, and campus management",
                            "ma’lumotlarga asoslangan institutsional qarorlar"
                            if language_code == "uz"
                            else "data-informed institutional decision-making",
                            "mahalliy va xalqaro hamkorlik"
                            if language_code == "uz"
                            else "local and international partnerships",
                        ],
                    },
                ],
            }
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
