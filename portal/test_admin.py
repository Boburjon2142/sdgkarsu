import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import NewsArticle


class SDGNewsAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser("sdg-admin", "admin@example.com", "test-password")

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_dashboard_has_goal_shortcuts(self):
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "sdg_goal=17")
        self.assertContains(response, "Boshqa boshqaruv bo'limlari")

    def test_add_form_preselects_goal(self):
        response = self.client.get(reverse("admin:portal_newsarticle_add"), {"sdg_goal": 4})
        self.assertEqual(response.context["adminform"].form.initial["sdg_goal"], "4")
        self.assertEqual(response.context["adminform"].form.initial["category"], "official")
        self.assertIsNotNone(response.context["adminform"].form.initial["published_on"])
        self.assertNotIn("summary_uz", response.context["adminform"].form.fields)
        self.assertNotIn("summary_en", response.context["adminform"].form.fields)

    def test_uzbek_news_gets_unique_slug_and_legacy_content(self):
        payload = {
            "sdg_goal": 4, "title_uz": "Yangi dars",
            "body_uz": "To'liq yangilik matni", "category": "official", "published_on": "2026-10-27",
            "_save": "Save",
        }
        for attempt in range(2):
            response = self.client.post(reverse("admin:portal_newsarticle_add"), payload)
            self.assertEqual(response.status_code, 302)
        articles = NewsArticle.objects.filter(title_uz="Yangi dars")
        self.assertEqual(articles.count(), 2)
        self.assertEqual(len(set(articles.values_list("slug", flat=True))), 2)
        self.assertEqual(articles.first().body, payload["body_uz"])
        self.assertEqual(articles.first().summary_uz, payload["body_uz"])

    def test_english_summary_strips_html_and_limits_length(self):
        response = self.client.post(reverse("admin:portal_newsarticle_add"), {
            "sdg_goal": 3, "title_en": "Health news", "body_en": "<p>Healthy campus</p> " * 40,
            "category": "official", "published_on": "2026-10-27",
        })
        self.assertEqual(response.status_code, 302)
        article = NewsArticle.objects.get(title_en="Health news")
        self.assertLessEqual(len(article.summary_en), 220)
        self.assertNotIn("<p>", article.summary_en)
        self.assertEqual(article.summary, article.summary_en)

    def test_existing_summary_preserved_until_body_changes(self):
        article = NewsArticle.objects.create(
            title="Original", title_uz="Original", body="Original body", body_uz="Original body",
            summary="Edited summary", summary_uz="Edited summary", slug="original",
            sdg_goal=4, category="official", published_on="2026-10-27",
        )
        payload = {"title_uz": "Updated title", "body_uz": "Original body", "sdg_goal": 4,
                   "category": "official", "published_on": "2026-10-27", "slug": "original"}
        change_url = reverse("admin:portal_newsarticle_change", args=[article.pk])
        self.assertEqual(self.client.post(change_url, payload).status_code, 302)
        article.refresh_from_db()
        self.assertEqual(article.summary_uz, "Edited summary")
        payload["body_uz"] = "Updated body"
        self.assertEqual(self.client.post(change_url, payload).status_code, 302)
        article.refresh_from_db()
        self.assertEqual(article.summary_uz, "Updated body")

    def test_goal_and_content_are_required(self):
        response = self.client.post(reverse("admin:portal_newsarticle_add"), {
            "category": "official", "published_on": "2026-10-27",
        })
        errors = response.context["adminform"].form.errors
        self.assertIn("sdg_goal", errors)
        self.assertIn("title_uz", errors)
        self.assertIn("body_uz", errors)

    def test_news_blocks_save_and_render_safely_in_order(self):
        body = json.dumps({"format": "sdg-news-blocks-v1", "blocks": [
            {"type": "text", "text": "Birinchi qism"},
            {"type": "table", "rows": [["Yil", "Natija"], ["2026", "<script>alert(1)</script>"]]},
            {"type": "text", "text": "Oxirgi qism"},
        ]})
        response = self.client.post(reverse("admin:portal_newsarticle_add"), {
            "sdg_goal": 3, "title_uz": "Jadvalli yangilik", "body_uz": body,
            "category": "official", "published_on": "2026-10-27",
        })
        self.assertEqual(response.status_code, 302)
        article = NewsArticle.objects.get(title_uz="Jadvalli yangilik")
        self.assertNotIn("sdg-news-blocks-v1", article.summary_uz)
        self.assertIn("Birinchi qism", article.summary_uz)
        session = self.client.session
        session["portal_language"] = "uz"
        session.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, '<th scope="col">Yil</th>', html=True)
        self.assertNotContains(response, "<script>alert(1)</script>")
        content = response.content.decode()
        self.assertLess(content.index("<th"), content.index("<p>Oxirgi qism"))
        response = self.client.get(reverse("sdg-updates", args=[3]))
        self.assertContains(response, "Jadvalli yangilik")
        self.assertContains(response, "Birinchi qism")
        self.assertNotContains(response, "sdg-news-blocks-v1")
        self.assertContains(response, article.get_absolute_url())

    def test_invalid_table_is_rejected(self):
        response = self.client.post(reverse("admin:portal_newsarticle_add"), {
            "sdg_goal": 3, "title_uz": "Invalid", "body_uz": json.dumps({
                "format": "sdg-news-blocks-v1", "blocks": [{"type": "table", "rows": [["One"], ["Two", "Three"]]}],
            }), "category": "official", "published_on": "2026-10-27",
        })
        self.assertIn("body_uz", response.context["adminform"].form.errors)

    def test_localized_news_preserves_json_with_quotes_and_entities(self):
        body = json.dumps({"format": "sdg-news-blocks-v1", "blocks": [
            {"type": "text", "text": "Campus \u201cgreen\u201d &quot;mobility&quot;\n\nNext paragraph"},
            {"type": "table", "rows": [["Program"], ["\u201cWater\u201d &quot;research&quot;"]]},
            {"type": "text", "text": "<script>alert(1)</script>"},
        ]}, ensure_ascii=False)
        article = NewsArticle.objects.create(
            title="Campus", slug="campus-quotes", body=body, body_en=body, body_uz=body,
            category="official", published_on="2026-10-29",
        )
        for language in ("en", "uz"):
            with self.subTest(language=language):
                session = self.client.session
                session["portal_language"] = language
                session.save()
                response = self.client.get(article.get_absolute_url())
                self.assertContains(response, '<p>Campus &quot;green&quot; &quot;mobility&quot;</p>', html=True)
                self.assertContains(response, '<p>Next paragraph</p>', html=True)
                self.assertContains(response, '<td>&quot;Water&quot; &quot;research&quot;</td>', html=True)
                self.assertNotContains(response, "sdg-news-blocks-v1")
                self.assertNotContains(response, "<script>alert(1)</script>")
        article.refresh_from_db()
        self.assertEqual(article.body_en, body)

    def test_unrelated_staff_does_not_get_news_shortcuts(self):
        staff = get_user_model().objects.create_user("contacts-editor", is_staff=True)
        staff.user_permissions.add(Permission.objects.get(codename="view_contactsubmission"))
        self.client.force_login(staff)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "sdg_goal=17")
