from django.conf import settings
from django.urls import path
from django.views.static import serve

from .views import (
    AboutView,
    AntiCorruptionContactView,
    ContactView,
    EducationView,
    ethics_code_document,
    EventDetailView,
    GovernanceDetailView,
    HomeView,
    NewsDetailView,
    NewsEventsView,
    ProgramsView,
    ReportsView,
    ResearchView,
    SDGDetailView,
    SDGUpdatesView,
    SustainabilityView,
    health_check,
    robots_txt,
    set_portal_language,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("language/<str:language_code>/", set_portal_language, name="set-language"),
    path("about/", AboutView.as_view(), name="about"),
    path("about/<slug:slug>/", GovernanceDetailView.as_view(), name="governance-detail"),
    path("about/anti-corruption/contact/", AntiCorruptionContactView.as_view(), name="anti-corruption-contact"),
    path("about/ethics-code/document/", ethics_code_document, name="ethics-code-document"),
    path("programs/", ProgramsView.as_view(), name="programs"),
    path("programs/sdg-<int:number>/", SDGDetailView.as_view(), name="sdg-detail"),
    path("programs/sdg-<int:number>/updates/", SDGUpdatesView.as_view(), name="sdg-updates"),
    path("research-projects/", ResearchView.as_view(), name="research"),
    path("education-initiatives/", EducationView.as_view(), name="education"),
    path("sustainability-strategy/", SustainabilityView.as_view(), name="sustainability"),
    path("reports-insights/", ReportsView.as_view(), name="reports"),
    path("news-events/", NewsEventsView.as_view(), name="news-events"),
    path("news/<slug:slug>/", NewsDetailView.as_view(), name="news-detail"),
    path("events/<slug:slug>/", EventDetailView.as_view(), name="event-detail"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("meedia/<path:path>", serve, {"document_root": settings.BASE_DIR / "meedia"}),
    path("health/", health_check, name="health-check"),
    path("robots.txt", robots_txt, name="robots-txt"),
]
