from django import template
from django.core.exceptions import ValidationError
from django.utils.html import format_html, format_html_join, linebreaks
from django.utils.safestring import mark_safe

from portal.news_blocks import parse_news_blocks


register = template.Library()


@register.filter
def news_content(value):
    try:
        blocks = parse_news_blocks(value)
    except ValidationError:
        blocks = None
    if blocks is None:
        return mark_safe(linebreaks(value, autoescape=True))
    rendered = []
    for block in blocks:
        if block["type"] == "text":
            rendered.append(mark_safe(linebreaks(block["text"], autoescape=True)))
        else:
            rows = []
            for index, row in enumerate(block["rows"]):
                cell_template = '<th scope="col">{}</th>' if index == 0 else "<td>{}</td>"
                cells = format_html_join("", cell_template, ((cell,) for cell in row))
                rows.append(format_html("<tr>{}</tr>", cells))
            rendered.append(format_html(
                '<div class="governance-table-wrap" tabindex="0" role="region" aria-label="Yangilik jadvali"><table class="governance-table"><thead>{}</thead><tbody>{}</tbody></table></div>',
                rows[0], format_html_join("", "{}", ((row,) for row in rows[1:])),
            ))
    return format_html_join("", "{}", ((block,) for block in rendered))
