# Responsive portal verification

Verified on 2026-10-28 using headless Microsoft Edge (Playwright).

- Ten portal routes checked at 320, 375, 580, 768, 1024, 1280, 1366 and 1920 px: no horizontal page overflow.
- Uzbek and English checked at 375, 768, 1280, 1366 and 1920 px: navigation, search bounds and clicking the news card image pass.
- Mobile search uses a flexible grid so its input remains usable alongside the submit button.
- Rankings use the available width on intermediate desktop screens; document buttons wrap on phones.
- Document contents, text, download links, news styles, WebP uploads and loader improvements are included in this update.
- Django system check, migration drift check and JavaScript syntax check pass.
- Django suite: 38 of 40 pass. Existing failures: test_disability_support_roadmap_loads expects June 2026; test_governance_meeting_minutes_detail_loads expects February 2025. Dates were not changed without a content requirement.

Local environment configuration, database, uploaded media, scratch folders and Python bytecode are excluded from this commit.
