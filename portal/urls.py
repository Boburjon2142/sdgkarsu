from django.urls import path

from .views import (
    AboutView,
    ContactView,
    EducationView,
    EventDetailView,
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
    path("health/", health_check, name="health-check"),
    path("robots.txt", robots_txt, name="robots-txt"),
]
