from django import forms

from .models import ContactSubmission
from .translation_utils import translate_text


class ContactSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["full_name", "email", "organization", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@organization.uz"}),
            "organization": forms.TextInput(attrs={"placeholder": "Institution or organization"}),
            "subject": forms.Select(),
            "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Describe your request, partnership proposal, or information need."}),
        }

    def __init__(self, *args, language_code="en", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].label = translate_text("Full name", language_code)
        self.fields["email"].label = translate_text("Email", language_code)
        self.fields["organization"].label = translate_text("Organization", language_code)
        self.fields["subject"].label = translate_text("Subject", language_code)
        self.fields["message"].label = translate_text("Message", language_code)
        self.fields["full_name"].widget.attrs["placeholder"] = translate_text("Full name", language_code)
        self.fields["email"].widget.attrs["placeholder"] = translate_text("Email address", language_code)
        self.fields["organization"].widget.attrs["placeholder"] = translate_text("Institution or organization", language_code)
        self.fields["message"].widget.attrs["placeholder"] = translate_text(
            "Describe your request, partnership proposal, or information need.",
            language_code,
        )
        self.fields["subject"].choices = [
            (value, translate_text(label, language_code)) for value, label in self.fields["subject"].choices
        ]
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
