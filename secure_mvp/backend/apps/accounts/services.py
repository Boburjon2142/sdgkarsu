from django.contrib.auth import login, logout

from apps.common.audit import record_audit_event


def login_user(request, user):
    login(request, user)
    record_audit_event(request, "auth.logged_in", user=user, target=user)


def logout_user(request):
    if request.user.is_authenticated:
        record_audit_event(request, "auth.logged_out", user=request.user, target=request.user)
    logout(request)


def register_user(request, user):
    login(request, user)
    record_audit_event(request, "auth.registered", user=user, target=user)
