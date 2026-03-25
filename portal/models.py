from django.db import models
from django.urls import reverse
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return


class SiteSettings(SingletonModel, TimeStampedModel):
    institution_name = models.TextField(default="Sustainable Development Governance Platform")
    institution_short_name = models.TextField(default="SDG")
    tagline = models.TextField(default="Official institutional platform for sustainability governance, policy, and public reporting")
    official_badge = models.TextField(default="Official Institutional Portal")
    navbar_cta_label = models.TextField(default="Reports Center")
    navbar_cta_url = models.TextField(default="/reports-insights/")
    hero_kicker = models.TextField(default="National-scale institutional platform")
    hero_title = models.TextField(default="A premium institutional portal for sustainability leadership, education, and evidence-based public accountability.")
    hero_description = models.TextField(default="This platform presents official strategy, flagship programs, research portfolios, educational initiatives, public reports, and stakeholder engagement in a unified and trusted digital environment.")
    hero_primary_label = models.TextField(default="Explore Strategic Priorities")
    hero_primary_url = models.TextField(default="/programs/")
    hero_secondary_label = models.TextField(default="View Reports & Insights")
    hero_secondary_url = models.TextField(default="/reports-insights/")
    overview_title = models.TextField(default="Institutional overview")
    overview_text = models.TextField(default="The platform aligns academic excellence, policy implementation, research leadership, and public service through a structured sustainability agenda designed for large-scale institutions.")
    mission = models.TextField(default="To lead a transparent, research-driven, and future-oriented sustainability transformation across education, governance, operations, and public partnerships.")
    vision = models.TextField(default="To become a benchmark institutional platform where trust, evidence, innovation, and strategic coordination advance long-term sustainable development outcomes.")
    strategic_approach = models.TextField(default="Our strategic approach combines executive governance, measurable performance indicators, flagship programs, applied research, and stakeholder-facing reporting under one integrated digital architecture.")
    governance_overview = models.TextField(default="Governance is coordinated through senior leadership, policy committees, implementation teams, and data stewards responsible for delivery quality and institutional accountability.")
    strategy_overview = models.TextField(default="The strategy focuses on resilient infrastructure, climate-aware planning, inclusive education, data-led management, and cross-sector collaboration.")
    leader_name = models.TextField(default="Nabiyev Dilmurod Xamidullayevich")
    leader_title = models.TextField(default="Qarshi davlat universiteti rektori, iqtisod fanlari doktori, professor")
    leader_photo = models.FileField(upload_to="leaders/", blank=True)
    leader_message = models.TextField(default="We are building a platform that reflects institutional maturity: one that is rigorous in governance, clear in communication, confident in design, and accountable in results. Every section of this portal is structured to strengthen trust among students, researchers, partners, public bodies, and international stakeholders.")
    leader_signature = models.TextField(default="Leadership Office")
    address = models.TextField(default="12 Mustaqillik Avenue, Tashkent, Uzbekistan")
    phone = models.TextField(default="+998 71 000 50 50")
    email = models.EmailField(default="office@institution.uz")
    office_hours = models.TextField(default="Monday-Friday, 09:00-18:00")
    map_embed_url = models.URLField(blank=True)
    footer_text = models.TextField(default="Built for official communication, public accountability, and coordinated institutional execution.")
    meta_title = models.TextField(default="Sustainable Development Governance Platform")
    meta_description = models.TextField(default="Official premium institutional web platform for sustainability strategy, programs, research, education, reports, and stakeholder engagement.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.institution_name


class PageContent(TimeStampedModel):
    class PageKey(models.TextChoices):
        HOME = "home", "Home"
        ABOUT = "about", "About"
        PROGRAMS = "programs", "Goals / Programs / Services"
        RESEARCH = "research", "Research / Projects"
        EDUCATION = "education", "Education / Initiatives"
        SUSTAINABILITY = "sustainability", "Sustainability / Strategy / Policy"
        REPORTS = "reports", "Reports & Insights"
        NEWS = "news", "News & Events"
        CONTACT = "contact", "Contact"

    page_key = models.CharField(max_length=30, choices=PageKey.choices, unique=True)
    eyebrow = models.TextField()
    title = models.TextField()
    intro = models.TextField()
    supporting_title = models.TextField(blank=True)
    supporting_text = models.TextField(blank=True)
    cta_title = models.TextField(blank=True)
    cta_text = models.TextField(blank=True)
    cta_primary_label = models.TextField(blank=True)
    cta_primary_url = models.TextField(blank=True)
    cta_secondary_label = models.TextField(blank=True)
    cta_secondary_url = models.TextField(blank=True)
    meta_title = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        ordering = ["page_key"]
        verbose_name = "Page content"
        verbose_name_plural = "Page contents"

    def __str__(self):
        return self.get_page_key_display()


class HeroStat(TimeStampedModel):
    value = models.TextField()
    label = models.TextField()
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"


class InstitutionalValue(TimeStampedModel):
    title = models.TextField()
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class GovernanceRole(TimeStampedModel):
    title = models.TextField()
    responsibility = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class StrategicPriority(TimeStampedModel):
    icon = models.CharField(max_length=40, default="compass")
    title = models.TextField()
    summary = models.TextField()
    metric = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class Program(TimeStampedModel):
    class Category(models.TextChoices):
        GOAL = "goal", "Strategic Goal"
        PROGRAM = "program", "Flagship Program"
        SERVICE = "service", "Institutional Service"

    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    outcome_value = models.TextField(blank=True)
    outcome_label = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class SDGWorkItem(TimeStampedModel):
    GOAL_CHOICES = [(number, f"SDG {number}") for number in range(1, 18)]

    goal_number = models.PositiveSmallIntegerField(choices=GOAL_CHOICES)
    title = models.TextField()
    summary = models.TextField()
    details = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="sdg_work_items/", blank=True)
    attachment = models.FileField(upload_to="sdg_work_items/attachments/", blank=True)
    external_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["goal_number", "display_order", "title"]
        verbose_name = "SDG work item"
        verbose_name_plural = "SDG work items"

    def __str__(self):
        return f"SDG {self.goal_number}: {self.title}"

    def get_absolute_url(self):
        return reverse("sdg-detail", kwargs={"number": self.goal_number})


class ResearchProject(TimeStampedModel):
    class Category(models.TextChoices):
        RESEARCH = "research", "Research Program"
        PROJECT = "project", "Strategic Project"
        LAB = "lab", "Laboratory / Center"
        COLLABORATION = "collaboration", "Partnership Project"

    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    lead_unit = models.TextField()
    timeframe = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class EducationInitiative(TimeStampedModel):
    class Category(models.TextChoices):
        CURRICULUM = "curriculum", "Curriculum"
        TRAINING = "training", "Training"
        FELLOWSHIP = "fellowship", "Fellowship"
        OUTREACH = "outreach", "Public Initiative"

    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    audience = models.TextField()
    delivery_model = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class PolicyDocument(TimeStampedModel):
    class Category(models.TextChoices):
        STRATEGY = "strategy", "Strategy"
        POLICY = "policy", "Policy"
        FRAMEWORK = "framework", "Framework"
        REGULATION = "regulation", "Regulation"

    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    publish_date = models.DateField()
    effective_period = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    file = models.FileField(upload_to="policies/", blank=True)
    external_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-publish_date", "title"]

    def __str__(self):
        return self.title


class ImpactMetric(TimeStampedModel):
    class Scope(models.TextChoices):
        HOME = "home", "Home"
        REPORTS = "reports", "Reports"
        BOTH = "both", "Both"

    label = models.TextField()
    value = models.TextField()
    description = models.TextField()
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.BOTH)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "label"]

    def __str__(self):
        return self.label


class Report(TimeStampedModel):
    class ReportType(models.TextChoices):
        ANNUAL = "annual", "Annual report"
        INSIGHT = "insight", "Insight brief"
        RANKING = "ranking", "Ranking submission"
        DASHBOARD = "dashboard", "Data dashboard"

    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    publish_date = models.DateField()
    highlight_metric = models.TextField(blank=True)
    file = models.FileField(upload_to="reports/", blank=True)
    external_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-publish_date", "title"]

    def __str__(self):
        return self.title


class Achievement(TimeStampedModel):
    title = models.TextField()
    subtitle = models.TextField(blank=True)
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class Partner(TimeStampedModel):
    name = models.TextField()
    partner_type = models.TextField()
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class NewsArticle(TimeStampedModel):
    class Category(models.TextChoices):
        OFFICIAL = "official", "Official update"
        RESEARCH = "research", "Research"
        PROGRAM = "program", "Program"
        EVENT = "event", "Event"

    title = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    body = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True)
    published_on = models.DateField()
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_on", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news-detail", kwargs={"slug": self.slug})


class Event(TimeStampedModel):
    class Category(models.TextChoices):
        FORUM = "forum", "Forum"
        CONFERENCE = "conference", "Conference"
        WORKSHOP = "workshop", "Workshop"
        BRIEFING = "briefing", "Briefing"

    title = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    summary = models.TextField()
    details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    venue = models.TextField()
    audience = models.TextField()
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_date", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"slug": self.slug})


class DepartmentContact(TimeStampedModel):
    department_name = models.CharField(max_length=160)
    contact_person = models.CharField(max_length=120)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    office_location = models.CharField(max_length=160)
    office_hours = models.CharField(max_length=120)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "department_name"]

    def __str__(self):
        return self.department_name


class ContactSubmission(TimeStampedModel):
    class Subject(models.TextChoices):
        GENERAL = "general", "General inquiry"
        PARTNERSHIP = "partnership", "Partnership request"
        MEDIA = "media", "Media and communications"
        REPORT = "report", "Report and data request"

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    organization = models.CharField(max_length=160, blank=True)
    subject = models.CharField(max_length=20, choices=Subject.choices)
    message = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.get_subject_display()}"
