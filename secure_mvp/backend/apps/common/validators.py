from pathlib import Path

from django.core.exceptions import ValidationError


ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def validate_secure_upload(file_obj):
    extension = Path(file_obj.name).suffix.lower()
    if extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError("Unsupported file extension.")
    if getattr(file_obj, "size", 0) > MAX_UPLOAD_SIZE:
        raise ValidationError("File exceeds the 5 MB size limit.")
    content_type = getattr(file_obj, "content_type", "")
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError("Unsupported file type.")
