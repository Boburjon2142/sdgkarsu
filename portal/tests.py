from django.test import Client, TestCase
from django.urls import reverse

from .forms import ContactSubmissionForm
from .models import ContactSubmission, PageContent, SiteSettings


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
        self.assertContains(response, "Institutional platform")

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
