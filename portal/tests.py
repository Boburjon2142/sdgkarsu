from django.test import Client, TestCase
from django.urls import reverse

from .forms import ContactSubmissionForm
from .models import ContactSubmission, PageContent, SDGWorkItem, SiteSettings


class PortalSmokeTests(TestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "institution_name": "Institutional Platform",
                "institution_short_name": "IP",
                "tagline": "Official platform",
                "official_badge": "Official portal",
                "navbar_cta_label": "Reports",
                "navbar_cta_url": "/reports-insights/",
                "hero_kicker": "Institutional",
                "hero_title": "Institutional platform",
                "hero_description": "Portal description",
                "hero_primary_label": "Programs",
                "hero_primary_url": "/programs/",
                "hero_secondary_label": "Reports",
                "hero_secondary_url": "/reports-insights/",
                "overview_title": "Overview",
                "overview_text": "Overview text",
                "mission": "Mission text",
                "vision": "Vision text",
                "strategic_approach": "Strategy text",
                "governance_overview": "Governance text",
                "strategy_overview": "Policy text",
                "leader_name": "Leader",
                "leader_title": "Title",
                "leader_message": "Message",
                "leader_signature": "Office",
                "address": "Address",
                "phone": "+998700000000",
                "email": "office@example.com",
                "office_hours": "09:00-18:00",
                "footer_text": "Footer text",
                "meta_title": "Meta",
                "meta_description": "Description",
            },
        )
        for page_key, _label in PageContent.PageKey.choices:
            PageContent.objects.update_or_create(
                page_key=page_key,
                defaults={
                    "eyebrow": page_key.title(),
                    "title": f"{page_key.title()} title",
                    "intro": f"{page_key.title()} intro",
                },
            )

    def test_homepage_loads(self):
        response = Client().get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A sustainable future starts today")

    def test_health_check_returns_ok(self):
        response = Client().get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_homepage_switches_to_uzbek_copy(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("home"))

        self.assertContains(response, "Barqaror kelajak bugundan boshlanadi")
        self.assertContains(response, "Qarshi davlat universiteti rektori")
        self.assertContains(response, "Barqarorlikka oid yangiliklar")

    def test_contact_form_saves_submission(self):
        form = ContactSubmissionForm(
            data={
                "full_name": "Nodira Ermatova",
                "email": "nodira@example.com",
                "organization": "Policy Lab",
                "subject": "general",
                "message": "Requesting more information about the platform.",
            }
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(ContactSubmission.objects.count(), 1)

    def test_sdg_10_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 10}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tengsizlikni kamaytirish")
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Mamlakatlar o'rtasidagi va ichida mavjud bo'lgan tengsizlikni qisqartirish.",
        )

    def test_sdg_11_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 11}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Barqaror shaharlar va aholi yashash joylari")
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Shahar va aholi yashash joylarining ochiqligi, xavfsizligi, mustahkamligi va ekologik barqarorligini ta'minlash.",
        )

    def test_sdg_12_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 12}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Mas'uliyatli iste'mol va ishlab chiqarish",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Oqilona iste'mol qilish va ishlab chiqarish modellariga o'tishni ta'minlash.",
        )

    def test_sdg_13_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 13}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Iqlim o'zgarishiga qarshi kurashish",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Iqlim o'zgarishi va uning oqibatlariga qarshi kurashish bo'yicha tezkor choralar ko'rish.",
        )

    def test_sdg_14_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 14}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Dengiz ekotizimlarini asrash",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Barqaror taraqqiyot yo'lida okeanlar, dengizlar va dengiz zaxiralarini asrash va ulardan oqilona foydalanish.",
        )

    def test_sdg_15_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 15}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Quruqlikdagi ekotizimlarni asrash",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "O'rmonlardan oqilona foydalanish, cho'llashishga qarshi kurashish, yer tanazzuli holatlariga chek qo'yish va yer unumdorligini qayta tiklash hamda biologik xilma-xillikning yo'qolib ketish xavfini bartaraf etish.",
        )

    def test_sdg_16_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 16}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Tinchlik, adolat va samarali boshqaruv",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Barqaror rivojlanish manfaatlari yo'lida tinchliksevar va ochiq jamiyatlar qurilishiga ko'maklashish, barcha uchun odil sudlov imkoniyatidan foydalanishni ta'minlash va barcha darajalarda samarali, hisobdor va keng ishtirokka asoslangan muassasalarni tashkil etish.",
        )

    def test_sdg_17_detail_uses_uzbek_custom_content(self):
        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 17}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["detail_content"]["hero_title"],
            "Barqaror rivojlanish yo'lida hamkorlik",
        )
        self.assertEqual(
            response.context["detail_content"]["idea_text"],
            "Barqaror rivojlanish manfaatlari yo'lida global hamkorlikni faollashtirish.",
        )

    def test_homepage_has_clickable_sdg_cards(self):
        response = Client().get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("sdg-updates", kwargs={"number": 4}))
        self.assertContains(response, "sdg-news-card")

    def test_sdg_detail_shows_admin_work_items(self):
        SDGWorkItem.objects.create(
            goal_number=4,
            title="Yashil kampus darsi",
            summary="SDG 4 doirasida yangi o'quv tashabbusi.",
            details="Talabalar uchun maxsus modul yo'lga qo'yildi.",
            external_url="https://example.com/sdg4",
        )

        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-detail", kwargs={"number": 4}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yashil kampus darsi")
        self.assertContains(response, "SDG 4 bo'yicha amalga oshirilgan ishlar")

    def test_sdg_updates_page_shows_goal_specific_news(self):
        SDGWorkItem.objects.create(
            goal_number=2,
            title="Oziq-ovqat xavfsizligi loyihasi",
            summary="SDG 2 bo'yicha yangi yangilik.",
        )

        client = Client()
        session = client.session
        session["portal_language"] = "uz"
        session.save()

        response = client.get(reverse("sdg-updates", kwargs={"number": 2}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SDG 2 bo'yicha yangiliklar")
        self.assertContains(response, "Oziq-ovqat xavfsizligi loyihasi")
