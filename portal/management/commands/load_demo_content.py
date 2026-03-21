from datetime import date, timedelta
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from portal.models import NewsArticle, SDGWorkItem, SiteSettings


BASE_DIR = Path(__file__).resolve().parents[3]
ASSETS_DIR = BASE_DIR / "assets" / "images"
GOALS_DIR = ASSETS_DIR / "goals"


class Command(BaseCommand):
    help = (
        "Load demo content with bundled local images for news, SDG work items, "
        "and site settings. Suitable for first-time setup on PythonAnywhere or local environments."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Replace existing demo news and SDG work items before loading new demo content.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            NewsArticle.objects.filter(slug__startswith="demo-").delete()
            SDGWorkItem.objects.filter(title__startswith="Demo:").delete()
            self.stdout.write(self.style.WARNING("Existing demo records were removed."))

        site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
        self._assign_file(site_settings, "leader_photo", ASSETS_DIR / "rektor.jpg")

        self._seed_news()
        self._seed_sdg_work_items()

        self.stdout.write(self.style.SUCCESS("Demo content with images loaded successfully."))

    def _seed_news(self):
        news_items = [
            {
                "slug": "demo-institutional-reporting-framework-launch",
                "title": "Official launch of the institutional reporting framework",
                "category": NewsArticle.Category.OFFICIAL,
                "summary": "The university launched a new reporting framework to unify sustainability evidence, metrics, and governance disclosures.",
                "body": (
                    "This demo article shows how a production news card looks with a real image. "
                    "It can be edited later from the admin panel and replaced with official content."
                ),
                "published_on": date.today(),
                "featured": True,
                "image_path": ASSETS_DIR / "hero-back.jpg",
            },
            {
                "slug": "demo-research-governance-portfolio-expansion",
                "title": "Research platform expands applied climate governance portfolio",
                "category": NewsArticle.Category.RESEARCH,
                "summary": "A new group of applied research initiatives was approved to support governance, impact tracking, and sustainability strategy.",
                "body": (
                    "This demo entry is designed to populate the research/news experience with a high-quality image. "
                    "Editors can update its text and keep the media structure as-is."
                ),
                "published_on": date.today() - timedelta(days=5),
                "featured": False,
                "image_path": GOALS_DIR / "E_WEB_13.png",
            },
            {
                "slug": "demo-operations-program-delivery-phase",
                "title": "Flagship operations program enters new implementation phase",
                "category": NewsArticle.Category.PROGRAM,
                "summary": "Operational milestones for the sustainability roadmap were refreshed and a new implementation cycle started.",
                "body": (
                    "This article exists as demo content so the homepage and news section always have polished visuals "
                    "during development, presentations, or first deployment."
                ),
                "published_on": date.today() - timedelta(days=12),
                "featured": False,
                "image_path": GOALS_DIR / "E_WEB_11.png",
            },
        ]

        for item in news_items:
            article, _ = NewsArticle.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "body": item["body"],
                    "published_on": item["published_on"],
                    "featured": item["featured"],
                },
            )
            self._assign_file(article, "image", item["image_path"])

    def _seed_sdg_work_items(self):
        work_items = [
            {
                "goal_number": 4,
                "title": "Demo: Inclusive education outreach campaign",
                "summary": "A sample SDG 4 work item showing how campus initiatives appear with media on the updates page.",
                "details": "Use this item as a placeholder until official university work is uploaded by the admin team.",
                "display_order": 1,
                "featured": True,
                "image_path": GOALS_DIR / "E_WEB_04.png",
            },
            {
                "goal_number": 11,
                "title": "Demo: Sustainable campus mobility pilot",
                "summary": "Illustrates an SDG 11 update card with image support and polished presentation.",
                "details": "Suitable for demonstrating card layout, image crop, and detail content in admin previews.",
                "display_order": 1,
                "featured": True,
                "image_path": GOALS_DIR / "E_WEB_11.png",
            },
            {
                "goal_number": 13,
                "title": "Demo: Climate action awareness week",
                "summary": "Shows how climate-related activities can be presented with a high-quality visual.",
                "details": "This sample can be edited later into a real SDG 13 initiative without changing the structure.",
                "display_order": 1,
                "featured": True,
                "image_path": GOALS_DIR / "E_WEB_13.png",
            },
        ]

        for item in work_items:
            work_item, _ = SDGWorkItem.objects.update_or_create(
                goal_number=item["goal_number"],
                title=item["title"],
                defaults={
                    "summary": item["summary"],
                    "details": item["details"],
                    "display_order": item["display_order"],
                    "featured": item["featured"],
                },
            )
            self._assign_file(work_item, "cover_image", item["image_path"])

    def _assign_file(self, instance, field_name, source_path):
        if not source_path.exists():
            self.stdout.write(self.style.WARNING(f"Missing asset: {source_path}"))
            return

        field = getattr(instance, field_name)
        current_name = Path(field.name).name if field and field.name else ""
        target_name = source_path.name
        if current_name == target_name:
            return

        with source_path.open("rb") as source_file:
            field.save(target_name, File(source_file), save=False)

        instance.save()
