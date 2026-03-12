from django.urls import path

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("language/<str:language_code>/", views.set_portal_language, name="set-language"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("sdgs/", views.SDGListView.as_view(), name="sdg-list"),
    path("sdgs/<int:number>/", views.SDGDetailView.as_view(), name="sdg-detail"),
    path("research-education/", views.ResearchEducationView.as_view(), name="research-education"),
    path("campus/", views.CampusView.as_view(), name="campus"),
    path("engagement/", views.EngagementView.as_view(), name="engagement"),
    path("insights/", views.InsightsView.as_view(), name="insights"),
    path("news-events/", views.NewsEventsView.as_view(), name="news-events"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news-detail"),
    path("events/<slug:slug>/", views.EventDetailView.as_view(), name="event-detail"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
