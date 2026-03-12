from django.contrib import admin

from .models import (
    CampusInitiative,
    ContactSubmission,
    EngagementInitiative,
    Event,
    GovernanceRole,
    InsightMetric,
    NewsArticle,
    Partner,
    ResearchItem,
    SDG,
    SDGProject,
    SiteSettings,
    SustainabilityPolicy,
    SustainabilityReport,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "contact_phone")
    fieldsets = (
        ("Branding", {"fields": ("site_name", "short_name", "tagline")}),
        ("Hero", {"fields": ("hero_background_image", "hero_title", "hero_text")}),
        ("Leadership", {"fields": ("rector_name", "rector_title", "rector_message")}),
        ("Strategy", {"fields": ("sustainability_strategy", "governance_overview")}),
        ("Contact", {"fields": ("contact_address", "contact_phone", "contact_email", "office_hours")}),
    )


@admin.register(GovernanceRole)
class GovernanceRoleAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order")
    list_editable = ("display_order",)


@admin.register(SustainabilityPolicy)
class SustainabilityPolicyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_on")
    list_filter = ("category",)
    search_fields = ("title", "summary")


@admin.register(SustainabilityReport)
class SustainabilityReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "publish_date")
    list_filter = ("report_type",)
    search_fields = ("title", "summary")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "display_order")
    list_editable = ("display_order",)


class SDGProjectInline(admin.TabularInline):
    model = SDGProject
    extra = 0


@admin.register(SDG)
class SDGAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "featured")
    list_editable = ("featured",)
    inlines = [SDGProjectInline]


@admin.register(ResearchItem)
class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "department")
    list_filter = ("category",)
    search_fields = ("title", "summary", "department")


@admin.register(CampusInitiative)
class CampusInitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "metric")
    list_filter = ("category",)


@admin.register(EngagementInitiative)
class EngagementInitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "audience")
    list_filter = ("category",)


@admin.register(InsightMetric)
class InsightMetricAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "page_scope", "display_order")
    list_editable = ("display_order",)
    list_filter = ("page_scope",)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_on", "featured")
    list_filter = ("category", "featured")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "body")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "venue")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "details")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "submitted_at")
    readonly_fields = ("full_name", "email", "organization", "subject", "message", "submitted_at")
    search_fields = ("full_name", "email", "organization", "message")

# Register your models here.
