from django import forms

from .models import ContactSubmission
from .translation_utils import translate_text


class ContactSubmissionForm(forms.ModelForm):
    def __init__(self, *args, language_code="en", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].label = translate_text("Full name", language_code)
        self.fields["email"].label = translate_text("Email address", language_code)
        self.fields["organization"].label = translate_text("Organization", language_code)
        self.fields["subject"].label = translate_text("Subject", language_code)
        self.fields["message"].label = translate_text("Message", language_code)
        self.fields["subject"].choices = [
            (value, translate_text(label, language_code)) for value, label in self.fields["subject"].choices
        ]

    class Meta:
        model = ContactSubmission
        fields = ["full_name", "email", "organization", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }
