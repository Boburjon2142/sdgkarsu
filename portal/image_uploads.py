from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


def webp_content(source):
    """Keep dimensions, orientation, transparency and animation of uploaded images."""
    with Image.open(source) as image:
        output = BytesIO()
        if getattr(image, "is_animated", False):
            frames, durations = [], []
            for index in range(image.n_frames):
                image.seek(index)
                frames.append(image.convert("RGBA"))
                durations.append(image.info.get("duration", 100))
            frames[0].save(
                output, "WEBP", save_all=True, append_images=frames[1:],
                duration=durations, loop=image.info.get("loop", 0), quality=85,
            )
        else:
            ImageOps.exif_transpose(image).convert("RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB").save(
                output, "WEBP", quality=85, method=4,
            )
        return ContentFile(output.getvalue())


@receiver(pre_save, dispatch_uid="portal_webp_uploads")
def optimize_uploaded_images(sender, instance, raw=False, update_fields=None, **kwargs):
    if raw or sender._meta.app_label != "portal":
        return
    for field in sender._meta.fields:
        if not isinstance(field, models.FileField) or (update_fields is not None and field.name not in update_fields):
            continue
        upload = getattr(instance, field.name)
        if not upload or upload._committed:
            continue
        if Path(upload.name).suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"}:
            continue
        try:
            upload.seek(0)
            converted = webp_content(upload)
        except (UnidentifiedImageError, OSError, ValueError):
            upload.seek(0)
            continue
        upload.save(f"{Path(upload.name).stem}.webp", converted, save=False)
