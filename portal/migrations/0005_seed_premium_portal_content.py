from datetime import date

from django.db import migrations


def seed_content(apps, schema_editor):
    SiteSettings = apps.get_model("portal", "SiteSettings")
    PageContent = apps.get_model("portal", "PageContent")
    HeroStat = apps.get_model("portal", "HeroStat")
    InstitutionalValue = apps.get_model("portal", "InstitutionalValue")
    GovernanceRole = apps.get_model("portal", "GovernanceRole")
    StrategicPriority = apps.get_model("portal", "StrategicPriority")
    Program = apps.get_model("portal", "Program")
    ResearchProject = apps.get_model("portal", "ResearchProject")
    EducationInitiative = apps.get_model("portal", "EducationInitiative")
    PolicyDocument = apps.get_model("portal", "PolicyDocument")
    ImpactMetric = apps.get_model("portal", "ImpactMetric")
    Report = apps.get_model("portal", "Report")
    Achievement = apps.get_model("portal", "Achievement")
    Partner = apps.get_model("portal", "Partner")
    NewsArticle = apps.get_model("portal", "NewsArticle")
    Event = apps.get_model("portal", "Event")
    DepartmentContact = apps.get_model("portal", "DepartmentContact")

    SiteSettings.objects.update_or_create(
        pk=1,
        defaults={
            "institution_name": "Uzbekistan Sustainable Development Governance Platform",
            "institution_short_name": "USDG",
            "tagline": "Official platform for strategy, programs, research, education, and public accountability",
            "official_badge": "Official Government-Grade Institutional Portal",
            "navbar_cta_label": "Reports Center",
            "navbar_cta_url": "/reports-insights/",
            "hero_kicker": "Trusted institutional ecosystem",
            "hero_title": "A premium national-style digital platform for sustainability governance and institutional leadership.",
            "hero_description": "Designed for ministries, universities, and large public organizations, this portal combines strategic communication, evidence reporting, flagship programs, research coordination, and public-facing credibility in one refined institutional interface.",
            "hero_primary_label": "Explore Programs",
            "hero_primary_url": "/programs/",
            "hero_secondary_label": "Open Reports Center",
            "hero_secondary_url": "/reports-insights/",
            "overview_title": "Institutional overview",
            "overview_text": "The portal is structured to present official leadership messages, strategic priorities, core services, data-backed reporting, and public communication with clarity, authority, and trust.",
            "mission": "To deliver a trusted, coordinated, and future-oriented institutional platform where policy, education, research, and stakeholder engagement support sustainable development at scale.",
            "vision": "To set a benchmark for premium institutional communication in Uzbekistan through credible design, robust governance, and measurable public value.",
            "strategic_approach": "The platform integrates leadership oversight, flagship programs, evidence architecture, public reporting, and cross-sector collaboration through a unified and carefully governed digital environment.",
            "governance_overview": "Governance is led through executive oversight, implementation councils, operational units, and reporting stewards responsible for quality, compliance, and transparent delivery.",
            "strategy_overview": "Our strategy emphasizes resilience, environmental stewardship, academic modernization, public accountability, and nationally relevant innovation.",
            "leader_name": "Professor Shavkat Rahimov",
            "leader_title": "Rector and Chair of the Institutional Strategy Council",
            "leader_message": "A serious institution should look serious, communicate clearly, and operate with confidence. This portal reflects that principle by connecting our strategy, delivery systems, people, and evidence in a way that is accessible, modern, and trustworthy.",
            "leader_signature": "Office of the Rector",
            "address": "14 Amir Temur Street, Tashkent, Uzbekistan",
            "phone": "+998 71 205 44 44",
            "email": "coordination@usdg.uz",
            "office_hours": "Monday-Friday, 09:00-18:00",
            "footer_text": "A premium digital environment built for institutional trust, public accountability, and strategic execution.",
            "meta_title": "Uzbekistan Sustainable Development Governance Platform",
            "meta_description": "Premium institutional Django portal for official strategy, programs, research, education initiatives, reports, news, events, and public contact.",
        },
    )

    pages = [
        ("home", "Institutional platform", "National-scale premium portal", "Official, structured, and high-trust digital environment for sustainability governance, public reporting, and flagship institutional delivery.", "Why this platform matters", "It combines formal communication, executive messaging, evidence reporting, and public-facing service architecture in one coherent system."),
        ("about", "About the institution", "Institutional identity and direction", "Mission, vision, governance, values, and strategic positioning presented in a modern editorial format rather than a static corporate page.", "Institutional note", "This section is written to strengthen confidence and communicate authority without visual heaviness."),
        ("programs", "Goals, programs, and services", "Operational delivery architecture", "A curated view of strategic goals, flagship programs, and institution-wide services supporting sustainability outcomes and public value.", "Programs logic", "Each program is presented with a clear purpose, narrative, and measurable outcome."),
        ("research", "Research and projects", "Research-led transformation", "Applied projects, cross-sector research, and implementation partnerships aligned with institutional and national priorities.", "Research note", "The emphasis is on credibility, public relevance, and clear stewardship."),
        ("education", "Education and initiatives", "Human capital and capability building", "Academic and public-facing initiatives designed to build literacy, expertise, and leadership for long-term sustainable development.", "Education note", "This page supports both academic positioning and stakeholder communication."),
        ("sustainability", "Strategy, policy, and governance", "Official policy framework", "Policy documents, strategic priorities, and implementation logic presented with the level of seriousness expected from major institutions.", "Policy note", "This is the page that most strongly reinforces the ministry-grade institutional character of the website."),
        ("reports", "Reports and insights", "Evidence and public disclosure", "Downloadable reports, indicators, achievements, and formal highlights arranged as a premium public accountability center.", "Reporting note", "Strong hierarchy, easy scanning, and reliable structure make this section feel immediately official."),
        ("news", "News and events", "Media center and institutional communication", "Professional publication area for updates, briefings, conferences, and public announcements.", "Communications note", "The structure balances editorial polish with official clarity."),
        ("contact", "Contact and coordination", "Trusted contact environment", "A clear and reliable contact page with official channels, department contacts, and a professional inquiry form.", "Contact note", "The layout is designed to reassure visitors that their inquiry reaches a real institutional office."),
    ]
    for page_key, eyebrow, title, intro, supporting_title, supporting_text in pages:
        PageContent.objects.update_or_create(
            page_key=page_key,
            defaults={
                "eyebrow": eyebrow,
                "title": title,
                "intro": intro,
                "supporting_title": supporting_title,
                "supporting_text": supporting_text,
                "meta_title": f"{title} | USDG Platform",
                "meta_description": intro,
            },
        )

    HeroStat.objects.all().delete()
    for order, item in enumerate(
        [
            ("24", "strategic programs", "Flagship institutional programs and services under active delivery"),
            ("72", "official indicators", "Performance indicators used across reports and governance reviews"),
            ("18", "partner institutions", "Government, academic, and development partners in cooperation"),
            ("2026", "active roadmap", "Current institutional implementation cycle and reporting year"),
        ],
        start=1,
    ):
        HeroStat.objects.create(value=item[0], label=item[1], description=item[2], display_order=order)

    InstitutionalValue.objects.all().delete()
    for order, item in enumerate(
        [
            ("Public trust", "Every digital touchpoint should reinforce seriousness, reliability, and accountability."),
            ("Structured governance", "Responsibilities, information hierarchy, and decisions are communicated with clarity."),
            ("Evidence orientation", "The platform privileges measurable data, report-ready narratives, and decision support."),
            ("Institutional polish", "Visual quality is treated as part of credibility, not decoration."),
        ],
        start=1,
    ):
        InstitutionalValue.objects.create(title=item[0], description=item[1], display_order=order)

    GovernanceRole.objects.all().delete()
    for order, item in enumerate(
        [
            ("Strategic Council", "Approves direction, policy priorities, and yearly institutional targets."),
            ("Executive Delivery Office", "Coordinates cross-department implementation and escalates risks."),
            ("Research and Innovation Board", "Aligns research projects with institutional strategy and external partnerships."),
            ("Public Reporting Unit", "Maintains evidence quality, reporting schedules, and publication workflows."),
        ],
        start=1,
    ):
        GovernanceRole.objects.create(title=item[0], responsibility=item[1], display_order=order)

    StrategicPriority.objects.all().delete()
    for order, item in enumerate(
        [
            ("go", "Governance modernization", "Strengthen formal coordination, decision visibility, and institutional accountability.", "Executive reporting reform"),
            ("da", "Data and reporting excellence", "Build reliable reporting architecture for indicators, dashboards, and public reports.", "72 indicators in active use"),
            ("ed", "Education and talent development", "Advance curriculum renewal, leadership capability, and sustainability literacy.", "32 integrated initiatives"),
            ("re", "Research and strategic partnerships", "Expand applied research and long-term collaboration with priority stakeholders.", "18 active partnerships"),
        ],
        start=1,
    ):
        StrategicPriority.objects.create(icon=item[0], title=item[1], summary=item[2], metric=item[3], display_order=order)

    Program.objects.all().delete()
    for order, item in enumerate(
        [
            ("goal", "Institutional Resilience Roadmap", "institutional-resilience-roadmap", "A high-level goal focused on long-term resilience in governance, infrastructure, and service continuity.", "The roadmap aligns planning, facilities, governance, procurement, and communication around measurable resilience priorities that can be tracked year over year.", "2028", "target horizon", True),
            ("program", "Green Operations Acceleration Program", "green-operations-acceleration-program", "Flagship program focused on operational efficiency, resource stewardship, and responsible procurement.", "The program bundles building upgrades, utility monitoring, transport planning, and resource governance into one managed portfolio with executive oversight.", "31%", "efficiency gain pathway", True),
            ("service", "Institutional Data & Reporting Service", "institutional-data-reporting-service", "Internal service for report preparation, evidence validation, and public disclosure workflows.", "The service ensures metrics, annual reports, policy digests, and dashboard outputs follow a consistent and trusted institutional standard.", "12", "scheduled disclosures", True),
            ("program", "Regional Partnership Facilitation Track", "regional-partnership-facilitation-track", "Structured program for public-sector and development-partner engagement.", "The track helps convert cooperation opportunities into governed projects, shared briefs, and visible institutional outcomes.", "18", "active partner channels", False),
        ],
        start=1,
    ):
        Program.objects.create(
            category=item[0],
            title=item[1],
            slug=item[2],
            summary=item[3],
            body=item[4],
            outcome_value=item[5],
            outcome_label=item[6],
            featured=item[7],
            display_order=order,
        )

    ResearchProject.objects.all().delete()
    for order, item in enumerate(
        [
            ("research", "Climate Governance Observatory", "climate-governance-observatory", "A research platform examining resilience policy, implementation barriers, and public-sector adaptation models.", "The observatory combines policy analysis, field evidence, and decision support outputs for public and institutional stakeholders.", "Policy Research Unit", "2025-2027", True),
            ("project", "Integrated Campus Data Twin", "integrated-campus-data-twin", "Strategic project connecting facilities, reporting, and planning data in one decision-support environment.", "The project creates stronger visibility for operational performance and enables premium-quality reporting across the institution.", "Digital Transformation Office", "2026 roadmap", True),
            ("lab", "Sustainable Infrastructure Lab", "sustainable-infrastructure-lab", "Applied laboratory supporting infrastructure innovation, energy performance, and built-environment research.", "The lab bridges engineering, policy, and public value outcomes through prototype testing and advisory work.", "Engineering Faculty", "Permanent facility", False),
        ],
        start=1,
    ):
        ResearchProject.objects.create(
            category=item[0],
            title=item[1],
            slug=item[2],
            summary=item[3],
            body=item[4],
            lead_unit=item[5],
            timeframe=item[6],
            featured=item[7],
            display_order=order,
        )

    EducationInitiative.objects.all().delete()
    for order, item in enumerate(
        [
            ("curriculum", "Sustainability Curriculum Upgrade", "sustainability-curriculum-upgrade", "A structured curriculum enhancement process integrating sustainability competencies across major programs.", "The initiative supports faculty review, outcomes mapping, and institutional quality assurance around sustainability literacy.", "Faculty and students", "Curriculum integration cycle", True),
            ("training", "Executive Sustainability Academy", "executive-sustainability-academy", "Short-format institutional training for managers, coordinators, and delivery teams.", "The academy supports policy literacy, reporting quality, and project governance capability within large organizations.", "Managers and coordinators", "Hybrid cohort model", True),
            ("outreach", "Youth Leadership Initiative", "youth-leadership-initiative", "Public-facing initiative that introduces future leaders to sustainability strategy, innovation, and civic responsibility.", "The program is designed to combine credibility, accessibility, and strong institutional branding in external engagement.", "Students and youth groups", "Workshop and forum format", False),
        ],
        start=1,
    ):
        EducationInitiative.objects.create(
            category=item[0],
            title=item[1],
            slug=item[2],
            summary=item[3],
            body=item[4],
            audience=item[5],
            delivery_model=item[6],
            featured=item[7],
            display_order=order,
        )

    PolicyDocument.objects.all().delete()
    for item in [
        ("strategy", "Institutional Sustainability Strategy 2026-2030", "institutional-sustainability-strategy-2026-2030", "Core strategy document establishing institutional priorities, governance responsibilities, and delivery principles.", "This document formalizes the strategic direction of the platform and connects leadership intent with actionable implementation lines.", date(2026, 1, 15), "2026-2030", True),
        ("policy", "Responsible Procurement Policy", "responsible-procurement-policy", "Official policy guiding sustainable purchasing and supplier due diligence.", "The policy introduces lifecycle thinking, quality controls, and accountability standards for institutional purchasing decisions.", date(2025, 11, 20), "Active policy", True),
        ("framework", "Public Reporting and Evidence Framework", "public-reporting-and-evidence-framework", "Framework for how indicators, report narratives, and public-facing evidence are managed.", "The framework standardizes publication quality and makes the reporting environment more reliable for internal and external users.", date(2026, 2, 7), "Reviewed annually", True),
        ("regulation", "Green Campus Operations Regulation", "green-campus-operations-regulation", "Operational regulation for facilities, utilities, and environmental stewardship procedures.", "The regulation clarifies the responsibilities of operational teams and strengthens delivery discipline.", date(2025, 9, 10), "Operational regulation", False),
    ]:
        PolicyDocument.objects.create(
            category=item[0],
            title=item[1],
            slug=item[2],
            summary=item[3],
            body=item[4],
            publish_date=item[5],
            effective_period=item[6],
            featured=item[7],
        )

    ImpactMetric.objects.all().delete()
    for order, item in enumerate(
        [
            ("Executive decisions supported", "148", "Decisions informed by structured reporting and institutional evidence.", "both"),
            ("Priority initiatives under governance", "32", "Programs and initiatives tracked under formal oversight.", "both"),
            ("Public reports published", "12", "Reports and briefs released through the official portal over the cycle.", "reports"),
            ("Stakeholder engagement reach", "24K", "Audience reached across initiatives, forums, and public communications.", "home"),
        ],
        start=1,
    ):
        ImpactMetric.objects.create(label=item[0], value=item[1], description=item[2], scope=item[3], display_order=order)

    Report.objects.all().delete()
    for item in [
        ("annual", "Institutional Sustainability Report 2025", "institutional-sustainability-report-2025", "Comprehensive annual publication covering governance, initiatives, indicators, and public value outcomes.", "The annual report consolidates core indicators, strategic commentary, case studies, and executive messaging into a single formal publication.", date(2026, 2, 20), "148 executive decisions supported", True),
        ("insight", "Green Procurement Insight Brief", "green-procurement-insight-brief", "Focused brief summarizing procurement reform progress and priority recommendations.", "Prepared for decision-makers seeking a concise but credible view of institutional procurement modernization.", date(2026, 1, 28), "27 supplier reviews completed", True),
        ("ranking", "International Ranking Evidence Submission", "international-ranking-evidence-submission", "Evidence package prepared for international benchmarking and external review.", "The submission demonstrates structured public reporting, measurable outcomes, and documentation discipline.", date(2026, 2, 4), "18 evidence domains covered", True),
        ("dashboard", "Operational Indicators Dashboard", "operational-indicators-dashboard", "Dashboard-focused publication centered on metrics for operations, programs, and reporting.", "A structured data product designed for both internal monitoring and external visibility.", date(2026, 3, 1), "72 live indicators", False),
    ]:
        Report.objects.create(
            report_type=item[0],
            title=item[1],
            slug=item[2],
            summary=item[3],
            body=item[4],
            publish_date=item[5],
            highlight_metric=item[6],
            featured=item[7],
        )

    Achievement.objects.all().delete()
    for order, item in enumerate(
        [
            ("National excellence recognition", "2025", "Recognized for institutional modernization and public accountability practices."),
            ("Regional partnership distinction", "Central Asia", "Highlighted for strong multi-stakeholder collaboration and delivery architecture."),
            ("Digital governance commendation", "Public sector innovation", "Acknowledged for structured reporting and premium institutional user experience."),
        ],
        start=1,
    ):
        Achievement.objects.create(title=item[0], subtitle=item[1], description=item[2], display_order=order)

    Partner.objects.all().delete()
    for order, item in enumerate(
        [
            ("Ministry-level Strategic Partner", "Government", "Formal coordination on policy alignment and reporting standards."),
            ("National Research Network", "Academic", "Collaboration on research, data, and publication quality."),
            ("Regional Innovation Alliance", "Development", "Joint work on capability building and strategic projects."),
            ("International Sustainability Consortium", "International", "Knowledge exchange and benchmark cooperation."),
        ],
        start=1,
    ):
        Partner.objects.create(name=item[0], partner_type=item[1], description=item[2], display_order=order)

    NewsArticle.objects.all().delete()
    for item in [
        ("Official launch of the institutional reporting framework", "official-launch-of-the-institutional-reporting-framework", "official", "The institution has approved a unified framework for reports, evidence handling, and public disclosure.", "The approved framework strengthens transparency, consistency, and the overall quality of institutional communication across all major programs and reports.", date(2026, 3, 10), True),
        ("Research platform expands applied climate governance portfolio", "research-platform-expands-applied-climate-governance-portfolio", "research", "A new wave of applied research projects has been approved under the climate governance portfolio.", "The portfolio connects policy analysis, institutional planning, and stakeholder-facing outputs in a way designed for both academic depth and public value.", date(2026, 3, 5), False),
        ("Flagship operations program enters new implementation phase", "flagship-operations-program-enters-new-implementation-phase", "program", "The Green Operations Acceleration Program has entered its next delivery phase with updated milestones.", "The new phase strengthens governance discipline, data quality, and cross-unit coordination for operational improvement.", date(2026, 2, 26), False),
    ]:
        NewsArticle.objects.create(
            title=item[0],
            slug=item[1],
            category=item[2],
            summary=item[3],
            body=item[4],
            published_on=item[5],
            featured=item[6],
        )

    Event.objects.all().delete()
    for item in [
        ("National Sustainability Leadership Forum", "national-sustainability-leadership-forum", "forum", "Senior institutional leaders and partners will review strategic delivery priorities.", "The forum brings together leadership teams, public stakeholders, and partners for a formal discussion on strategic execution and cooperation.", date(2026, 4, 12), date(2026, 4, 12), "Main Conference Hall", "Leaders and partners", True),
        ("Public Reporting Excellence Workshop", "public-reporting-excellence-workshop", "workshop", "Operational and communications teams will review evidence quality and reporting standards.", "The workshop is designed to strengthen publication workflows, document discipline, and report usability.", date(2026, 4, 22), date(2026, 4, 22), "Training Center", "Coordinators and editors", False),
        ("Executive Briefing on Institutional Indicators", "executive-briefing-on-institutional-indicators", "briefing", "A briefing focused on 2026 priority metrics and reporting implications.", "This executive session is intended to align leadership understanding around current performance and upcoming reporting requirements.", date(2026, 5, 3), date(2026, 5, 3), "Strategy Room", "Executive team", False),
    ]:
        Event.objects.create(
            title=item[0],
            slug=item[1],
            category=item[2],
            summary=item[3],
            details=item[4],
            start_date=item[5],
            end_date=item[6],
            venue=item[7],
            audience=item[8],
            featured=item[9],
        )

    DepartmentContact.objects.all().delete()
    for order, item in enumerate(
        [
            ("Strategic Coordination Office", "Aziza Mamatova", "+998 71 205 44 51", "strategy@usdg.uz", "Rectorate Building, Floor 3", "Monday-Friday, 09:00-18:00"),
            ("Reports and Insights Unit", "Jahongir Karimov", "+998 71 205 44 52", "reports@usdg.uz", "Analytics Center", "Monday-Friday, 09:00-18:00"),
            ("Partnerships and Communications", "Malika Sobirova", "+998 71 205 44 53", "partnerships@usdg.uz", "External Relations Wing", "Monday-Friday, 09:00-18:00"),
        ],
        start=1,
    ):
        DepartmentContact.objects.create(
            department_name=item[0],
            contact_person=item[1],
            phone=item[2],
            email=item[3],
            office_location=item[4],
            office_hours=item[5],
            display_order=order,
        )


def clear_content(apps, schema_editor):
    model_names = [
        "DepartmentContact",
        "Event",
        "NewsArticle",
        "Partner",
        "Achievement",
        "Report",
        "ImpactMetric",
        "PolicyDocument",
        "EducationInitiative",
        "ResearchProject",
        "Program",
        "StrategicPriority",
        "GovernanceRole",
        "InstitutionalValue",
        "HeroStat",
        "PageContent",
    ]
    for model_name in model_names:
        apps.get_model("portal", model_name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("portal", "0004_achievement_departmentcontact_educationinitiative_and_more")]

    operations = [migrations.RunPython(seed_content, clear_content)]
