from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from portal.image_uploads import webp_content


class Command(BaseCommand):
    help = "Convert existing uploaded raster images to WebP; retain original files."

    def handle(self, *args, **options):
        count = 0
        for model in apps.get_app_config("portal").get_models():
            fields = [field for field in model._meta.fields if isinstance(field, models.FileField)]
            for instance in model.objects.iterator():
                for field in fields:
                    upload = getattr(instance, field.name)
                    if not upload or Path(upload.name).suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"}:
                        continue
                    try:
                        with upload.open("rb") as source:
                            converted = webp_content(source)
                        original = upload.name
                        upload.save(f"{Path(original).stem}.webp", converted, save=False)
                        # Preserve content timestamps and retain the original for rollback.
                        model.objects.filter(pk=instance.pk).update(**{field.name: upload.name})
                        count += 1
                        self.stdout.write(f"{original} -> {upload.name}")
                    except (OSError, ValueError) as exc:
                        self.stderr.write(f"Skipped {model.__name__} #{instance.pk}: {exc}")
        self.stdout.write(self.style.SUCCESS(f"Converted {count} uploaded images."))
