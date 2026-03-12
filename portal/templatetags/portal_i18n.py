from django import template
from django.utils.safestring import mark_safe

from portal.translation_utils import translate_text

register = template.Library()


SDG_ICONS = {
    1: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="16" cy="15" r="4"/><circle cx="32" cy="15" r="4"/><circle cx="48" cy="15" r="4"/><path d="M16 22v16m-5 7 5-7 5 7m11-23v23m-7-13h14m9-10v16m-5 7 5-7 5 7"/></g></svg>
    """,
    2: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 28h28c-2 10-8 17-14 17s-12-7-14-17Z"/><path d="M13 49h38"/><path d="M23 12c0 4-3 4-3 8s3 4 3 8m9-16c0 4-3 4-3 8s3 4 3 8m9-16c0 4-3 4-3 8s3 4 3 8"/></g></svg>
    """,
    3: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 35h13l5-11 8 24 8-19 10 6"/><path d="m50 18 4 4-4 4-4-4 4-4Z"/></g></svg>
    """,
    4: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 18c8 0 13 2 20 7 7-5 12-7 20-7v28c-8 0-13 2-20 7-7-5-12-7-20-7V18Z"/><path d="M32 25v28"/></g></svg>
    """,
    5: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="25" cy="23" r="10"/><path d="M35 13 52 6m-8 0h8v8M25 33v24m-9-8h18"/></g></svg>
    """,
    6: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 16h28l-3 18H21l-3-18Z"/><path d="m32 39 7 10a8 8 0 1 1-14 0l7-10Z"/><path d="M24 34v8m16-8v8"/></g></svg>
    """,
    7: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="10"/><path d="M32 8v8m0 32v8M8 32h8m32 0h8m-41-17 6 4m22 26 6 4m0-34-6 4M21 45l-6 4"/><path d="M32 26v7l4 3"/></g></svg>
    """,
    8: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 48V30m14 18V22m14 26V14"/><path d="M8 48h40"/><path d="m28 34 10-10 8 8 10-14"/></g></svg>
    """,
    9: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"><path d="m16 20 12-7 12 7v14l-12 7-12-7V20Zm12 21v14m-12-7 12 7 12-7m4-28 12-7 12 7v14l-12 7-12-7V20Zm12 21v14m-12-7 12 7 12-7"/></g></svg>
    """,
    10: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M16 20h32M16 32h32M16 44h32"/><path d="m10 20 6-6v12l-6-6Zm44 0 6-6v12l-6-6ZM10 44l6-6v12l-6-6Zm44 0 6-6v12l-6-6Z"/></g></svg>
    """,
    11: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"><path d="M10 52V34l10-8v26H10Zm16 0V14h12v38H26Zm18 0V24h10v28H44Zm-39 0h54"/></g></svg>
    """,
    12: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 22a14 14 0 1 0 10 24"/><path d="m18 16 4 6-7 1m34 19a14 14 0 1 0-10-24"/><path d="m46 48-4-6 7-1"/></g></svg>
    """,
    13: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 34c9-12 35-12 44 0-9 12-35 12-44 0Z"/><circle cx="32" cy="34" r="9"/><path d="M32 25c-2 3-3 5-3 9 0 3 2 6 3 9m-6-15h12"/></g></svg>
    """,
    14: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 18c4 4 8 4 12 0s8-4 12 0 8 4 12 0 8-4 12 0M10 28c4 4 8 4 12 0s8-4 12 0 8 4 12 0 8-4 12 0"/><path d="M18 44c9-12 23-12 32 0-9 12-23 12-32 0Z"/><circle cx="40" cy="44" r="1.5" fill="currentColor" stroke="none"/></g></svg>
    """,
    15: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M30 52V34"/><path d="M22 34c-5 0-8-4-8-8s3-8 8-8c1 0 2 0 3 1 1-5 5-8 10-8 6 0 11 5 11 11v1c4 1 7 4 7 8 0 5-4 9-9 9H22Zm-8 18h36M18 46h28"/></g></svg>
    """,
    16: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m18 50 8-5 8 5 8-5"/><path d="M16 54h34"/><path d="M44 17c0 9-7 16-16 16S12 26 12 17c5 0 9-2 12-7 3 5 7 7 12 7 2 0 5 0 8 0Z"/><path d="m49 14 3 5 6 1-4 4 1 6-6-3-5 3 1-6-4-4 6-1 2-5Z"/></g></svg>
    """,
    17: """
    <svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3"><circle cx="32" cy="18" r="9"/><circle cx="18" cy="32" r="9"/><circle cx="46" cy="32" r="9"/><circle cx="24" cy="46" r="9"/><circle cx="40" cy="46" r="9"/></g></svg>
    """,
}


@register.simple_tag(takes_context=True)
def tr(context, value):
    request = context.get("request")
    language_code = getattr(request, "LANGUAGE_CODE", "en")
    return translate_text(value, language_code)


@register.filter
def translate_value(value, language_code):
    return translate_text(value, language_code)


@register.simple_tag
def sdg_icon(number):
    try:
        key = int(number)
    except (TypeError, ValueError):
        return ""
    return mark_safe(SDG_ICONS.get(key, ""))
