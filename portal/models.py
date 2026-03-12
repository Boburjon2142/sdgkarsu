from django.db import models
from django.urls import reverse


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=40, default="SDG")
    tagline = models.CharField(max_length=255)
    hero_background_image = models.FileField(upload_to="hero/", blank=True)
    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField()
    rector_name = models.CharField(max_length=120)
    rector_title = models.CharField(max_length=120)
    rector_message = models.TextField()
    sustainability_strategy = models.TextField()
    governance_overview = models.TextField()
    contact_address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=50)
    contact_email = models.EmailField()
    office_hours = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self) -> str:
        return self.site_name


class GovernanceRole(models.Model):
    title = models.CharField(max_length=120)
    responsibility = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self) -> str:
        return self.title


class SustainabilityPolicy(models.Model):
    class Category(models.TextChoices):
        ENVIRONMENT = "environment", "Environment"
        EDUCATION = "education", "Education"
        PROCUREMENT = "procurement", "Procurement"
        RESEARCH = "research", "Research"
        RISK = "risk", "Risk"
        DISCLOSURE = "disclosure", "Disclosure"

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    published_on = models.DateField()

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class SustainabilityReport(models.Model):
    class ReportType(models.TextChoices):
        ANNUAL = "annual", "Annual Report"
        RANKING = "ranking", "Ranking Submission"
        DASHBOARD = "dashboard", "Dashboard"
        POLICY = "policy", "Policy Digest"

    title = models.CharField(max_length=180)
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    summary = models.TextField()
    publish_date = models.DateField()
    download_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self) -> str:
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=160)
    partner_type = models.CharField(max_length=80)
    website = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        return self.name


class SDG(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=255)
    overview = models.TextField()
    university_actions = models.TextField()
    indicators = models.TextField()
    color_class = models.CharField(max_length=20)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return f"SDG {self.number}: {self.title}"

    def get_absolute_url(self):
        return reverse("sdg-detail", kwargs={"number": self.number})


class SDGProject(models.Model):
    sdg = models.ForeignKey(SDG, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=160)
    summary = models.TextField()
    project_type = models.CharField(max_length=80)

    class Meta:
        ordering = ["sdg__number", "title"]

    def __str__(self) -> str:
        return self.title


class ResearchItem(models.Model):
    class Category(models.TextChoices):
        PROJECT = "project", "SDG Research Project"
        PUBLICATION = "publication", "SDG Publication"
        CENTER = "center", "Research Center"
        INNOVATION = "innovation", "Innovation and Startup"
        GRANT = "grant", "Grant and Funding"
        COURSE = "course", "SDG-related Course"
        PROGRAM = "program", "Degree Program"
        STUDENT = "student", "Student Project"
        MOOC = "mooc", "MOOC / Training"

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    department = models.CharField(max_length=120, blank=True)
    highlight_metric = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self) -> str:
        return self.title


class CampusInitiative(models.Model):
    class Category(models.TextChoices):
        GREEN = "green", "Green Campus"
        ENERGY = "energy", "Energy & Climate"
        WASTE = "waste", "Waste Management"
        WATER = "water", "Water Management"
        TRANSPORT = "transport", "Sustainable Transportation"
        BUILDING = "building", "Green Buildings"
        BIODIVERSITY = "biodiversity", "Biodiversity"

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    metric = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self) -> str:
        return self.title


class EngagementInitiative(models.Model):
    class Category(models.TextChoices):
        SOCIAL = "social", "Social Impact Project"
        VOLUNTEER = "volunteer", "Volunteer Program"
        GOVERNMENT = "government", "Government Partnership"
        INDUSTRY = "industry", "Industry Collaboration"
        TRAINING = "training", "Community Training"

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    audience = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self) -> str:
        return self.title


class InsightMetric(models.Model):
    class PageScope(models.TextChoices):
        HOME = "home", "Home"
        INSIGHTS = "insights", "Insights"
        BOTH = "both", "Both"

    label = models.CharField(max_length=160)
    value = models.CharField(max_length=40)
    context = models.CharField(max_length=200)
    page_scope = models.CharField(max_length=20, choices=PageScope.choices, default=PageScope.BOTH)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "label"]

    def __str__(self) -> str:
        return self.label


class NewsArticle(models.Model):
    class Category(models.TextChoices):
        POLICY = "policy", "Policy Update"
        RESEARCH = "research", "Research"
        CAMPUS = "campus", "Campus"
        ENGAGEMENT = "engagement", "Engagement"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    body = models.TextField()
    published_on = models.DateField()
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_on", "title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("news-detail", kwargs={"slug": self.slug})


class Event(models.Model):
    class Category(models.TextChoices):
        EVENT = "event", "Event"
        CONFERENCE = "conference", "Conference"
        WORKSHOP = "workshop", "Workshop"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    details = models.TextField()
    start_date = models.DateField()
    venue = models.CharField(max_length=160)
    audience = models.CharField(max_length=160)

    class Meta:
        ordering = ["start_date", "title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"slug": self.slug})


class ContactSubmission(models.Model):
    class Subject(models.TextChoices):
        GENERAL = "general", "General inquiry"
        PARTNERSHIP = "partnership", "Partnership request"
        REPORT = "report", "Report request"
        STUDENT = "student", "Student engagement"

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    organization = models.CharField(max_length=160, blank=True)
    subject = models.CharField(max_length=20, choices=Subject.choices)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_subject_display()}"
