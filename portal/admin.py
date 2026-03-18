from django.contrib import admin

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
    SiteSettings,
    StrategicPriority,
)


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


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
        ("Leadership", {"fields": ("leader_name", "leader_title", "leader_message", "leader_signature")}),
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
    list_display = ("title", "category", "published_on", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "body")


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
