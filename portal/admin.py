from django import forms
from django.contrib import admin
from django.utils.html import format_html

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
            "image": "Recommended size: 1600 x 1000 px (16:10), landscape. 1200 x 750 px also works well. Keep the main subject near the center because the card uses cover cropping.",
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("institution_name", "email", "phone")
    fieldsets = (
        ("Brand", {"fields": ("institution_name", "institution_short_name", "tagline", "official_badge")}),
        ("Navigation", {"fields": ("navbar_cta_label", "navbar_cta_url")}),
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
        ("Institutional narrative", {"fields": ("overview_title", "overview_text", "mission", "vision", "strategic_approach", "governance_overview", "strategy_overview")}),
        ("Leadership", {"fields": ("leader_name", "leader_title", "leader_photo", "leader_message", "leader_signature")}),
        ("Contact and footer", {"fields": ("address", "phone", "email", "office_hours", "map_embed_url", "footer_text")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("page_key", "title", "eyebrow")
    search_fields = ("title", "intro", "supporting_text")


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


@admin.register(EducationInitiative)
class EducationInitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "audience", "featured", "display_order")
    list_filter = ("category", "featured")
    list_editable = ("featured", "display_order")
    search_fields = ("title", "summary", "body", "audience")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PolicyDocument)
class PolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "publish_date", "featured")
    list_filter = ("category", "featured")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}


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
    list_display = ("title", "category", "published_on", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "body")
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "featured")}),
        ("Content", {"fields": ("summary", "body", "image", "image_preview")}),
        ("Publishing", {"fields": ("published_on",)}),
    )

    def image_preview(self, obj):
        if not obj or not obj.image:
            return "Image preview will appear after upload."
        return format_html(
            '<div style="max-width: 420px;">'
            '<img src="{}" alt="News image preview" style="width: 100%; max-width: 420px; aspect-ratio: 16 / 10; object-fit: cover; border-radius: 12px; border: 1px solid rgba(17, 24, 39, 0.08);" />'
            '<p style="margin: 10px 0 0; color: #52606d; font-size: 12px;">Current preview in a 16:10 crop.</p>'
            "</div>",
            obj.image.url,
        )

    image_preview.short_description = "Preview"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "venue", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "details", "venue")


@admin.register(DepartmentContact)
class DepartmentContactAdmin(admin.ModelAdmin):
    list_display = ("department_name", "contact_person", "phone", "display_order")
    list_editable = ("display_order",)
    search_fields = ("department_name", "contact_person", "email")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    readonly_fields = ("full_name", "email", "organization", "subject", "message", "created_at", "updated_at")
    search_fields = ("full_name", "email", "organization", "message")


admin.site.site_header = "Institutional Portal Administration"
admin.site.site_title = "Portal Admin"
admin.site.index_title = "Content management"
