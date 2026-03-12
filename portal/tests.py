from django.test import TestCase

from .forms import ContactSubmissionForm
from .models import ContactSubmission, SDG, SiteSettings


class PortalModelAndFormTests(TestCase):
    def test_seeded_site_settings_exist(self):
        self.assertTrue(SiteSettings.objects.exists())

    def test_contact_form_saves_submission(self):
        form = ContactSubmissionForm(
            data={
                "full_name": "Amina Akbarova",
                "email": "amina@example.com",
                "organization": "Regional NGO",
                "subject": "partnership",
                "message": "We would like to discuss a community water stewardship partnership.",
            }
        )
        self.assertTrue(form.is_valid())
        submission = form.save()
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertEqual(submission.subject, "partnership")

    def test_sdg_absolute_url(self):
        sdg = SDG.objects.get(number=4)
        self.assertEqual(sdg.get_absolute_url(), "/sdgs/4/")

# Create your tests here.
