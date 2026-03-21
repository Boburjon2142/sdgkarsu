import logging

from .models import AuditLog


audit_logger = logging.getLogger("apps.audit")


def record_audit_event(request, action, user=None, target=None, metadata=None):
    metadata = metadata or {}
    if user is None and request and getattr(request, "user", None) and request.user.is_authenticated:
        user = request.user

    target_type = ""
    target_id = ""
    if target is not None:
        target_type = target.__class__.__name__
        target_id = str(getattr(target, "pk", ""))

    AuditLog.objects.create(
        actor=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        ip_address=_get_client_ip(request),
        user_agent=(request.META.get("HTTP_USER_AGENT", "")[:255] if request else ""),
        metadata=metadata,
    )
    audit_logger.info("audit action=%s target=%s target_id=%s", action, target_type, target_id)


def _get_client_ip(request):
    if not request:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
