from uuid import uuid4

from django import forms
from django.contrib import admin
from django.utils.html import format_html, strip_tags
from django.utils import timezone
from django.utils.text import Truncator, slugify
from .news_blocks import news_plain_text

from .models import (
    Achievement,
    ContactSubmission,
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
    SDGWorkItem,
    SiteSettings,
    StrategicPriority,
)


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class NewsArticleAdminForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = "__all__"
        help_texts = {
            "image": "Tavsiya: 1600 × 1000 px. Asosiy tasvir rasm markazida bo'lsin.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "sdg_goal": "SDG maqsadi", "title_uz": "Sarlavha",
            "body_uz": "Yangilik matni", "title_en": "English title",
            "body_en": "English content", "image": "Yangilik rasmi", "published_on": "Sana",
            "category": "Yangilik turi", "featured": "Ajratib ko'rsatish", "slug": "Havola nomi",
        }
        for name, label in labels.items():
            if name in self.fields:
                self.fields[name].label = label
        for name in ("title", "body"):
            if f"{name}_uz" in self.fields and not getattr(self.instance, f"{name}_uz") and not getattr(self.instance, f"{name}_en"):
                self.initial[f"{name}_uz"] = getattr(self.instance, name)
        if "sdg_goal" in self.fields:
            self.fields["sdg_goal"].required = True
        if "slug" in self.fields:
            self.fields["slug"].required = False
            self.fields["slug"].help_text = "Bo'sh qoldiring: sarlavhadan avtomatik yaratiladi."
        if "category" in self.fields and not self.instance.pk and not self.initial.get("category"):
            self.initial["category"] = NewsArticle.Category.OFFICIAL
        if "published_on" in self.fields and not self.instance.pk:
            if not self.initial.get("published_on"):
                self.initial["published_on"] = timezone.localdate()
        for name in ("title_uz", "title_en"):
            if name in self.fields:
                self.fields[name].widget = forms.TextInput(attrs={"class": "vTextField"})

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["title"] = cleaned_data.get("title_en") or cleaned_data.get("title_uz") or cleaned_data.get("title") or ""
        cleaned_data["body"] = cleaned_data.get("body_en") or cleaned_data.get("body_uz") or cleaned_data.get("body") or ""
        plain_bodies = {}
        for language in ("uz", "en"):
            try:
                plain_bodies[language] = news_plain_text(cleaned_data.get(f"body_{language}", ""))
            except forms.ValidationError as error:
                self.add_error(f"body_{language}", error)
                plain_bodies[language] = ""
        for language in ("uz", "en"):
            body_name = f"body_{language}"
            summary_name = f"summary_{language}"
            body = cleaned_data.get(body_name, "")
            existing_summary = getattr(self.instance, summary_name)
            if existing_summary and body == getattr(self.instance, body_name):
                cleaned_data[summary_name] = existing_summary
            else:
                cleaned_data[summary_name] = Truncator(" ".join(strip_tags(plain_bodies[language]).split())).chars(220)
        cleaned_data["summary"] = cleaned_data["summary_en"] or cleaned_data["summary_uz"]
        for name in ("title", "body"):
            content = " ".join(plain_bodies.values()) if name == "body" else cleaned_data[name]
            if not content.strip():
                self.add_error(f"{name}_uz", "O'zbekcha yoki inglizcha matn kiriting.")
        if not cleaned_data.get("slug"):
            base_slug = slugify(cleaned_data["title"])[:40] or "yangilik"
            candidate = base_slug
            while NewsArticle.objects.filter(slug=candidate).exclude(pk=self.instance.pk).exists():
                candidate = f"{base_slug}-{uuid4().hex[:8]}"
            cleaned_data["slug"] = candidate
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.title = self.cleaned_data.get("title", "")
        instance.summary = self.cleaned_data.get("summary", "")
        instance.summary_uz = self.cleaned_data.get("summary_uz", "")
        instance.summary_en = self.cleaned_data.get("summary_en", "")
        instance.body = self.cleaned_data.get("body", "")
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("institution_name", "email", "phone")
    fieldsets = (
        ("Basic information", {"fields": ("institution_name", "tagline")}),
        (
            "Hero",
            {
                "fields": (
                    "hero_kicker",
                    "hero_title",
                    "hero_description",
                    "hero_primary_label",
                    "hero_primary_url",
                    "hero_secondary_label",
                    "hero_secondary_url",
                )
            },
        ),
        ("Institutional narrative", {"fields": ("overview_title", "overview_text", "mission", "vision")}),
        ("Leadership", {"fields": ("leader_name", "leader_title", "leader_photo", "leader_message")}),
        ("Contact information", {"fields": ("address", "phone", "email", "office_hours")}),
    )


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("page_key", "title", "eyebrow")
    search_fields = ("title", "intro", "supporting_text")
    fieldsets = (
        ("Basic information", {"fields": ("page_key", "eyebrow", "title", "intro")}),
        ("Supporting content", {"fields": ("supporting_title", "supporting_text")}),
    )


@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "display_order")
    list_editable = ("display_order",)


@admin.register(InstitutionalValue)
class InstitutionalValueAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order")
    list_editable = ("display_order",)


@admin.register(GovernanceRole)
class GovernanceRoleAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order")
    list_editable = ("display_order",)


@admin.register(StrategicPriority)
class StrategicPriorityAdmin(admin.ModelAdmin):
    list_display = ("title", "metric", "display_order")
    list_editable = ("display_order",)
    search_fields = ("title", "summary", "metric")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "display_order")
    list_filter = ("category", "featured")
    list_editable = ("featured", "display_order")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic information", {"fields": ("category", "title", "slug", "summary")}),
        ("Detailed content", {"fields": ("body",)}),
        ("Display", {"fields": ("featured", "display_order")}),
    )


@admin.register(SDGWorkItem)
class SDGWorkItemAdmin(admin.ModelAdmin):
    list_display = ("title", "goal_number", "featured", "display_order")
    list_filter = ("goal_number", "featured")
    list_editable = ("featured", "display_order")
    search_fields = ("title", "summary", "details")
    fieldsets = (
        (None, {"fields": ("goal_number", "title", "featured", "display_order")}),
        ("Content", {"fields": ("summary", "details")}),
        ("Media", {"fields": ("cover_image", "attachment", "external_url")}),
    )


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "lead_unit", "featured", "display_order")
    list_filter = ("category", "featured")
    list_editable = ("featured", "display_order")
    search_fields = ("title", "summary", "body", "lead_unit")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic information", {"fields": ("category", "title", "slug", "lead_unit", "summary")}),
        ("Detailed content", {"fields": ("body",)}),
        ("Display", {"fields": ("featured", "display_order")}),
    )


@admin.register(EducationInitiative)
class EducationInitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "audience", "featured", "display_order")
    list_filter = ("category", "featured")
    list_editable = ("featured", "display_order")
    search_fields = ("title", "summary", "body", "audience")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic information", {"fields": ("category", "title", "slug", "audience", "summary")}),
        ("Detailed content", {"fields": ("body",)}),
        ("Display", {"fields": ("featured", "display_order")}),
    )


@admin.register(PolicyDocument)
class PolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "publish_date", "featured")
    list_filter = ("category", "featured")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic information", {"fields": ("category", "title", "slug", "publish_date", "summary")}),
        ("Detailed content", {"fields": ("body",)}),
        ("Document source", {"fields": ("file", "external_url", "featured")}),
    )


@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "scope", "display_order")
    list_filter = ("scope",)
    list_editable = ("display_order",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "publish_date", "featured")
    list_filter = ("report_type", "featured")
    search_fields = ("title", "summary", "body", "highlight_metric")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic information", {"fields": ("report_type", "title", "slug", "publish_date", "summary")}),
        ("Detailed content", {"fields": ("body",)}),
        ("Report source", {"fields": ("file", "external_url", "featured")}),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "display_order")
    list_editable = ("display_order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name", "description")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleAdminForm
    change_form_template = "admin/portal/newsarticle/change_form.html"
    list_display = ("news_title", "sdg_goal", "published_on", "featured")
    list_filter = ("sdg_goal", "published_on")
    list_per_page = 25
    search_fields = ("title_uz", "title_en", "summary_uz", "summary_en", "body_uz", "body_en", "title", "summary", "body")
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Yangilik matni", {"fields": ("title_uz", "body_uz"), "classes": ("news-editor-main",), "description": "Kartalardagi qisqacha mazmun yangilik matnidan avtomatik olinadi."}),
        ("Nashr va rasm", {"fields": ("sdg_goal", "published_on", "image", "image_preview"), "classes": ("news-editor-publish",)}),
        ("Inglizcha tarjima (ixtiyoriy)", {"fields": ("title_en", "body_en"), "classes": ("collapse", "news-editor-translation")}),
        ("Qo'shimcha sozlamalar", {"fields": ("category", "featured", "slug"), "classes": ("collapse", "news-editor-options")}),
    )

    @admin.display(description="Yangilik")
    def news_title(self, obj):
        return str(obj)

    def image_preview(self, obj):
        if not obj or not obj.image:
            return "Rasm tanlanganda shu yerda ko'rinadi."
        return format_html(
            '<div style="max-width: 420px;">'
            '<img src="{}" alt="News image preview" style="width: 100%; max-width: 420px; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 12px; border: 1px solid rgba(17, 24, 39, 0.08);" />'
            '<p style="margin: 10px 0 0; color: #52606d; font-size: 12px;">Current preview in a 16:10 crop.</p>'
            "</div>",
            obj.image.url,
        )

    image_preview.short_description = "Rasm ko'rinishi"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "venue", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "details", "venue")
    fieldsets = (
        ("Basic information", {"fields": ("category", "title", "slug", "start_date", "venue", "summary")}),
        ("Detailed content", {"fields": ("details",)}),
        ("Display", {"fields": ("featured",)}),
    )


@admin.register(DepartmentContact)
class DepartmentContactAdmin(admin.ModelAdmin):
    list_display = ("department_name", "contact_person", "phone", "display_order")
    list_editable = ("display_order",)
    search_fields = ("department_name", "contact_person", "email")
    fieldsets = (
        ("Department", {"fields": ("department_name", "contact_person")}),
        ("Contact information", {"fields": ("phone", "email", "office_location", "office_hours")}),
        ("Display", {"fields": ("display_order",)}),
    )


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    readonly_fields = ("full_name", "email", "organization", "subject", "message", "created_at", "updated_at")
    search_fields = ("full_name", "email", "organization", "message")
