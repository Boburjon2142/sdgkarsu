from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .image_uploads import webp_content
from .models import SiteSettings


class ImageOptimizationTests(TestCase):
    def test_upload_is_webp_and_keeps_dimensions_and_transparency(self):
        source = BytesIO()
        Image.new("RGBA", (120, 80), (30, 90, 20, 100)).save(source, "PNG")
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            settings = SiteSettings.objects.get(pk=1)
            settings.leader_photo = SimpleUploadedFile("portrait.png", source.getvalue(), "image/png")
            settings.save()
            settings.refresh_from_db()
            self.assertTrue(settings.leader_photo.name.endswith(".webp"))
            with settings.leader_photo.open() as file, Image.open(file) as image:
                self.assertEqual(image.format, "WEBP")
                self.assertEqual(image.size, (120, 80))
                self.assertIn("A", image.getbands())

    def test_animation_keeps_frames_and_timing(self):
        source = BytesIO()
        Image.new("RGB", (20, 20), "red").save(
            source, "GIF", save_all=True,
            append_images=[Image.new("RGB", (20, 20), "blue")],
            duration=[100, 200], loop=0,
        )
        source.seek(0)
        result = webp_content(source)
        with Image.open(result) as image:
            self.assertEqual(image.n_frames, 2)
            self.assertEqual(image.size, (20, 20))
