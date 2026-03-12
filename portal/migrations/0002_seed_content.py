from datetime import date

from django.db import migrations


def seed_content(apps, schema_editor):
    SiteSettings = apps.get_model("portal", "SiteSettings")
    GovernanceRole = apps.get_model("portal", "GovernanceRole")
    SustainabilityPolicy = apps.get_model("portal", "SustainabilityPolicy")
    SustainabilityReport = apps.get_model("portal", "SustainabilityReport")
    Partner = apps.get_model("portal", "Partner")
    SDG = apps.get_model("portal", "SDG")
    SDGProject = apps.get_model("portal", "SDGProject")
    ResearchItem = apps.get_model("portal", "ResearchItem")
    CampusInitiative = apps.get_model("portal", "CampusInitiative")
    EngagementInitiative = apps.get_model("portal", "EngagementInitiative")
    InsightMetric = apps.get_model("portal", "InsightMetric")
    NewsArticle = apps.get_model("portal", "NewsArticle")
    Event = apps.get_model("portal", "Event")

    SiteSettings.objects.create(
        site_name="University Sustainability Portal",
        short_name="SDG",
        tagline="Strategy, evidence, and public accountability",
        hero_title="Advancing the Sustainable Development Goals through governance, research, and campus action.",
        hero_text="This portal presents the university's formal sustainability commitments, strategic initiatives, measurable indicators, and public reporting aligned with national priorities and the global SDG agenda.",
        rector_name="Professor Dilshod Karimov",
        rector_title="Rector",
        rector_message="Our university regards sustainability as a core responsibility of public higher education. We are strengthening governance, expanding interdisciplinary research, and transforming campus operations to ensure graduates are prepared to lead responsible change.",
        sustainability_strategy="The current institutional strategy embeds SDG priorities into planning, budgeting, academic quality assurance, infrastructure investment, and public engagement.",
        governance_overview="A formal steering structure led by senior leadership coordinates sustainability delivery, reporting, and evidence management across academic and administrative units.",
        contact_address="1 Academic Avenue, Main Campus",
        contact_phone="+998 71 000 00 00",
        contact_email="sustainability@example.edu",
        office_hours="Monday to Friday, 09:00-18:00",
    )

    for order, item in enumerate([
        ("Executive Council", "Approves sustainability targets, allocates resources, and reviews annual progress."),
        ("SDG Steering Committee", "Coordinates implementation across faculties, operations, student life, and external partnerships."),
        ("Sustainability Office", "Maintains reporting systems, manages evidence files, and supports project delivery."),
    ], start=1):
        GovernanceRole.objects.create(title=item[0], responsibility=item[1], display_order=order)

    for item in [
        ("Environmental Management Policy", "environment", "Defines responsibilities for energy, water, waste, and environmental performance.", date(2025, 1, 14)),
        ("Inclusive Education Policy", "education", "Supports equitable access, safe learning environments, and inclusive student support.", date(2024, 9, 1)),
        ("Responsible Procurement Guidelines", "procurement", "Introduces lifecycle and supplier standards into purchasing decisions.", date(2025, 2, 7)),
        ("Research Ethics and Public Impact Framework", "research", "Promotes research that addresses social and environmental priorities.", date(2024, 11, 22)),
        ("Climate and Risk Preparedness Protocol", "risk", "Guides resilience planning for heat, water stress, and emergency response.", date(2025, 3, 11)),
        ("Data Disclosure Procedure", "disclosure", "Standardizes review and publication of sustainability indicators and evidence.", date(2025, 4, 18)),
    ]:
        SustainabilityPolicy.objects.create(title=item[0], category=item[1], summary=item[2], published_on=item[3])

    for item in [
        ("Annual Sustainability Report 2025", "annual", "Integrated annual report covering governance, indicators, and case studies.", date(2026, 2, 20), "https://example.edu/reports/annual-2025.pdf"),
        ("THE Impact Rankings Submission", "ranking", "Methodological notes and evidence mapped to SDG performance.", date(2026, 1, 30), "https://example.edu/reports/the-impact.pdf"),
        ("Campus Resource Dashboard", "dashboard", "Operational overview for energy, waste, water, transport, and infrastructure indicators.", date(2026, 2, 10), "https://example.edu/reports/dashboard"),
        ("Policy and Regulation Digest", "policy", "Core sustainability-related policies and governance references.", date(2025, 12, 15), "https://example.edu/reports/policy-digest.pdf"),
    ]:
        SustainabilityReport.objects.create(title=item[0], report_type=item[1], summary=item[2], publish_date=item[3], download_url=item[4])

    for order, item in enumerate([
        ("Ministry of Higher Education", "Government"),
        ("Municipal Development Authority", "Government"),
        ("International Sustainability Network", "International"),
        ("Regional Industry Council", "Industry"),
        ("Green Campus Alliance", "Academic"),
    ], start=1):
        Partner.objects.create(name=item[0], partner_type=item[1], display_order=order)

    sdg_data = [
        (1, "No Poverty", "Supporting social inclusion, targeted outreach, and student assistance to reduce barriers to participation.", "The university supports vulnerable students through scholarships, outreach, and social protection referrals.", "Financial aid, outreach, and inclusive access measures are embedded in student services.", "Scholarship coverage, retention support, and outreach beneficiaries.", "sdg-1", False),
        (2, "Zero Hunger", "Advancing nutrition awareness, food security partnerships, and responsible campus food systems.", "Programs combine food literacy, research, and community cooperation.", "The university works with local partners on nutrition education and campus food service standards.", "Food support sessions, nutrition campaigns, and partner outputs.", "sdg-2", False),
        (3, "Good Health and Well-being", "Promoting health services, wellbeing education, and research that supports healthier communities.", "Health and wellbeing are addressed through services, curriculum, and public outreach.", "Student wellbeing services, health campaigns, and applied health research are coordinated institutionally.", "Participation in wellbeing services and public health initiatives.", "sdg-3", False),
        (4, "Quality Education", "Enhancing access, educational quality, and lifelong learning opportunities across disciplines.", "Educational quality and inclusive access remain core institutional priorities.", "Programs align teaching quality, student support, and lifelong learning opportunities with SDG commitments.", "Curriculum mapping, course access, and graduate outcomes.", "sdg-4", True),
        (5, "Gender Equality", "Strengthening equal opportunity, safe learning environments, and women’s leadership participation.", "Institutional policy supports equal access and leadership opportunities.", "Gender-responsive support services, career development, and safeguarding measures are maintained across the university.", "Participation, leadership, and policy implementation indicators.", "sdg-5", False),
        (6, "Clean Water and Sanitation", "Improving conservation, sanitation standards, and water-related research and outreach activity.", "Water stewardship is addressed through infrastructure, monitoring, and literacy.", "Metering, leak response, sanitation standards, and educational programs improve water resilience.", "Water intensity, sanitation coverage, and training participation.", "sdg-6", True),
        (7, "Affordable and Clean Energy", "Driving efficient energy use, renewable deployment, and climate-conscious infrastructure planning.", "Energy governance combines monitoring, retrofit planning, and clean energy pilots.", "Operational teams manage energy data, retrofits, and renewable technology pilots.", "Energy intensity, clean energy pilots, and retrofit performance.", "sdg-7", True),
        (8, "Decent Work and Economic Growth", "Preparing graduates for responsible employment and supporting enterprise and innovation ecosystems.", "Employability and responsible innovation are embedded in academic and startup pathways.", "Career services, incubators, and industry collaboration support sustainable employment outcomes.", "Graduate outcomes, startup activity, and employer engagement.", "sdg-8", False),
        (9, "Industry, Innovation and Infrastructure", "Supporting applied research, entrepreneurship, and resilient physical and digital infrastructure.", "Research and infrastructure programs support applied innovation and resilience.", "Innovation hubs, research labs, and infrastructure planning link academic capacity to sector needs.", "Lab investment, innovation outputs, and infrastructure upgrades.", "sdg-9", True),
        (10, "Reduced Inequalities", "Promoting inclusion, accessibility, and equitable participation in university life and outreach.", "Inclusion measures focus on access, support services, and equitable participation.", "Policies and student services reduce institutional barriers for underrepresented groups.", "Access, support utilization, and retention indicators.", "sdg-10", False),
        (11, "Sustainable Cities and Communities", "Working with cities and communities on planning, mobility, resilience, and cultural sustainability.", "City partnerships connect teaching and research to local planning challenges.", "Urban studies, planning support, and community resilience projects serve regional needs.", "Municipal partnerships, training activity, and project outputs.", "sdg-11", True),
        (12, "Responsible Consumption and Production", "Advancing sustainable procurement, waste reduction, reuse systems, and resource awareness.", "Operational management emphasizes responsible procurement and circular practices.", "Waste sorting, reuse systems, and procurement reforms reduce resource intensity.", "Waste diversion, procurement standards, and awareness participation.", "sdg-12", False),
        (13, "Climate Action", "Integrating emissions reduction, adaptation planning, and climate education across the institution.", "Climate action is advanced through low-carbon operations, climate literacy, and resilience planning.", "Energy upgrades, adaptation research, and awareness programs shape the institutional response.", "Energy, resilience, and climate learning indicators.", "sdg-13", True),
        (14, "Life Below Water", "Supporting water ecosystem protection through research, literacy, and responsible water management.", "Water ecosystem issues are approached through research and awareness.", "Projects examine water quality, conservation, and ecosystem stewardship.", "Water research outputs and stewardship engagement.", "sdg-14", False),
        (15, "Life on Land", "Protecting biodiversity, green spaces, and land stewardship through campus and field-based initiatives.", "Biodiversity and landscape stewardship support teaching and campus resilience.", "Tree management, habitat areas, and environmental education contribute to land stewardship.", "Biodiversity inventory and campus landscape indicators.", "sdg-15", False),
        (16, "Peace, Justice and Strong Institutions", "Building transparency, ethical governance, legal literacy, and accountable institutional practice.", "Good governance and public accountability underpin the sustainability program.", "Disclosure, ethics, legal literacy, and participatory governance support institutional trust.", "Disclosure performance and governance participation indicators.", "sdg-16", False),
        (17, "Partnerships for the Goals", "Expanding collaboration with public institutions, industry, civil society, and international networks.", "Institutional partnerships extend the reach and quality of sustainability outcomes.", "Government, industry, civil society, and international collaboration support delivery and benchmarking.", "Partnership count, joint outputs, and collaborative training.", "sdg-17", False),
    ]
    sdg_objects = {}
    for item in sdg_data:
        sdg_objects[item[0]] = SDG.objects.create(
            number=item[0], title=item[1], short_description=item[2], overview=item[3],
            university_actions=item[4], indicators=item[5], color_class=item[6], featured=item[7]
        )

    for number, title, summary, project_type in [
        (4, "Inclusive Curriculum Renewal", "Faculty teams revised core modules to integrate sustainability outcomes and inclusive teaching practice.", "Curriculum"),
        (6, "Smart Water Metering Program", "Digital metering and leak response protocols improved water stewardship across campus.", "Infrastructure"),
        (7, "Solar Pilot for Academic Blocks", "Pilot photovoltaic systems support clean energy learning and operational savings.", "Energy"),
        (9, "Applied Innovation Hub", "An interdisciplinary hub supports prototypes and startups addressing regional sustainability needs.", "Innovation"),
        (11, "Urban Resilience Planning Studio", "Student and faculty teams support municipal planning on mobility and public space.", "Community"),
        (13, "Climate Risk Mapping Initiative", "Research teams analyze heat exposure and resilience options for surrounding districts.", "Research"),
    ]:
        SDGProject.objects.create(sdg=sdg_objects[number], title=title, summary=summary, project_type=project_type)

    for item in [
        ("Climate Resilience Research Cluster", "project", "Interdisciplinary project on urban heat, water stress, and adaptation planning.", "Research Office", "11 active work packages"),
        ("Water Stewardship Technical Series", "publication", "Policy briefs and technical notes on water conservation and sanitation governance.", "Engineering Faculty", "12 published briefs"),
        ("Center for Sustainable Infrastructure", "center", "Research center linking engineering, planning, and public policy expertise.", "Engineering Faculty", "18 affiliated researchers"),
        ("Green Enterprise Incubator", "innovation", "Startup support for resource efficiency, climate technology, and circular economy ideas.", "Innovation Office", "9 startup teams"),
        ("Regional Sustainability Grants Portfolio", "grant", "Externally funded research and community projects addressing SDG priorities.", "Research Office", "11 active grants"),
        ("Sustainability in Public Administration", "course", "Course on governance, planning, and accountability for sustainable development.", "Public Policy", "180 annual students"),
        ("Environmental Systems Engineering", "program", "Degree pathway emphasizing resilient infrastructure and efficient resource systems.", "Engineering Faculty", "4-year program"),
        ("Student Energy Audit Challenge", "student", "Students assess building performance and propose efficiency measures.", "Campus Operations", "14 project teams"),
        ("Open SDG Literacy Course", "mooc", "Short online training on SDG implementation, indicators, and community action.", "Continuing Education", "2,400 learners"),
    ]:
        ResearchItem.objects.create(title=item[0], category=item[1], summary=item[2], department=item[3], highlight_metric=item[4])

    for item in [
        ("Green Campus Landscape Program", "green", "Campus planning supports shaded circulation routes, native planting, and outdoor learning space.", "4,200 managed green assets"),
        ("Energy Monitoring and Retrofit Plan", "energy", "Real-time dashboards and retrofit sequencing support lower energy use.", "31% reduction since baseline"),
        ("Integrated Waste Segregation System", "waste", "Sorting infrastructure and reuse pathways reduce landfill dependency.", "58% waste diversion"),
        ("Water Efficiency Upgrade Cycle", "water", "Conservation fixtures and metering improvements reduce water losses.", "22% water use reduction"),
        ("Low-impact Mobility Program", "transport", "Pedestrian access, cycle support, and shuttle coordination improve mobility options.", "3 modal shift pilots"),
        ("Resilient Buildings Standard", "building", "Renovation and capital projects prioritize ventilation, durability, and efficiency.", "7 major buildings upgraded"),
        ("Campus Biodiversity Inventory", "biodiversity", "Tree mapping and habitat management support environmental stewardship.", "Annual biodiversity audit"),
    ]:
        CampusInitiative.objects.create(title=item[0], category=item[1], summary=item[2], metric=item[3])

    for item in [
        ("School Sustainability Outreach", "social", "Faculty and students deliver sustainability awareness and practical sessions in local schools.", "Schools and youth groups"),
        ("Student Volunteer Green Corps", "volunteer", "Volunteer teams support campaigns, campus action days, and community events.", "Students and local residents"),
        ("Municipal Resilience Partnership", "government", "Joint planning and data initiatives support urban resilience and public service improvement.", "Municipal authorities"),
        ("Industry Resource Efficiency Clinic", "industry", "Applied collaboration supports production efficiency and graduate employability.", "Regional employers"),
        ("Community Water Stewardship Training", "training", "Public training on efficient water use, sanitation awareness, and monitoring.", "Schools, NGOs, service providers"),
    ]:
        EngagementInitiative.objects.create(title=item[0], category=item[1], summary=item[2], audience=item[3])

    for order, item in enumerate([
        ("Energy intensity reduction", "31%", "Reduction in campus energy intensity since 2021 baseline", "both"),
        ("Waste diversion", "58%", "Waste diverted from landfill through sorting and reuse streams", "both"),
        ("Water use reduction", "22%", "Reduction in campus water use after retrofit cycle", "insights"),
        ("SDG-linked courses", "74", "Courses with explicit sustainability learning outcomes", "both"),
        ("Community beneficiaries", "16,800", "Annual beneficiaries reached through community engagement activities", "home"),
    ], start=1):
        InsightMetric.objects.create(label=item[0], value=item[1], context=item[2], page_scope=item[3], display_order=order)

    for item in [
        ("University adopts revised sustainability reporting framework", "university-adopts-revised-sustainability-reporting-framework", "policy", "The updated framework harmonizes campus operational data, research outputs, and engagement metrics for annual disclosure.", "The revised framework aligns evidence collection across campus operations, education, research, and engagement, improving data integrity and disclosure quality.", date(2026, 3, 12), True),
        ("Interdisciplinary climate resilience project receives national grant", "interdisciplinary-climate-resilience-project-receives-national-grant", "research", "Faculty and graduate researchers will examine heat adaptation and water resilience in rapidly urbanizing districts.", "The grant supports field studies, local data collection, and policy engagement on climate resilience priorities.", date(2026, 3, 3), True),
        ("New energy monitoring system commissioned across academic buildings", "new-energy-monitoring-system-commissioned-across-academic-buildings", "campus", "Real-time dashboards will support targeted efficiency upgrades and stronger operational governance.", "The monitoring platform provides building-level analysis to support retrofit decisions and annual reporting.", date(2026, 2, 24), True),
    ]:
        NewsArticle.objects.create(title=item[0], slug=item[1], category=item[2], summary=item[3], body=item[4], published_on=item[5], featured=item[6])

    for item in [
        ("Campus Sustainability Open Day", "campus-sustainability-open-day", "event", "An open campus event presenting new initiatives, student projects, and partner exhibits.", "The open day includes guided visits, exhibitions, and dialogue with staff, students, and external partners.", date(2026, 3, 24), "Main Campus", "Students, staff, and public visitors"),
        ("University SDG Research and Innovation Conference", "university-sdg-research-and-innovation-conference", "conference", "Researchers and public partners review evidence, prototypes, and policy pathways.", "The conference includes plenaries, technical panels, and a student research showcase.", date(2026, 4, 7), "Conference Hall, Main Campus", "Researchers, students, public partners"),
        ("Community Water Stewardship Workshop", "community-water-stewardship-workshop", "workshop", "Public training on efficient water use, monitoring, and educational outreach methods.", "The workshop supports local schools, NGOs, and public service actors working on water stewardship.", date(2026, 4, 16), "Training Center", "Schools, NGOs, service providers"),
    ]:
        Event.objects.create(title=item[0], slug=item[1], category=item[2], summary=item[3], details=item[4], start_date=item[5], venue=item[6], audience=item[7])


def unseed_content(apps, schema_editor):
    for model_name in [
        "ContactSubmission", "Event", "NewsArticle", "InsightMetric", "EngagementInitiative",
        "CampusInitiative", "ResearchItem", "SDGProject", "SDG", "Partner",
        "SustainabilityReport", "SustainabilityPolicy", "GovernanceRole", "SiteSettings",
    ]:
        apps.get_model("portal", model_name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("portal", "0001_initial")]

    operations = [migrations.RunPython(seed_content, unseed_content)]
