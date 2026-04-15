from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.views.generic import DetailView, TemplateView

from .forms import ContactSubmissionForm
from .models import (
    Achievement,
    DepartmentContact,
    EducationInitiative,
    Event,
    GovernanceRole,
    HeroStat,
    ImpactMetric,
    InstitutionalValue,
    NewsArticle,
    PageContent,
    Partner,
    PolicyDocument,
    Program,
    Report,
    ResearchProject,
    SDGWorkItem,
    SiteSettings,
    StrategicPriority,
)
from .research_centers_data import (
    RESEARCH_CENTER_CARDS,
    RESEARCH_CENTER_CARDS_EN,
    RESEARCH_CENTER_DETAILS,
    RESEARCH_CENTER_TRANSLATIONS_EN,
)
from .sdg_publications_data import get_sdg_publication_data
from .sustainability_subjects_tables import (
    SUSTAINABILITY_SUBJECTS_RAW_HTML_EN,
    SUSTAINABILITY_SUBJECTS_RAW_HTML_UZ,
)
from .sustainability_study_programs_tables import (
    SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_EN,
    SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_UZ,
)
from .translation_utils import build_page_content_fallback, localize_collection, localize_object, translate_text


ETHICS_CODE_PDF_PATH = Path(settings.BASE_DIR) / "meedia" / "QARSHI DAVLAT UNIVERSITETINING ODOB-AXLOQ KODEKSI.pdf"

ANTI_CORRUPTION_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Korrupsiyaga qarshi kurashish bo'limi",
        "intro": "Bo'lim boshlig'i va bo'lim faoliyati bo'yicha batafsil ma'lumotlar.",
        "leader_title": "Bo'lim boshlig'i",
        "leader_name": "Ismatov Xolmumin Xurozovich",
        "leader_role": "Bo'lim boshlig'i",
        "leader_details": [
            "Telefon: 75-220-02-17, 98-776-59-08",
            "Elektron pochta: halmumin8@gmail.com",
            "Qabul vaqti: har kuni 09:00 dan 18:00 gacha",
        ],
        "sections": [
            {
                "title": "Mehnat faoliyati",
                "paragraphs": [
                    "1983-1988 yillarda Moskva muhandis qurilish institutida tahsil olgan. 1988-1995 yillarda Toshkent yengil metal konstruksiya zavodida texnik nazorat bo'limi boshlig'i bo'lib ishlagan.",
                    "1995-2013 yillarda Milliy xavfsizlik xizmatida ishlagan. 2013-2017 yillarda \"Sho'rtan neftgaz\" UKda 1-bo'lim boshlig'i va rahbar o'rinbosari bo'lgan.",
                    "2017-2023 yillarda G'uzor tumani Sho'rtan neft-gaz qazib chiqarish boshqarmasi o'quv markaziga rahbarlik qilgan. 2023 yildan hozirgacha Qarshi davlat universitetida ushbu bo'lim boshlig'i sifatida faoliyat yuritmoqda.",
                ],
            },
            {
                "title": "Bo'lim tarixi",
                "paragraphs": [
                    "Bo'lim O'zbekiston Respublikasi Oliy va o'rta maxsus ta'lim vazirligining 2021-yil 28-iyundagi 281-sonli buyrug'i ijrosini ta'minlash maqsadida, Qarshi davlat universiteti rektorining 2021-yil 5-iyuldagi 171-I-sonli buyrug'i bilan tashkil etilgan.",
                    "Bo'lim tarkibi: 1 nafar bo'lim boshlig'i va 2 nafar bosh mutaxassis.",
                ],
            },
            {
                "title": "Asosiy vazifalari",
                "bullets": [
                    "universitetda korrupsiyaga oid huquqbuzarliklarning oldini olish va ularga qarshi kurashish",
                    "\"Korrupsiyasiz soha\" loyihasini universitetda joriy etish",
                    "korrupsion xavf yuqori bo'lgan yo'nalishlarni aniqlash",
                    "sabab va shart-sharoitlarni bartaraf etish",
                    "monitoring va jamoatchilik nazoratini yo'lga qo'yish",
                    "xalqaro tajribani o'rganish",
                    "texnikumlar va akademik litsey faoliyatini muvofiqlashtirish",
                ],
            },
            {
                "title": "Bo'lim mutaxassislari aloqalari",
                "bullets": [
                    "+99897-319-00-12 РІР‚вЂќ nodirasrajiddinova@gmail.com",
                    "+99877-106-67-77 РІР‚вЂќ shuxrataxmedov2778@gmail.com",
                ],
            },
            {
                "title": "Botlar",
                "links": [
                    {"label": "@QarDu_AntiKor_bot", "url": "https://t.me/QarDu_AntiKor_bot", "description": "Qarshi davlat universiteti bo'limi boti."},
                    {"label": "@eduuzanticor_bot", "url": "https://t.me/eduuzanticor_bot", "description": "Oliy ta'lim, fan va innovatsiyalar vazirligi korrupsiyaga qarshi kurashish bo'limi boti."},
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Anti-Corruption Department",
        "intro": "Detailed information about the department head and the department's activities.",
        "leader_title": "Head of the department",
        "leader_name": "Ismatov Xolmumin Xurozovich",
        "leader_role": "Head of department",
        "leader_details": [
            "Phone: 75-220-02-17, 98-776-59-08",
            "Email: halmumin8@gmail.com",
            "Reception hours: every day from 09:00 to 18:00",
        ],
        "sections": [
            {
                "title": "Professional background",
                "paragraphs": [
                    "From 1983 to 1988, he studied at the Moscow Institute of Civil Engineering. From 1988 to 1995, he worked as Head of the Technical Control Department at the Tashkent Light Metal Structures Plant.",
                    "From 1995 to 2013, he served in the National Security Service. From 2013 to 2017, he was Head of Department No. 1 and Deputy Manager at Shurtan Neftgaz UK.",
                    "From 2017 to 2023, he led the training center of the Shurtan oil and gas production administration in Guzor district. Since 2023, he has been serving as the head of this department at Karshi State University.",
                ],
            },
            {
                "title": "History of the department",
                "paragraphs": [
                    "The department was established by Rector's Order No. 171-I dated July 5, 2021, in order to implement Order No. 281 of the Ministry of Higher and Secondary Specialized Education of the Republic of Uzbekistan dated June 28, 2021.",
                    "The department structure consists of 1 head of department and 2 chief specialists.",
                ],
            },
            {
                "title": "Main responsibilities",
                "bullets": [
                    "preventing and combating corruption-related offenses at the university",
                    "implementing the \"Corruption-Free Sphere\" project at the university",
                    "identifying areas with high corruption risk",
                    "eliminating root causes and enabling conditions",
                    "establishing monitoring and public oversight",
                    "studying international best practices",
                    "coordinating the activities of technical schools and academic lyceums",
                ],
            },
            {
                "title": "Specialists' contacts",
                "bullets": [
                    "+99897-319-00-12 РІР‚вЂќ nodirasrajiddinova@gmail.com",
                    "+99877-106-67-77 РІР‚вЂќ shuxrataxmedov2778@gmail.com",
                ],
            },
            {
                "title": "Bots",
                "links": [
                    {"label": "@QarDu_AntiKor_bot", "url": "https://t.me/QarDu_AntiKor_bot", "description": "Bot of the Karshi State University department."},
                    {"label": "@eduuzanticor_bot", "url": "https://t.me/eduuzanticor_bot", "description": "Bot of the anti-corruption department of the Ministry of Higher Education, Science and Innovations."},
                ],
            },
        ],
    },
    "disability-support-policy": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Nogironligi bo'lgan shaxslarni qo'llab-quvvatlash siyosati",
        "title_en": "Support Policy for Persons with Disabilities",
        "intro_uz": "Inklyuziv ta'lim, teng imkoniyatlar va moslashtirilgan xizmatlar uchun institutsional siyosat.",
        "intro_en": "An institutional policy for inclusive education, equal opportunity, and accessible support services.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>Nogironligi bo'lgan shaxslarni qo'llab-quvvatlash siyosati</strong></p>
              <p>O'zbekiston Respublikasi Prezidentining 2019-yil 29-apreldagi PF-5712-son Farmoni hamda 2020-2025-yillarda inklyuziv ta'limni rivojlantirish konsepsiyasiga muvofiq, Qarshi davlat universitetida alohida ta'lim ehtiyojlariga ega bo'lgan talabalar uchun teng, qulay va sifatli ta'lim muhitini yaratish ustuvor vazifa etib belgilanadi.</p>
              <p>Mazkur siyosat nogironligi bo'lgan talabalar, xodimlar va tashrif buyuruvchilar uchun teng imkoniyatlar yaratish, ularning ta'lim, mehnat va ijtimoiy hayotda to'liq va samarali ishtirokini ta'minlashga qaratilgan. Siyosat inklyuzivlik, kamsitmaslik, individual yondashuv, maxfiylik va barqarorlik tamoyillariga asoslanadi hamda Barqaror rivojlanish maqsadlari bilan uyg'un holda amalga oshiriladi.</p>
              <p><strong>Qo'llash sohasi va majburiy hollari</strong></p>
              <p>Siyosat barcha ta'lim bosqichlari talabalari, akademik va ma'muriy xodimlar, tashrif buyuruvchilar hamda hamkor tashkilot vakillariga tatbiq etiladi. U ta'lim jarayoni, ish faoliyati, tadbirlar va infratuzilma xizmatlarini qamrab oladi va quyidagi holatlarda majburiy hisoblanadi:</p>
              <ul>
                <li>ma'ruza, seminar va imtihonlar kabi ta'lim jarayonlarida;</li>
                <li>ishga qabul qilish va mehnat faoliyatida;</li>
                <li>tadbirlar va jamoat faoliyatida;</li>
                <li>infratuzilma va xizmatlardan foydalanishda.</li>
              </ul>
              <p><strong>Asosiy tamoyillar</strong></p>
              <ul>
                <li>har bir shaxs uchun teng huquq va imkoniyatlar;</li>
                <li>to'g'ridan-to'g'ri yoki bilvosita diskriminatsiyani qat'iy rad etish;</li>
                <li>individual ehtiyojlarni alohida baholash va moslashtirilgan qo'llab-quvvatlash;</li>
                <li>nogironlikka oid ma'lumotlarning maxfiyligi;</li>
                <li>qo'llab-quvvatlash xizmatlarini doimiy rivojlantirish.</li>
              </ul>
              <p><strong>Qo'llab-quvvatlash xizmatlari</strong></p>
              <p>Akademik qo'llab-quvvatlash doirasida individual o'quv rejalarini ishlab chiqish, o'quv materiallarini braille, audio va raqamli shakllarda taqdim etish, imtihonlarda qo'shimcha vaqt ajratish, alohida sharoit yaratish va moslashtirilgan baholash tizimlarini joriy etish ko'zda tutiladi. O'qituvchilar uchun inkluziv pedagogika bo'yicha treninglar muntazam o'tkaziladi.</p>
              <p>Jismoniy muhitni moslashtirish doirasida panduslar, liftlar, keng kirish yo'laklari, maxsus hojatxonalar, taktil yo'laklar hamda vizual va audio belgilar joriy etiladi. Texnologik qo'llab-quvvatlash screen reader, speech-to-text va text-to-speech vositalarini, shuningdek, onlayn ta'lim platformalarini xalqaro accessibility standartlariga moslashtirishni o'z ichiga oladi. Kutubxonalarda maxsus texnika va raqamli resurslar kengaytiriladi.</p>
              <p>Psixologik va ijtimoiy yordam xizmatlari professional maslahat, stressni boshqarish, yangi muhitga moslashish dasturlari, tengdoshlar o'rtasida o'zaro yordam tizimlari va inklyuziv madaniyatni shakllantirishga qaratilgan ma'naviy-ma'rifiy tadbirlarni o'z ichiga oladi.</p>
              <p><strong>Inkluziv qo'llab-quvvatlash markazi</strong></p>
              <p>Universitetda tashkil etilgan "Inkluziv qo'llab-quvvatlash markazi" quyidagilar uchun mas'ul:</p>
              <ul>
                <li>talablarni aniqlash;</li>
                <li>xizmatlarni tashkil etish;</li>
                <li>monitoring olib borish;</li>
                <li>har bir fakultet va bo'limning siyosatga amal qilishini ta'minlash;</li>
                <li>o'qituvchilar tomonidan inkluziv yondashuv qo'llanilishini kuzatish.</li>
              </ul>
              <p><strong>Monitoring va baholash</strong></p>
              <p>Siyosatning samarali ijrosi yillik auditlar va hisobotlar, talaba va xodimlar fikr-mulohazalari, KPI hamda SDG indikatorlari asosida baholanadi. Natijalar doimiy takomillashtirish rejasiga kiritilib boriladi.</p>
              <p><strong>Moliyalashtirish</strong></p>
              <p>Moliyalashtirish universitetning ichki budjeti, davlat dasturlari, xalqaro grantlar, xususiy sektor hamda donor tashkilotlar bilan hamkorlik orqali shakllantiriladi. Bu yondashuv infratuzilmani moslashtirish, assistiv texnologiyalarni xarid qilish, mutaxassislarni tayyorlash va qo'llab-quvvatlash xizmatlarini barqaror saqlashga xizmat qiladi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>Support Policy for Persons with Disabilities</strong></p>
              <p>In accordance with the Decree of the President of the Republic of Uzbekistan No. PF-5712 dated April 29, 2019, and the Concept for the Development of Inclusive Education in 2020-2025, Karshi State University identifies the creation of an equal, accessible, and high-quality educational environment for students with special educational needs as a priority task.</p>
              <p>This policy is aimed at creating equal opportunities for students, staff, and visitors with disabilities and ensuring their full and effective participation in education, employment, and social life. It is based on the principles of inclusion, non-discrimination, individual approach, confidentiality, and sustainability, and it is implemented in alignment with the Sustainable Development Goals.</p>
              <p><strong>Scope and mandatory cases</strong></p>
              <p>The policy applies to students at all levels of education, academic and administrative staff, visitors, guests, and partner organizations. It covers educational processes, work activities, events, and infrastructure services and is mandatory in the following cases:</p>
              <ul>
                <li>lectures, seminars, and examinations;</li>
                <li>recruitment and employment activities;</li>
                <li>events and public activities;</li>
                <li>use of infrastructure and services.</li>
              </ul>
              <p><strong>Core principles</strong></p>
              <ul>
                <li>equal rights and opportunities for every individual;</li>
                <li>strict prohibition of direct and indirect disability-based discrimination;</li>
                <li>separate assessment of individual needs and tailored support;</li>
                <li>confidential handling of disability-related information;</li>
                <li>continuous and systematic development of support services.</li>
              </ul>
              <p><strong>Support services</strong></p>
              <p>Academic support includes individual learning plans, learning materials in Braille, audio, and digital formats, extra time in examinations, separate conditions, and adapted assessment systems. Teachers receive regular training in inclusive pedagogy.</p>
              <p>Accessibility improvements include ramps, elevators, wide access corridors, accessible restrooms, tactile pathways, and visual and audio signage. Technological support includes screen reader software, speech-to-text and text-to-speech tools, adaptation of online learning platforms to international accessibility standards, and expanded access to specialized equipment and digital library resources.</p>
              <p>Psychological and social support services include professional counseling, stress management and adaptation programs, peer-support systems, and educational activities that help build an inclusive culture.</p>
              <p><strong>Inclusion Support Unit</strong></p>
              <p>The university has established an "Inclusion Support Unit" responsible for:</p>
              <ul>
                <li>identifying needs;</li>
                <li>organizing services;</li>
                <li>conducting monitoring;</li>
                <li>ensuring every faculty and department follows the policy;</li>
                <li>supporting teachers in applying inclusive approaches.</li>
              </ul>
              <p><strong>Monitoring and evaluation</strong></p>
              <p>Policy implementation is assessed through annual audits and reports, feedback from students and staff, KPI tracking, SDG indicators, and a continuous improvement plan.</p>
              <p><strong>Financing</strong></p>
              <p>The financing system follows a sustainable, multi-source approach. Primary funds are allocated from the university budget, while additional resources are attracted through government programs, international grants, private-sector partnerships, donor organizations, sponsorships, and joint social initiatives. This mechanism supports infrastructure adaptation, assistive technology procurement, specialist training, and the long-term sustainability of services.</p>
            </div>
        """,
    },
}


FINANCIAL_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Reja-moliya bo'limi",
        "intro": "Reja-moliya bo'limi РІР‚вЂќ Qarshi davlat universiteti sahifasi, 24-fevral 2025 sanasi bilan joylangan.",
        "leader_title": "Bo'lim boshlig'i",
        "leader_name": "Xolbayev Sodiq Utaganovich",
        "leader_role": "Reja-moliya bo'limi boshlig'i",
        "leader_details": [
            "Telefon: +998 90 428 00 38",
            "Elektron pochta: Rejamoliya@mail.ru",
            "Qabul kunlari: Dushanba-Juma, 09:00 dan 16:00 gacha",
        ],
        "image_url": "/static/images/staff/reja-moliya.jpg",
        "sections": [
            {
                "title": "Mehnat faoliyati",
                "bullets": [
                    "1983-1983 yy. РІР‚вЂќ Dehqonobod tumani \"Krupskaya\" nomli jamoa xo'jaligida hisobchi",
                    "1983-1985 yy. РІР‚вЂќ muddatli harbiy xizmat chaqiriluvchisi",
                    "1985-1986 yy. РІР‚вЂќ Dehqonobod tumani \"Krupskaya\" nomli jamoa xo'jaligida chorva bo'yicha hisobchi",
                    "1986-1997 yy. РІР‚вЂќ Nishon tumani \"Salvador Alyendi\" nomli jamoa xo'jaligida hisobchi",
                    "1997-2004 yy. РІР‚вЂќ Qarshi davlat universiteti Reja-moliya bo'limi boshlig'i",
                    "2004-2005 yy. РІР‚вЂќ Qarshi davlat universitetida bosh hisobchi",
                    "2005 yildan hozirga qadar РІР‚вЂќ Qarshi davlat universiteti Reja-moliya bo'limi boshlig'i",
                ],
            },
            {
                "title": "Bo'lim tarixi",
                "paragraphs": [
                    "Reja-moliya bo'limi universitet tashkil qilinganidan buyon faoliyat yuritib keladi. 1992-yildan boshlab alohida bo'lim sifatida ishlamoqda.",
                ],
            },
            {
                "title": "Asosiy vazifalari",
                "paragraphs": [
                    "OTM faoliyatini takomillashtirish, budjet va budjetdan tashqari mablag'lar bo'yicha daromad hamda xarajatlar smetasini tuzish, iqtisodiy tahlil o'tkazish, namunaviy shtatlar jadvalining to'g'ri yuritilishini nazorat qilish va universitet faoliyatini muntazam moliyalashtirib borish.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Planning and Finance Department",
        "intro": "Planning and Finance Department page of Karshi State University, published on February 24, 2025.",
        "leader_title": "Head of the department",
        "leader_name": "Xolbayev Sodiq Utaganovich",
        "leader_role": "Head of the Planning and Finance Department",
        "leader_details": [
            "Phone: +998 90 428 00 38",
            "Email: Rejamoliya@mail.ru",
            "Reception days: Monday-Friday, from 09:00 to 16:00",
        ],
        "image_url": "/static/images/staff/reja-moliya.jpg",
        "sections": [
            {
                "title": "Professional background",
                "bullets": [
                    "1983-1983 РІР‚вЂќ Accountant at the \"Krupskaya\" collective farm, Dehqonobod district",
                    "1983-1985 РІР‚вЂќ Conscript in compulsory military service",
                    "1985-1986 РІР‚вЂќ Livestock accountant at the \"Krupskaya\" collective farm, Dehqonobod district",
                    "1986-1997 РІР‚вЂќ Accountant at the \"Salvador Allende\" collective farm, Nishon district",
                    "1997-2004 РІР‚вЂќ Head of the Planning and Finance Department, Karshi State University",
                    "2004-2005 РІР‚вЂќ Chief accountant at Karshi State University",
                    "Since 2005 РІР‚вЂќ Head of the Planning and Finance Department, Karshi State University",
                ],
            },
            {
                "title": "Department history",
                "paragraphs": [
                    "The Planning and Finance Department has been operating since the establishment of the university. Since 1992, it has functioned as an independent department.",
                ],
            },
            {
                "title": "Main responsibilities",
                "paragraphs": [
                    "Improving the activities of the higher education institution, preparing income and expenditure estimates for budgetary and extra-budgetary funds, conducting economic analysis, monitoring the proper maintenance of standard staffing schedules, and ensuring the regular financing of university operations.",
                ],
            },
        ],
    },
}


WOMEN_SUPPORT_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Xotin-qizlar bilan ishlash va psixologik maslahat markazi",
        "intro": "Xotin-qizlar bilan ishlash va psixologik maslahat markazi sahifasi. URL eski nom bilan ochiladi: xotin-qizlar-maslahat-kengashi.",
        "leader_title": "Rahbar",
        "leader_name": "Karamova Shoxida Luftillayevna",
        "leader_role": "Xotin-qizlar bilan ishlash va psixologik maslahat markazi boshlig'i, filologiya fanlari bo'yicha falsafa doktori, dotsent.",
        "leader_details": [
            "Telefon: +998 97 229-69-27",
            "Elektron pochta: sh.l.karamova@qardu.uz",
            "Qabul kunlari: haftaning juft kunlari, 09:00 dan 17:00 gacha",
        ],
        "image_url": "/static/images/staff/karomova.jpg",
        "sections": [
            {
                "title": "Mehnat faoliyati",
                "bullets": [
                    "2018-2020 yy. РІР‚вЂќ Qarshi davlat universiteti adabiyotshunoslik kafedrasi o'qituvchisi",
                    "2020-2022 yy. РІР‚вЂќ Qarshi davlat universiteti adabiyotshunoslik kafedrasi katta o'qituvchisi",
                    "2022-2023 yy. РІР‚вЂќ Qarshi davlat universiteti xotin-qizlar maslahat kengashi raisi",
                    "2023 yildan hozirgacha РІР‚вЂќ Qarshi davlat universiteti xotin-qizlar bilan ishlash va psixologik maslahat markazi boshlig'i.",
                ],
            },
            {
                "title": "Bo'lim tarixi",
                "paragraphs": [
                    "2023-yil 6-martgacha universitet xotin-qizlar kengashi faoliyat yuritgan. 2023-yil 7-martdan boshlab Qarshi davlat universiteti rektorining 111-X-sonli buyrug'i asosida Xotin-qizlar bilan ishlash va psixologik maslahat markazi ish boshlagan.",
                ],
            },
            {
                "title": "Asosiy vazifalari",
                "bullets": [
                    "talaba-qizlarning axloqiy va estetik madaniyatini, ijtimoiy-siyosiy faolligini oshirish;",
                    "ularni kasb-hunarga yo'naltirish va bo'sh vaqtini mazmunli tashkil etish;",
                    "talabalar turar joylaridagi xotin-qizlar o'rtasida ma'naviy-axloqiy va tarbiyaviy ishlarni kuchaytirish;",
                    "TTJlarda ijodiy, kasbiy va badiiy to'garak-klublar faoliyatini kuchaytirish;",
                    "yordamga muhtoj, og'ir ijtimoiy ahvoldagi xotin-qizlarni aniqlash va ularga ijtimoiy-huquqiy, psixologik hamda moddiy yordam ko'rsatish;",
                    "xotin-qizlarga nisbatan tazyiq va zo'ravonlik holatlarini aniqlash bo'yicha so'rovnomalar o'tkazish;",
                    "notinch oilalardagi talaba-qizlarga alohida e'tibor qaratish;",
                    "ijarada yashovchi talaba-qizlarning yashash sharoitlarini o'rganish va manzillariga tashrif buyurish.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Center for Work with Women and Psychological Counseling",
        "intro": "Center for Work with Women and Psychological Counseling page. The URL still opens under the former name: xotin-qizlar-maslahat-kengashi.",
        "leader_title": "Head",
        "leader_name": "Karamova Shoxida Luftillayevna",
        "leader_role": "Head of the Center for Work with Women and Psychological Counseling, Doctor of Philosophy in Philology, Associate Professor.",
        "leader_details": [
            "Phone: +998 97 229-69-27",
            "Email: sh.l.karamova@qardu.uz",
            "Reception days: even weekdays, from 09:00 to 17:00",
        ],
        "image_url": "/static/images/staff/karomova.jpg",
        "sections": [
            {
                "title": "Professional background",
                "bullets": [
                    "2018-2020 РІР‚вЂќ Teacher at the Department of Literary Studies, Karshi State University",
                    "2020-2022 РІР‚вЂќ Senior teacher at the Department of Literary Studies, Karshi State University",
                    "2022-2023 РІР‚вЂќ Chair of the Women's Advisory Council, Karshi State University",
                    "Since 2023 РІР‚вЂќ Head of the Center for Work with Women and Psychological Counseling, Karshi State University.",
                ],
            },
            {
                "title": "Department history",
                "paragraphs": [
                    "Until March 6, 2023, the university's Women's Council operated at the institution. Starting from March 7, 2023, the Center for Work with Women and Psychological Counseling began its work on the basis of Order No. 111-X of the Rector of Karshi State University.",
                ],
            },
            {
                "title": "Main responsibilities",
                "bullets": [
                    "improving the moral, aesthetic, and socio-political engagement of female students;",
                    "guiding them toward professions and organizing their free time meaningfully;",
                    "strengthening spiritual, moral, and educational work among women in student dormitories;",
                    "expanding the activities of creative, professional, and artistic clubs in dormitories;",
                    "identifying women in need and in difficult social conditions and providing them with social, legal, psychological, and material support;",
                    "conducting surveys to identify cases of pressure and violence against women;",
                    "paying special attention to female students from troubled families;",
                    "studying the living conditions of female students living in rented housing and visiting their addresses.",
                ],
            },
        ],
    },
}


YOUTH_AFFAIRS_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Yoshlar bilan ishlash bo'limi",
        "intro": "Yoshlar bilan ishlash bo'limi boshlig'i va bo'lim faoliyati bo'yicha batafsil ma'lumotlar.",
        "leader_title": "Bo'lim boshlig'i",
        "leader_name": "Norbek Pardaqulov Pardaqulovich",
        "leader_role": "Yoshlar bilan ishlash bo'limi boshlig'i.",
        "leader_details": [
            "Telefon: +998 97 070-77-90",
            "Elektron pochta: norbekpx90@umail.com",
            "Qabul kunlari: har kuni soat 9:00 dan 18:00 gacha",
        ],
        "image_url": "/static/images/staff/yoshlar-bilan-ishlash.jpg",
        "sections": [
            {
                "title": "Mehnat faoliyati",
                "paragraphs": [
                    "U mehnat faoliyatini 2012-yilda Qarshi shahridagi 35-umumiy o'rta ta'lim maktabida psixolog sifatida boshlagan. 2015-yildan 2023-yilgacha Qarshi davlat universitetida turli lavozimlarda, jumladan Talabalar shaharchasi direktori, Pedagogika kafedrasi o'qituvchisi va Pedagogika fakulteti tyutori sifatida ishlagan. 2023-yildan hozirgacha Qarshi davlat universiteti Yoshlar bilan ishlash bo'limi boshlig'i lavozimida faoliyat yuritmoqda.",
                ],
            },
            {
                "title": "Bo'lim tarixi",
                "paragraphs": [
                    "Mazkur bo'lim Qarshi davlat universiteti rektorining 2023-yil 16-noyabrdagi buyrug'i bilan tashkil etilgan. Sahifada buyruq raqami ko'rsatilmagan, joyi bo'sh qolgan va bu qism draft holatda qolgan.",
                ],
            },
            {
                "title": "Asosiy vazifalari",
                "paragraphs": [
                    "Bo'lim talaba-yoshlarga ta'lim olishda va bo'sh vaqtlarini mazmunli tashkil etishda ko'maklashadi, ularni insonparvarlik, adolat, mehnatsevarlik va Vatanga muhabbat ruhida tarbiyalashga qaratilgan ishlarni olib boradi.",
                    "Shuningdek, tyutorlarning TTJda, ijarada va xususiy xonadonlarda yashovchi talabalar holatini o'rganishini tashkil etadi, yashash sharoitlari va muammolarini aniqlash hamda yaxshilash choralarini ko'radi.",
                    "Bo'lim talabalar qonuniy manfaatlarini himoya qilish, ularga o'qish, ilm-fan, yashash va dam olish uchun zarur sharoitlar yaratishga amaliy yordam ko'rsatish bilan ham shug'ullanadi. Faoliyat amaldagi qonunchilik, ichki tartib-qoidalar, odob-axloq kodeksi va bo'lim nizomi asosida yuritiladi.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Youth Affairs Department",
        "intro": "Detailed information about the head of the Youth Affairs Department and the department's work.",
        "leader_title": "Head of the department",
        "leader_name": "Norbek Pardaqulov Pardaqulovich",
        "leader_role": "Head of the Youth Affairs Department.",
        "leader_details": [
            "Phone: +998 97 070-77-90",
            "Email: norbekpx90@umail.com",
            "Reception days: every day from 9:00 to 18:00",
        ],
        "image_url": "/static/images/staff/yoshlar-bilan-ishlash.jpg",
        "sections": [
            {
                "title": "Professional background",
                "paragraphs": [
                    "He began his professional career in 2012 as a psychologist at School No. 35 in Qarshi city. From 2015 to 2023, he worked at Karshi State University in various roles, including Director of the Student Campus, Lecturer at the Department of Pedagogy, and Tutor of the Faculty of Pedagogy. Since 2023, he has been serving as Head of the Youth Affairs Department at Karshi State University.",
                ],
            },
            {
                "title": "Department history",
                "paragraphs": [
                    "This department was established by an order of the Rector of Karshi State University dated November 16, 2023. The order number is not indicated on the original source page and that part appears to have remained in draft form.",
                ],
            },
            {
                "title": "Main responsibilities",
                "paragraphs": [
                    "The department supports students in their studies and in organizing their free time meaningfully, while carrying out activities aimed at educating them in the spirit of humanism, justice, diligence, and love for the homeland.",
                    "It also organizes the work of tutors who study the conditions of students living in dormitories, rental housing, and private homes, identify their living conditions and problems, and help improve them.",
                    "The department is also responsible for protecting the legal interests of students and providing practical support in creating proper conditions for study, research, living, and recreation. Its work is carried out on the basis of current legislation, internal regulations, the code of ethics, and the department regulation.",
                ],
            },
        ],
    },
}


TRADE_UNION_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Qarshi davlat universiteti xodimlari va talabalari kasaba uyushma qo'mitasi",
        "intro": "Qarshi davlat universiteti xodimlari va talabalari kasaba uyushma qo'mitasi bo'yicha batafsil ma'lumotlar.",
        "leader_title": "Qo'mita raisi",
        "leader_name": "Norov Abdisait Muradovich",
        "leader_role": "Kasaba uyushma qo'mitasi raisi (2020-yil 23-iyuldan buyon).",
        "leader_details": [
            "Telefon: +998 90 721-31-13 (telegram ham shu nomerda)",
            "Elektron pochta: qardukasaba@umail.uz",
        ],
        "image_url": "/static/images/staff/norov.jpg",
        "sections": [
            {
                "title": "Kasaba uyushma qo'mitasi raisining ish rejimi",
                "bullets": [
                    "Ish haftasi - 6 kunlik (dushanba-shanba).",
                    "Dushanba-Juma kunlari: 09:00 dan 18:00 gacha.",
                    "Shanba kuni (qisqartirilgan ish kuni): 09:00 dan 13:00 gacha.",
                    "Tushlik tanaffus: 13:00 dan 14:00 gacha (Dushanba-Juma kunlari).",
                    "Yakshanba - dam olish kuni hisoblanadi.",
                ],
            },
            {
                "title": "Qabul kunlari va tartibi",
                "bullets": [
                    "Seshanba: 10:00 dan 13:00 gacha.",
                    "Payshanba: 14:00 dan 17:00 gacha.",
                    "Shanba kuni qabul o'tkazilmaydi, ushbu kun ichki tashkiliy ishlar uchun ajratiladi.",
                    "Zarur hollarda fuqarolar va xodimlar navbatdan tashqari qabul qilinishi mumkin.",
                ],
            },
            {
                "title": "Vazifalari",
                "bullets": [
                    "Xodimlar mehnat huquqlarini himoya qiladi.",
                    "Ish beruvchi bilan kelishmovchiliklarda xodimlar tomonini qo'llab-quvvatlaydi.",
                    "Adolatsiz ishdan bo'shatish yoki jazolarga qarshi yordam beradi.",
                    "Ish joyidagi xavfsizlik va qulaylikni nazorat qiladi.",
                    "Ish vaqti, dam olish va ta'til masalalarini ko'rib chiqadi.",
                    "Moddiy yordam, nafaqa yoki imtiyozlar ajratishda ko'maklashadi.",
                    "Sog'lomlashtirish, sanatoriy va dam olish yo'llanmalarini tashkil qiladi.",
                    "Bayramlar, sport musobaqalari va turli tadbirlar tashkil etadi.",
                    "Ish beruvchi bilan jamoaviy shartnomalar tuzishda qatnashadi va xodimlar manfaatini himoya qiladi.",
                    "Talabalar manfaatlarini himoya qiladi hamda ijtimoiy yordam, stipendiya va yashash sharoitlari bo'yicha yordam beradi.",
                    "Barcha xodim va talabalar uchun teng imkoniyatlar yaratilishini qo'llab-quvvatlaydi.",
                    "Jins, millat, til, din yoki ijtimoiy holatga qarab kamsitishlarning oldini oladi.",
                    "Nogironligi bo'lgan shaxslar uchun qulay muhit yaratishga ko'maklashadi.",
                    "Inklyuziv ta'lim va ish muhitini rivojlantirishga hissa qo'shadi.",
                    "Turli guruhlar o'rtasida o'zaro hurmat va bag'rikenglik muhitini mustahkamlaydi.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Trade Union Committee of Employees and Students of Karshi State University",
        "intro": "Detailed information about the trade union committee of employees and students of Karshi State University.",
        "leader_title": "Chairperson of the committee",
        "leader_name": "Norov Abdisait Muradovich",
        "leader_role": "Chairperson of the trade union committee (since July 23, 2020).",
        "leader_details": [
            "Phone: +998 90 721-31-13 (also available on Telegram)",
            "Email: qardukasaba@umail.uz",
        ],
        "image_url": "/static/images/staff/norov.jpg",
        "sections": [
            {
                "title": "Working schedule of the trade union committee chairperson",
                "bullets": [
                    "Workweek - 6 days (Monday-Saturday).",
                    "Monday-Friday: from 09:00 to 18:00.",
                    "Saturday (shortened working day): from 09:00 to 13:00.",
                    "Lunch break: 13:00-14:00 (Monday-Friday).",
                    "Sunday is a day off.",
                ],
            },
            {
                "title": "Reception days and procedures",
                "bullets": [
                    "Tuesday: 10:00-13:00.",
                    "Thursday: 14:00-17:00.",
                    "No reception is held on Saturdays; this day is allocated for internal organizational work.",
                    "In necessary cases, citizens and staff may be received outside scheduled hours.",
                ],
            },
            {
                "title": "Functions of the trade union committee",
                "bullets": [
                    "Protects employees' labor rights.",
                    "Supports employees in disputes with the employer.",
                    "Provides assistance against unfair dismissal or disciplinary actions.",
                    "Monitors workplace safety and comfort.",
                    "Reviews issues related to working hours, rest, and leave.",
                    "Assists in providing financial aid, benefits, and allowances.",
                    "Organizes health improvement activities, including sanatoriums and holiday trips.",
                    "Organizes celebrations, sports competitions, and various events.",
                    "Participates in concluding collective agreements with the employer while protecting employees' interests.",
                    "Protects students' interests and provides support on social assistance, scholarships, and living conditions.",
                    "Promotes equal opportunities for all employees and students.",
                    "Prevents discrimination based on gender, nationality, language, religion, or social status.",
                    "Supports the creation of an accessible environment for persons with disabilities.",
                    "Contributes to the development of inclusive education and workplace environments.",
                    "Fosters mutual respect and tolerance among different groups.",
                ],
            },
        ],
    },
}


DISABILITY_SUPPORT_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Inklyuziv qo'llab-quvvatlash markazi",
        "intro": "Nogironligi bo'lgan talabalar, xodimlar va tashrif buyuruvchilar uchun teng imkoniyatlarni ta'minlashga mas'ul markaz.",
        "leader_title": "Markaz rahbari",
        "leader_name": "Nurbek Farmonov",
        "leader_role": "Inklyuziv qo'llab-quvvatlash markazi rahbari (volontyorlik asosida).",
        "leader_details": [
            "Telefon: +998979500620",
            "Elektron pochta: nurbekfarmonov4@gmail.com",
            "Qabul kunlari: Dushanba 10:00-13:00, Chorshanba 14:00-17:00",
        ],
        "image_url": "/static/images/staff/farmonov.jpg",
        "image_fallback_url": "/meedia/farmonov.jpg",
        "sections": [
            {
                "title": "Asosiy vazifalari",
                "bullets": [
                    "nogironligi bo'lgan shaxslarning ehtiyojlarini aniqlash va individual qo'llab-quvvatlash choralarini ishlab chiqish",
                    "akademik va ijtimoiy moslashuv jarayonlarini tashkil etish va muvofiqlashtirish",
                    "inklyuziv ta'lim muhitini rivojlantirish va fakultetlar bilan hamkorlikda ishlash",
                    "assistiv texnologiyalar va moslashtirilgan xizmatlarni joriy etishni ta'minlash",
                    "psixologik va ijtimoiy yordam xizmatlarini yo'lga qo'yish",
                    "nogironligi bo'lgan shaxslar huquqlarini himoya qilish va diskriminatsiyaning oldini olish",
                    "talabalar va xodimlar o'rtasida inklyuziv madaniyatni shakllantirishga qaratilgan tadbirlarni tashkil etish",
                    "monitoring va baholash jarayonlarini olib borish hamda tegishli hisobotlarni tayyorlash",
                ],
            },
            {
                "title": "Volontyorlik asosidagi faoliyat",
                "paragraphs": [
                    "Mazkur faoliyat Nurbek Farmonov tomonidan volontyorlik asosida amalga oshiriladi va bu uning ijtimoiy mas'uliyat, insonparvarlik hamda jamiyatda teng imkoniyatlarni rivojlantirishga bo'lgan sadoqatini ifodalaydi.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Inclusion Support Center",
        "intro": "The center responsible for ensuring equal opportunities for students, staff, and visitors with disabilities.",
        "leader_title": "Head of the center",
        "leader_name": "Nurbek Farmonov",
        "leader_role": "Head of the Inclusion Support Center (on a voluntary basis).",
        "leader_details": [
            "Phone: +998979500620",
            "Email: nurbekfarmonov4@gmail.com",
            "Reception days: Monday 10:00-13:00, Wednesday 14:00-17:00",
        ],
        "image_url": "/static/images/staff/farmonov.jpg",
        "image_fallback_url": "/meedia/farmonov.jpg",
        "sections": [
            {
                "title": "Main responsibilities",
                "bullets": [
                    "identifying the needs of persons with disabilities and developing individualized support measures",
                    "organizing and coordinating academic and social adaptation processes",
                    "promoting an inclusive educational environment and collaborating with faculties",
                    "ensuring the implementation of assistive technologies and adapted services",
                    "establishing psychological and social support services",
                    "protecting the rights of persons with disabilities and preventing discrimination",
                    "organizing activities aimed at fostering an inclusive culture among students and staff",
                    "conducting monitoring and evaluation processes and preparing relevant reports",
                ],
            },
            {
                "title": "Voluntary basis",
                "paragraphs": [
                    "This activity is carried out by Nurbek Farmonov on a voluntary basis, reflecting his strong commitment to social responsibility, humanity, and the promotion of equal opportunities in society.",
                ],
            },
        ],
    },
}


STUDENT_UNION_CONTACT_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Talabalar kengashi",
        "intro": "Talaba-yoshlar huquqlari, faolligi va tashabbuslarini qo'llab-quvvatlashga mas'ul vakil ma'lumotlari.",
        "leader_title": "Boshlang'ich tashkilot yetakchisi",
        "leader_name": "Ravshanov Doston Rustam o'g'li",
        "leader_role": "O'zbekiston Yoshlar ittifoqi Qarshi davlat universiteti boshlang'ich tashkilot yetakchisi",
        "leader_details": [
            "Telefon: +998 90 882 28 80",
            "Elektron pochta: dostonravshanov1996@gmail.com",
            "Qabul kunlari: Dushanba-Juma 9:00-18:00 gacha",
        ],
        "image_url": "/static/images/staff/dossi.jpg",
        "image_fallback_url": "/meedia/dossi.jpg",
        "sections": [
            {
                "title": "Mehnat faoliyati",
                "bullets": [
                    "2021-2022-y.y. Qarshi davlat universiteti Ma'naviy-ma'rifiy ishlarni tashkil etish bo'limi bosh mutaxassisi",
                    "2022-2024-y.y. Qarshi davlat universitetida Talabalarni turar joy bilan ta'minlash ishlarini tashkil etishni muvofiqlashtiruvchi bo'limi bosh mutaxassisi",
                    "2024-yildan O'zbekiston yoshlar ittifoqi Qarshi davlat universiteti boshlang'ich tashkilot yetakchisi",
                ],
            },
            {
                "title": "Vazifalari",
                "bullets": [
                    "Yoshlar yetakchisi boshlang'ich tashkilot ishlarini boshqaradi va umumiy faoliyatni yo'lga qo'yadi.",
                    "Universitet kengashi yig'ilishlarida yoshlar vakili sifatida qatnashadi, talaba-yoshlarning fikr-mulohazalari, taklif va tashabbuslarini ilgari suradi hamda qabul qilinayotgan qarorlarda ularning manfaatlari inobatga olinishi uchun faol ishtirok etadi.",
                    "Fakultetlar va guruhlardagi yoshlar yetakchilari ishini bir tizimga soladi, ularga metodik yordam beradi.",
                    "Talabalarning huquq va manfaatlarini himoya qiladi, ularning muammolarini rahbariyatga yetkazadi.",
                    "Talabalar tomonidan ilgari surilgan g'oya va loyihalarni rivojlantirishga yordam beradi.",
                    "Universitet ichida va yuqori tashkilotlar bilan aloqalarni olib boradi.",
                    "Olib borilgan ishlar yuzasidan muntazam ravishda hisobot beradi.",
                    "Yuqori tashkilotlar va universitet rahbariyati tomonidan berilgan vazifalarni bajaradi.",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Student Union",
        "intro": "Contact details for the representative responsible for supporting student rights, engagement, and youth initiatives.",
        "leader_title": "Leader of the primary organization",
        "leader_name": "Ravshanov Doston Rustam o'g'li",
        "leader_role": "Leader of the Primary Organization of the Youth Union of Uzbekistan at Karshi State University",
        "leader_details": [
            "Phone: +998 90 882 28 80",
            "Email: dostonravshanov1996@gmail.com",
            "Reception hours: Monday-Friday from 09:00 to 18:00",
        ],
        "image_url": "/static/images/staff/dossi.jpg",
        "image_fallback_url": "/meedia/dossi.jpg",
        "sections": [
            {
                "title": "Work Experience",
                "bullets": [
                    "2021-2022 РІР‚вЂњ Chief Specialist, Department for the Organization of Spiritual and Educational Activities, Karshi State University",
                    "2022-2024 РІР‚вЂњ Chief Specialist, Department for Coordination of Student Accommodation, Karshi State University",
                    "Since 2024 РІР‚вЂњ Leader of the Primary Organization of the Youth Union of Uzbekistan at Karshi State University",
                ],
            },
            {
                "title": "Responsibilities",
                "bullets": [
                    "Manages the activities of the primary organization and ensures the effective functioning of its overall operations.",
                    "Takes part in University Council meetings as a representative of youth, presents students' opinions, proposals, and initiatives, and actively contributes to ensuring that their interests are considered in decision-making processes.",
                    "Coordinates the work of youth leaders across faculties and groups and provides them with methodological support.",
                    "Safeguards the rights and interests of students and communicates their concerns to the university administration.",
                    "Encourages and supports ideas and projects initiated by students.",
                    "Represents the organization within the university and in relations with higher-level institutions.",
                    "Regularly provides reports on the activities carried out.",
                    "Ensures the execution of tasks assigned by higher organizations and the university administration.",
                ],
            },
        ],
    },
}


GOVERNANCE_PAGE_CONTENT = {
    "sdg-policy": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Barqarorlik siyosati",
        "title_en": "Sustainability Policy",
        "intro_uz": "Qarshi davlat universitetining atrof-muhit barqarorligi, resurslardan oqilona foydalanish va ekologik mas'uliyatni kuchaytirishga qaratilgan institutsional siyosati.",
        "intro_en": "Karshi State University's institutional policy on environmental sustainability, responsible resource use, and stronger environmental accountability.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>Qarshi davlat universiteti atrof-muhit barqarorligi siyosati</strong></p>
              <p><strong>Kirish.</strong> Qarshi Davlat Universiteti (QDU) barqaror va ekologik mas'uliyatli akademik muhitni rivojlantirishga sodiqdir. Ta'lim, tadqiqot va jamoatchilik bilan hamkorlikka bag'ishlangan muassasa sifatida QDU atrof-muhit barqarorligini targ'ib qilish va ekologik izini kamaytirishda o'z rolini anglaydi. Ushbu siyosat barqaror amaliyotlarga, resurslardan oqilona foydalanishga va atrof-muhitni muhofaza qilishda doimiy takomillashuvga bo'lgan majburiyatimizni bayon etadi.</p>
              <p><strong>Maqsadlar.</strong> Qarshi Davlat Universiteti (QDU) o'z faoliyatida atrof-muhit barqarorligini ustuvor yo'nalishlardan biri sifatida belgilaydi va uni universitetning ta'lim, ilmiy-tadqiqot hamda boshqaruv jarayonlariga tizimli ravishda integratsiya qilishni maqsad qiladi. Ushbu siyosat universitet faoliyatining barcha bosqichlarida barqarorlik tamoyillarini joriy etish, tabiiy resurslardan oqilona foydalanish hamda ekologik mas'uliyatni kuchaytirishga qaratilgan. Shu bilan birga, issiqxona gazlari chiqindilarini kamaytirish, energiya samaradorligini oshirish, suv va chiqindilarni boshqarishda ilg'or yondashuvlarni qo'llash, shuningdek, barqaror transport va iste'mol madaniyatini rivojlantirish asosiy ustuvor vazifalar sifatida e'tirof etiladi. Universitet o'z faoliyatida milliy va xalqaro ekologik me'yorlar hamda standartlarga qat'iy amal qilish bilan birga, barqarorlik tashabbuslarini kengaytirish maqsadida turli darajadagi hamkorlik aloqalarini rivojlantirishni qo'llab-quvvatlaydi.</p>
              <p><strong>Energiya va iqlim harakati.</strong> Energiya va iqlim harakati doirasida universitet barcha binolar va inshootlarda energiya samaradorligini oshirishga alohida e'tibor qaratadi. Zamonaviy energiya tejovchi texnologiyalarni joriy etish, aqlli resurslarni boshqarish tizimlaridan foydalanish hamda imkoniyat darajasida qayta tiklanadigan energiya manbalariga o'tish orqali karbonat angidrid chiqindilarini kamaytirish ko'zda tutiladi. Shu bilan birga, universitet hamjamiyati orasida energiya tejash madaniyatini shakllantirish muhim vazifalardan biri hisoblanadi.</p>
              <p><strong>Suvni tejash va boshqarish.</strong> Suv resurslarini boshqarish siyosati suvdan samarali va tejamkor foydalanishni ta'minlashga qaratilgan bo'lib, suv isrofini minimallashtirish ustuvor ahamiyatga ega. Universitet tomchilab sug'orish texnologiyalarini joriy etish, chiqindi suvlarni qayta ishlash imkoniyatlarini kengaytirish hamda axborot-targ'ibot ishlari orqali mas'uliyatli suv iste'molini rivojlantirishga intiladi. Bu jarayonda talabalar va xodimlarning ekologik ongini oshirish muhim o'rin tutadi.</p>
              <p><strong>Chiqindilarni qayta ishlash va kamaytirish.</strong> Chiqindilarni boshqarish yo'nalishida universitet chiqindilarni kamaytirish, saralash va qayta ishlash tizimini takomillashtirishga alohida e'tibor beradi. Bir martalik plastmassa mahsulotlaridan foydalanishni qisqartirish, ekologik jihatdan barqaror muqobillarni joriy etish hamda chiqindilar bilan mas'uliyatli muomala qilish madaniyatini shakllantirish asosiy vazifalardan hisoblanadi. Shu bilan birga, chiqindilarni samarali boshqarish bo'yicha mahalliy tashkilotlar bilan hamkorlik qilish orqali tizimli natijalarga erishish ko'zda tutiladi.</p>
              <p><strong>Barqaror transport.</strong> Barqaror transportni rivojlantirish maqsadida universitet xodimlar va talabalar orasida jamoat transporti, velosiped hamda avtohamkorlik (carpooling)dan foydalanishni rag'batlantiradi. Ekologik transport infratuzilmasini rivojlantirish, jumladan velosipedlar uchun maxsus joylar va elektromobillarni quvvatlash stansiyalarini tashkil etish, shuningdek, universitet transport vositalarini past uglerodli alternativalarga bosqichma-bosqich o'tkazish rejalashtirilgan.</p>
              <p><strong>Barqaror xarid va iste'mol.</strong> Barqaror xarid va iste'mol siyosati doirasida universitet ekologik toza, ijtimoiy va axloqiy jihatdan maqbul mahsulotlarni xarid qilishga ustuvorlik beradi. Raqamlashtirish jarayonlarini kengaytirish orqali qog'oz sarfini kamaytirish, mas'uliyatli chop etish amaliyotlarini joriy etish hamda universitet hududida barqaror oziq-ovqat va ovqatlanish xizmatlarini rivojlantirish ko'zda tutiladi.</p>
              <p><strong>Barqarorlik bo'yicha ta'lim va tadqiqot.</strong> Ta'lim va tadqiqot faoliyatida barqarorlikni integratsiya qilish universitet siyosatining muhim tarkibiy qismi hisoblanadi. O'quv dasturlari va ilmiy-tadqiqot loyihalarida atrof-muhit muammolari va barqaror rivojlanish masalalarini keng yoritish, professor-o'qituvchilar va talabalar tomonidan amalga oshirilayotgan tashabbuslarni qo'llab-quvvatlash, shuningdek, seminarlar, treninglar va ilmiy tadbirlar orqali ekologik bilim va ko'nikmalarni rivojlantirish ustuvor vazifalar sirasiga kiradi.</p>
              <p><strong>Jamoatchilik bilan hamkorlik va hamkorlik loyihalari.</strong> Jamoatchilik bilan hamkorlik universitetning barqarorlik strategiyasida alohida ahamiyat kasb etadi. Universitet mahalliy hamjamiyatlar, davlat tashkilotlari va xalqaro hamkorlar bilan hamkorlikda barqaror rivojlanish maqsadlariga erishishni ko'zlaydi. Shu bilan birga, talabalarni ekologik tashabbuslar va jamoat xizmatlariga jalb qilish orqali ularning ijtimoiy faolligini oshirishga intiladi.</p>
              <p><strong>Monitoring va doimiy takomillashtirish.</strong> Barqarorlik siyosatini samarali amalga oshirish uchun monitoring va doimiy takomillashtirish mexanizmlari joriy etiladi. Asosiy ko'rsatkichlar (KPI) ishlab chiqilib, barqarorlik tashabbuslari natijalari muntazam ravishda baholanadi. Atrof-muhitga ta'sirni tahlil qilish asosida siyosat doimiy ravishda yangilanib, zamonaviy talablar va yangi imkoniyatlarga moslashtiriladi.</p>
              <p><strong>Amalga oshirish va mas'uliyat.</strong> Mazkur siyosatning amalga oshirilishini universitetning Barqarorlik qo'mitasi muvofiqlashtiradi va nazorat qiladi. Professor-o'qituvchilar, xodimlar va talabalar ushbu jarayonda faol ishtirok etishlari kutiladi. Shuningdek, tashqi hamkorlar va mutaxassislar bilan hamkorlik qilish orqali barqarorlik tashabbuslarini yanada rivojlantirish rag'batlantiriladi.</p>
              <p>Qarshi Davlat Universiteti barqarorlikni o'zining ajralmas institutsional qadriyatiga aylantirishga sodiq bo'lib, ushbu siyosat orqali atrof-muhitni muhofaza qilish, resurslardan oqilona foydalanish va kelajak avlodlar uchun barqaror muhit yaratish borasidagi majburiyatini yana bir bor tasdiqlaydi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>Environmental sustainability policy of Karshi State University</strong></p>
              <p><strong>Introduction.</strong> Karshi State University (KSU) recognizes environmental sustainability as a core institutional priority and is committed to systematically integrating sustainability principles into its academic, research, and operational activities. This policy aims to embed sustainability across all levels of university functions, promote the responsible use of natural resources, and strengthen environmental accountability. In this context, reducing greenhouse gas emissions, improving energy efficiency, ensuring responsible water and waste management, and promoting sustainable transportation and consumption practices are identified as key priorities. The University is also committed to complying with national and international environmental standards while fostering collaboration with partners at local, national, and global levels to advance sustainability initiatives.</p>
              <p><strong>Objectives.</strong> Within the framework of energy and climate action, the University prioritizes improving energy efficiency across all buildings and facilities. This includes the implementation of modern energy-saving technologies, the adoption of smart resource management systems, and, where feasible, a gradual transition to renewable energy sources. These measures aim to reduce carbon dioxide emissions while cultivating a culture of energy conservation among students, faculty, and staff.</p>
              <p><strong>Energy and climate action.</strong> The University's water management approach focuses on ensuring efficient and responsible water use, with the objective of minimizing water waste. Efforts include the introduction of water-saving programs, the application of technologies such as drip irrigation, and the exploration of wastewater recycling systems. Additionally, awareness campaigns and training activities are conducted to promote responsible water consumption and enhance environmental awareness within the university community.</p>
              <p><strong>Water conservation and management.</strong> In the area of waste management, the University is committed to developing effective systems for waste reduction, sorting, and recycling. Particular emphasis is placed on reducing the use of single-use plastics and promoting environmentally sustainable alternatives. The University also seeks to foster responsible waste disposal practices among students and staff while strengthening cooperation with local waste management authorities to achieve sustainable outcomes.</p>
              <p><strong>Waste reduction and recycling.</strong> To support sustainable transportation, the University encourages the use of public transport, cycling, and carpooling among students and staff. It aims to develop environmentally friendly transport infrastructure, including bicycle parking facilities and electric vehicle charging stations. Furthermore, the University plans to gradually transition its fleet to low-carbon alternatives in order to reduce transportation-related emissions.</p>
              <p><strong>Sustainable transport.</strong> Sustainable procurement and consumption practices are promoted by prioritizing environmentally friendly and ethically sourced products. The University also seeks to reduce paper usage through digitalization and responsible printing practices, while encouraging sustainable food services and consumption patterns within the campus.</p>
              <p><strong>Sustainable procurement and consumption.</strong> Sustainability is also integrated into education and research activities. The University promotes the inclusion of environmental sustainability topics in academic curricula and research initiatives, supports sustainability-related projects led by faculty and students, and organizes seminars, training sessions, and events to raise awareness of environmental challenges and solutions.</p>
              <p><strong>Sustainability in education and research.</strong> Engagement with the broader community is an essential component of the University's sustainability strategy. The University collaborates with local communities, governmental institutions, and international partners to advance environmental sustainability goals. It also actively involves students in community service and outreach activities focused on sustainability, thereby fostering civic responsibility and environmental stewardship.</p>
              <p><strong>Community engagement and partnership projects.</strong> To ensure effective implementation, the University establishes monitoring and continuous improvement mechanisms. Key performance indicators are defined to track progress, and regular environmental impact assessments are conducted. Based on these evaluations, the policy is periodically reviewed and updated to reflect emerging challenges, opportunities, and best practices.</p>
              <p><strong>Monitoring and continuous improvement.</strong> The implementation of this policy is overseen by the University's Sustainability Committee. Faculty members, staff, and students are expected to actively participate in sustainability initiatives. The University also encourages collaboration with external partners and experts to further enhance its sustainability efforts.</p>
              <p>Karshi State University is committed to embedding sustainability as an integral institutional value. Through this policy, the University reaffirms its dedication to environmental protection, responsible resource management, and the creation of a more sustainable future for its community and beyond.</p>
            </div>
        """,
    },
    "sdg-investment": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Barqaror investitsiya siyosati (2025-2030)",
        "title_en": "Sustainable Investment Policy (2025-2030)",
        "intro_uz": "Investitsiya faoliyatida iqtisodiy samaradorlik, ekologik mas'uliyat va ijtimoiy barqarorlikni uyg'unlashtiruvchi institutsional siyosat.",
        "intro_en": "An institutional policy aligning investment decisions with economic efficiency, environmental responsibility, and social sustainability.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>BARQAROR INVESTITSIYA SIYOSATI (2025-2030)</strong></p>
              <p><strong>Ishlab chiquvchi:</strong> Reja-moliya bo'limi<br><strong>Amal qilish muddati:</strong> 2025-2030 yillar<br><strong>Qamrovi:</strong> Barcha tuzilmaviy bo'linmalar, loyihalar va investitsion faoliyat</p>
              <p>Ushbu siyosat tashkilotning investitsiya faoliyatida iqtisodiy samaradorlik, ekologik mas'uliyat va ijtimoiy barqarorlik tamoyillarini joriy etishni maqsad qiladi. Siyosat O'zbekiston Respublikasining Investitsiyalar va investitsiya faoliyati to'g'risidagi qonuni, xalqaro barqaror rivojlanish tamoyillari va "yashil iqtisodiyot" yondashuvlariga muvofiq ishlab chiqilgan.</p>
              <p><strong>MAQSAD VA VAZIFA</strong></p>
              <p>Barqaror investitsiyalar orqali xarajatlarni optimallashtirish, atrof-muhitga salbiy ta'sirni kamaytirish va ijtimoiy qiymat yaratish maqsad qilingan. Dasturning vazifasi 5-10 yillik iqtisodiy samaradorligini baholash, potensial iqtisodiy risklarni aniqlash va ularni kamaytirish choralarini ishlab chiqish, investitsiya qarorlarini obyektiv asosda qabul qilish, ESG (Environmental, Social, Governance) va barqarorlik qoidalariga muvofiqlikni ta'minlash, ekologik ta'sirni kamaytirish, ijtimoiy qiymat yaratish, moliyaviy risklarni boshqarish, ESG tamoyillarini investitsiya jarayoniga integratsiya qilish hamda korrupsiya xavflarini kamaytirish va shaffoflikni ta'minlashdan iborat.</p>
              <p>Siyosat quyidagi yo'nalishlarga tatbiq etiladi: kapital qo'yilmalar, infratuzilma loyihalari, davlat-xususiy sheriklik loyihalari, xalqaro grantlar, xalqaro moliya institutlari ishtirokidagi investitsiyalar, texnologik va energetik modernizatsiya loyihalari.</p>
              <p><strong>INVESTITSIYA TAMOYILLARI</strong></p>
              <p>Investitsiya faoliyatida ESG (Environmental, Social, Governance), SDG (Sustainable Development Goals), yashil iqtisodiyot tamoyillari va milliy qonunchilik talablari asos qilib olinadi. Innovatsiya tamoyiliga yashil texnologiyalar va raqamli yechimlardan foydalanish kiradi. Ekologik tamoyillarga karbon chiqindilarini kamaytirish, energiya samaradorligi va suv resurslaridan samarali foydalanish kiradi. Ijtimoiy tamoyillar mehnat huquqlariga rioya qilish, sog'liq va xavfsizlik, inklyuziv rivojlanishni qamrab oladi. Boshqaruv tamoyillari esa shaffoflik, korrupsiyaga qarshi siyosat va hisobdorlikni o'z ichiga oladi.</p>
              <p><strong>TAQIQLANGAN INVESTITSIYALAR</strong></p>
              <p>Universitet quyidagi faoliyatlarga investitsiya kiritmaydi: ko'mirga asoslangan energetika loyihalari, tamaki sanoati, qurol ishlab chiqarish, atrof-muhitga jiddiy zarar yetkazuvchi loyihalar va inson huquqlarini buzuvchi kompaniyalar.</p>
              <p><strong>ESG baholash tizimi</strong></p>
              <p>Har bir investitsiya loyihasi ESG mezonlari asosida baholanadi.</p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Mezoni</th>
                      <th>Ball</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Environmental impact</td>
                      <td>30</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Energy efficiency</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Social impact</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Governance</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>5</td>
                      <td>Financial sustainability</td>
                      <td>10</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Minimal ESG ball: 60. 60 balldan past loyihalar moliyalashtirilmaydi. Investitsiya qaror qabul qilish jarayoni loyiha taklifini taqdim etish, moliyaviy tahlil (NPV, IRR, ROI), ESG baholash, risk tahlili va investitsiya qo'mitasi qarori bosqichlarida amalga oshiriladi.</p>
              <p><strong>Loyiha ma'lumotlarini yig'ish</strong></p>
              <p>Investitsiya loyihasi bo'yicha avvalo loyiha turi, qo'llaniladigan texnologiya, faoliyat sohasi, prognoz xarajatlar, daromadlar, moliyaviy oqimlar hamda qarz va moliyalashtirish shartlari to'g'risidagi ma'lumotlar yig'iladi. Shundan so'ng loyiha tasavvuri, maqsadi va amalga oshiriladigan hududi aniqlanadi. Loyiha tavsifi doirasida uning joylashuvi, qo'llaniladigan texnologiya va faoliyat turi batafsil bayon etiladi. Loyiha milliy qonunchilik va xalqaro standartlarga muvofiqligi nuqtai nazaridan huquqiy jihatdan tahlil qilinadi.</p>
              <p>Ekologik tahlilda loyiha faoliyatining havo, suv, tuproq hamda biologik xilma-xillikka ta'siri baholanadi. Ijtimoiy tahlil doirasida aholi salomatligi, bandlik darajasi, migratsiya jarayonlari va ijtimoiy munosabatlarga ta'siri o'rganiladi. Ta'sirlarni baholash bosqichida loyiha natijasida yuzaga kelishi mumkin bo'lgan ijobiy va salbiy ta'sirlar aniqlanadi. Salbiy ta'sirlarni kamaytirish uchun mitigatsiya va kompensatsiya choralari ishlab chiqiladi.</p>
              <p>Monitoring rejasi ishlab chiqilib, unda mas'ullar, nazorat usullari, muddatlar va baholash indikatorlari belgilanadi. Yakuniy bosqichda loyiha bo'yicha qaror qabul qilinadi va uni tasdiqlash yoki takomillashtirish yuzasidan tavsiyalar beriladi. Loyiha iqtisodiy samaradorligi NPV, IRR, ROI va Payback period kabi ko'rsatkichlar orqali aniqlanadi. Risk tahlilida ekologik va ijtimoiy, moliyaviy, operatsion hamda qonunchilik va siyosiy risklar kompleks baholanadi. Ssenariy tahlilida optimistik, pessimistik va asosiy variantlar ishlab chiqiladi. Chuqurlashtirilgan tahlil jarayonida Monte Carlo simulyatsiyalari qo'llanadi hamda chiqindi va energiya xarajatlari hisobga olinadi.</p>
              <p>Loyiha ESG indikatorlari bilan integratsiya qilinadi. Moliyalashtirish manbalari sifatida davlat budjeti, maqsadli jamg'armalar, xalqaro moliya institutlari, yashil obligatsiyalar va xususiy investitsiyalar jalb etiladi. Monitoring va hisobot tizimi orqali yillik KPIlar belgilanadi, ESG hisobotlari tayyorlanadi va aniqlangan kamchiliklar bo'yicha tuzatish choralari ko'riladi. Ichki audit tizimi loyiha muvofiqligi va samaradorligini baholab boradi. Investitsiya loyihalari muntazam ravishda monitoring qilinadi.</p>
              <p><strong>Asosiy ko'rsatkichlar:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>KPI</th>
                      <th>Davriylik</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>ESG samaradorligi</td>
                      <td>yiliga 1 marta</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Uglerod (karbon) ta'siri</td>
                      <td>yiliga 1 marta</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Energiya tejalishi</td>
                      <td>yiliga 1 marta</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Ijtimoiy ta'sir</td>
                      <td>yiliga 1 marta</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Izoh. Natijalar yillik barqarorlik hisobotida e'lon qilinadi.</p>
              <p><strong>Barqaror investitsiyalar qo'mitasi</strong></p>
              <p>Investitsiya qarorlari quyidagi tarkibdagi qo'mita tomonidan ko'rib chiqiladi: rektor yoki prorektor, moliya bo'limi rahbari, barqaror rivojlanish bo'limi vakili, texnik ekspert va tashqi mustaqil ekspert.</p>
              <p><strong>Yakunlovchi qoida</strong></p>
              <p>Ushbu siyosat 2025 yildan kuchga kiradi va 2030 yilgacha amal qiladi. Zarur hollarda Reja-moliya bo'limi tomonidan qayta ko'rib chiqiladi va yangilanadi. Siyosat har 3 yilda qayta ko'rib chiqiladi yoki zarur hollarda yangilanadi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>SUSTAINABLE INVESTMENT POLICY (2025-2030)</strong></p>
              <p><strong>Prepared by:</strong> Planning and Finance Department<br><strong>Implementation period:</strong> 2025-2030<br><strong>Scope:</strong> All structural divisions, projects, and investment activities</p>
              <p>This policy aims to embed economic efficiency, environmental responsibility, and social sustainability principles into the institution's investment activities. It has been developed in accordance with the Law of the Republic of Uzbekistan on Investments and Investment Activity, international sustainable development principles, and green economy approaches.</p>
              <p><strong>PURPOSE AND OBJECTIVES</strong></p>
              <p>The policy seeks to optimize costs, reduce negative environmental impact, and create social value through sustainable investments. Its objectives include assessing medium- and long-term economic efficiency over 5-10 years, identifying potential economic risks and designing mitigation measures, making objective investment decisions, ensuring compliance with ESG (Environmental, Social, Governance) and sustainability principles, integrating ESG criteria into investment processes, reducing ecological impact, generating social value, managing financial risks, and reducing corruption risks while strengthening transparency.</p>
              <p>The policy applies to capital investments, infrastructure projects, public-private partnership initiatives, international grants, investments involving international financial institutions, and technology or energy modernization projects.</p>
              <p><strong>INVESTMENT PRINCIPLES</strong></p>
              <p>Investment activities are guided by ESG (Environmental, Social, Governance), SDG (Sustainable Development Goals), green economy principles, and national legal requirements. Innovation principles include the use of green technologies and digital solutions. Environmental principles include reduced carbon emissions, energy efficiency, and efficient use of water resources. Social principles include labor rights, health and safety, and inclusive development. Governance principles include transparency, anti-corruption policy, and accountability.</p>
              <p><strong>PROHIBITED INVESTMENTS</strong></p>
              <p>The University does not invest in coal-based energy projects, the tobacco industry, weapons manufacturing, projects causing serious environmental harm, or companies associated with human rights violations.</p>
              <p><strong>ESG evaluation system</strong></p>
              <p>Each investment project is assessed based on ESG criteria.</p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Criterion</th>
                      <th>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Environmental impact</td>
                      <td>30</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Energy efficiency</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Social impact</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Governance</td>
                      <td>20</td>
                    </tr>
                    <tr>
                      <td>5</td>
                      <td>Financial sustainability</td>
                      <td>10</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Minimum ESG score: 60. Projects scoring below 60 are not financed. Investment decision-making proceeds through the submission of a project proposal, financial analysis (NPV, IRR, ROI), ESG assessment, risk analysis, and review by the investment committee.</p>
              <p><strong>Project data collection</strong></p>
              <p>For each investment project, data are collected on project type, technology used, sector of activity, projected costs, revenues, financial flows, and debt or financing conditions. The project concept, objective, and implementation area are then defined. The project description explains the location, technology, and type of activity in detail. Legal analysis is carried out to assess compliance with national legislation and international standards.</p>
              <p>Environmental analysis evaluates impacts on air, water, soil, and biodiversity. Social analysis examines effects on public health, employment, migration processes, and social relations. During the impact assessment stage, both positive and negative effects are identified. Mitigation and compensation measures are developed to reduce negative impacts.</p>
              <p>A monitoring plan is prepared, defining responsible actors, control methods, timelines, and assessment indicators. The final stage involves project approval and recommendations for confirmation or improvement. Economic efficiency is assessed through NPV, IRR, ROI, and payback period indicators. Risk analysis covers environmental and social, financial, operational, legal, and political risks. Scenario analysis considers optimistic, pessimistic, and baseline cases. More advanced analysis may use Monte Carlo simulations and include waste and energy costs.</p>
              <p>Projects are integrated with ESG indicators. Financing sources may include the state budget, targeted funds, international financial institutions, green bonds, and private investment. Monitoring and reporting define annual KPIs, ESG reports, and corrective measures for detected shortcomings. Internal audit continuously evaluates compliance and effectiveness. Investment projects are monitored on a regular basis.</p>
              <p><strong>Key indicators:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>KPI</th>
                      <th>Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>ESG performance</td>
                      <td>once a year</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Carbon impact</td>
                      <td>once a year</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Energy savings</td>
                      <td>once a year</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Social impact</td>
                      <td>once a year</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Note: Results are disclosed in the annual sustainability report.</p>
              <p><strong>Sustainable investment committee</strong></p>
              <p>Investment decisions are reviewed by a committee composed of the rector or vice-rector, head of the finance department, a representative of the sustainable development unit, a technical expert, and an external independent expert.</p>
              <p><strong>Final provision</strong></p>
              <p>This policy enters into force in 2025 and remains valid until 2030. It may be reviewed and updated by the Planning and Finance Department whenever necessary. In all cases, the policy is reviewed every three years or updated as required.</p>
            </div>
        """,
    },
    "sdg-purchase": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Barqaror xaridlar siyosati (2025-2030)",
        "title_en": "Sustainable Procurement Policy (2025-2030)",
        "intro_uz": "Qarshi davlat universiteti xarid faoliyatida iqtisodiy samaradorlik, ekologik mas'uliyat va ijtimoiy barqarorlik tamoyillarini joriy etishga qaratilgan institutsional siyosat.",
        "intro_en": "Managing operational impact through sustainable procurement and supplier standards.",
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>BARQAROR XARIDLAR SIYOSATI (2025-2030)</strong></p>
              <p><strong>Ishlab chiquvchi:</strong> Reja-moliya bo'limi rahbari<br><strong>Amal qilish muddati:</strong> 2025-2030 yillar<br><strong>Qamrovi:</strong> Qarshi davlat universitetining barcha tuzilmaviy bo'linmalari</p>
              <p>Mazkur siyosat Qarshi davlat universiteti xarid faoliyatida iqtisodiy samaradorlik, ekologik mas'uliyat va ijtimoiy barqarorlik tamoyillarini joriy etishni maqsad qiladi. Siyosat davlat xaridlari to'g'risidagi qonunning 111-moddasi, davlat xaridlarini amalga oshirish bilan bog'liq tartib-taomillarni tashkil etish va o'tkazish tartibi to'g'risidagi nizom, "yashil iqtisodiyot", ESG tamoyillari, ISO 20400 Sustainable Procurement yondashuvi va Birlashgan Millatlar Tashkilotining barqaror rivojlanish maqsadlariga mos ravishda ishlab chiqilgan.</p>
              <p><strong>MAQSAD VA VAZIFA</strong></p>
              <p>Qarshi davlat universitetining xarid faoliyatida ekologik ta'sirni kamaytirish, energiya samarador mahsulotlar ulushini oshirish, ijtimoiy mas'ul yetkazib beruvchilar bilan ishlash, xarid jarayonlarida shaffoflikni ta'minlash va Life Cycle Cost - hayot sikli qiymati (LCC) yondashuvini joriy qilish ko'zda tutiladi.</p>
              <p>Barqaror xaridlar orqali xarajatlarni optimallashtirish, atrof-muhitga salbiy ta'sirni kamaytirish va ijtimoiy qiymat yaratish, ekologik toza va energiya tejamkor mahsulotlar ulushini oshirish, mahalliy ishlab chiqaruvchilar va ijtimoiy mas'ul yetkazib beruvchilarni qo'llab-quvvatlash, korrupsiya xavflarini kamaytirish hamda shaffoflikni ta'minlash maqsadida davlat xaridlari elektron tizimi orqali amalga oshiriladi.</p>
              <p>Siyosat quyidagi yo'nalishlarga tatbiq etiladi: kapital qo'yilmalar, infratuzilma loyihalari, davlat-xususiy sheriklik loyihalari, xalqaro va milliy grantlar, xalqaro moliya institutlari ishtirokidagi investitsiyalar, texnologik va energetik modernizatsiya loyihalari va xalqaro moliyalashtirish ishtirokidagi loyihalar.</p>
              <p>Ekologik tamoyillariga energiya samarador mahsulotlari, ekologik sertifikatlangan mahsulotlar, chiqindilarni kamaytirish, qayta ishlanadigan materiallardan foydalanish, karbon chiqindilarini kamaytirish va suv resurslaridan samarali foydalanish talablari kiradi. Ijtimoiy tamoyillarga mehnat huquqlariga rioya qilish va xavfsiz mehnat sharoitlarini ta'minlash kiradi. Boshqaruv tamoyillariga shaffof tender jarayonlari, korrupsiyaga qarshi mexanizmlar va hisobdorlik kiradi.</p>
              <p>Mazkur siyosat quyidagi xarid turlariga tatbiq etiladi: tovarlar xaridi, xizmatlar xaridi, qurilish va infratuzilma loyihalari, IT uskunalar, laboratoriya jihozlari va ofis materiallari.</p>
              <p>Xarid mezonlarida energiya samaradorligi va ekologik sertifikatlar (ISO, EcoLabel va h.k.), yashil texnologiyalar va raqamli yechimlardan foydalanganlik, qayta ishlanadigan yoki kam chiqindili materiallar, yetkazib beruvchining ESG ko'rsatkichlari muhim hisoblanadi.</p>
              <p><strong>Tender jarayonida quyidagi mezonlar qo'llaniladi:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Tender mezonlari</th>
                      <th>Tender ball</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Narx</td>
                      <td>50 ball</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Texnik sifat</td>
                      <td>20 ball</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>ESG ko'rsatkichlari</td>
                      <td>30 ball</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Yetkazib beruvchilar bilan ishlashda barqarorlik talablari kiritilgan shartnomalar, yetkazib beruvchilarni baholash va reytinglash, mahalliy va kichik biznesni rag'batlantirish hisobga olinadi. Supplier sustainability reyting tizimi joriy etiladi.</p>
              <p>Monitoring va hisobot jarayonlari yillik KPIlar va indikatorlar, ESG hisobotlari tayyorlash, hisobot kamchiliklari bo'yicha tuzatuv rejalari orqali amalga oshiriladi.</p>
              <p><strong>Barqaror xaridlar samaradorligi quyidagi ko'rsatkichlar orqali baholanadi:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Indikator</th>
                      <th>2030 yilgacha</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Sustainable procurement share</td>
                      <td>40%</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Eco-certified products</td>
                      <td>30%</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Supplier ESG compliance</td>
                      <td>70%</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Energy efficient equipment</td>
                      <td>50%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Izoh. Monitoring yiliga bir marta amalga oshiriladi.</p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Indikator</th>
                      <th>2030 yilgacha</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Karbon emissiyasi</td>
                      <td>-40% kamaytirish</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Qayta tiklanuvchi energiya ulushi</td>
                      <td>50%</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Suv iste'moli</td>
                      <td>-30% kamaytirish</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Chiqindilarni qayta ishlash</td>
                      <td>70%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Barqaror xaridlar siyosati orqali 2030 yilgacha ekologik barqarorlikka erishish maqsadlari monitoring natijalari orqali baholanadi.</p>
              <p><strong>Boshqaruv va mas'uliyat:</strong> Reja-moliya bo'limi siyosatni amalga oshiradi va monitoring olib boradi. Xaridlar komissiyasi mezonlar va tender jarayonlarini nazorat qiladi. Ichki audit muvofiqlik va samaradorlikni baholash tizimini yuritadi. Xatarlar va ularni boshqarishda moliyaviy va bozor xavflari, ta'minot zanjiridagi uzilishlar, regulyator o'zgarishlariga moslashuv tekshirilib boriladi.</p>
              <p><strong>Yakunlovchi qoidalar:</strong> Ushbu siyosat 2025 yildan kuchga kiradi va 2030 yilgacha amal qiladi. Zarur hollarda Reja-moliya bo'limi tomonidan qayta ko'rib chiqiladi va yangilanadi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>SUSTAINABLE PROCUREMENT POLICY (2025-2030)</strong></p>
              <p><strong>Prepared by:</strong> Head of the Planning and Finance Department<br><strong>Implementation period:</strong> 2025-2030<br><strong>Scope:</strong> All structural divisions of Karshi State University</p>
              <p>This policy aims to embed economic efficiency, environmental responsibility, and social sustainability principles into the procurement operations of Karshi State University. It has been developed in alignment with Article 111 of the Law on Public Procurement, the regulation governing public procurement procedures, the green economy agenda, ESG principles, the ISO 20400 Sustainable Procurement approach, and the United Nations Sustainable Development Goals.</p>
              <p><strong>PURPOSE AND OBJECTIVES</strong></p>
              <p>The policy is designed to reduce environmental impact in procurement, increase the share of energy-efficient products, work with socially responsible suppliers, ensure transparency in purchasing processes, and introduce a Life Cycle Cost (LCC) approach.</p>
              <p>Sustainable procurement is implemented through the public e-procurement system in order to optimize costs, reduce negative environmental impact, create social value, expand the share of eco-friendly and energy-efficient products, support local producers and socially responsible suppliers, reduce corruption risks, and improve transparency.</p>
              <p>The policy applies to the following areas: capital investments, infrastructure projects, public-private partnership projects, international and national grants, investments involving international financial institutions, technology and energy modernization projects, and projects supported by international financing.</p>
              <p>Environmental principles include requirements related to energy-efficient products, eco-certified products, waste reduction, the use of recyclable materials, lower carbon emissions, and efficient use of water resources. Social principles include respect for labor rights and the provision of safe working conditions. Governance principles include transparent tender procedures, anti-corruption mechanisms, and accountability.</p>
              <p>This policy applies to the following procurement categories: goods procurement, services procurement, construction and infrastructure projects, IT equipment, laboratory equipment, and office supplies.</p>
              <p>Procurement criteria place importance on energy efficiency, ecological certifications (ISO, EcoLabel, etc.), the use of green technologies and digital solutions, recyclable or low-waste materials, and the supplier's ESG performance indicators.</p>
              <p><strong>The following criteria are applied in the tender process:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Tender criteria</th>
                      <th>Tender score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Price</td>
                      <td>50 points</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Technical quality</td>
                      <td>20 points</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>ESG indicators</td>
                      <td>30 points</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Work with suppliers takes into account contracts containing sustainability requirements, supplier evaluation and ranking, and incentives for local and small businesses. A supplier sustainability rating system will be introduced.</p>
              <p>Monitoring and reporting will include annual KPIs and indicators, ESG reporting, and corrective action plans based on reporting gaps.</p>
              <p><strong>Sustainable procurement performance will be assessed through the following indicators:</strong></p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Indicator</th>
                      <th>By 2030</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Sustainable procurement share</td>
                      <td>40%</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Eco-certified products</td>
                      <td>30%</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Supplier ESG compliance</td>
                      <td>70%</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Energy efficient equipment</td>
                      <td>50%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Note: Monitoring is carried out once a year.</p>
              <div class="governance-table-wrap">
                <table class="governance-table">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Indicator</th>
                      <th>By 2030</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>Carbon emissions</td>
                      <td>Reduce by 40%</td>
                    </tr>
                    <tr>
                      <td>2</td>
                      <td>Renewable energy share</td>
                      <td>50%</td>
                    </tr>
                    <tr>
                      <td>3</td>
                      <td>Water consumption</td>
                      <td>Reduce by 30%</td>
                    </tr>
                    <tr>
                      <td>4</td>
                      <td>Waste recycling</td>
                      <td>70%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p>Through this policy, the University seeks to achieve key environmental sustainability targets by 2030.</p>
              <p><strong>Governance and responsibility:</strong> The Planning and Finance Department implements the policy and conducts monitoring. The Procurement Commission supervises the criteria and tender processes. Internal audit manages the compliance and effectiveness assessment system. Risks and risk management include financial and market risks, supply-chain disruptions, and adaptation to regulatory changes.</p>
              <p><strong>Final provisions:</strong> This policy enters into force in 2025 and remains valid until 2030. Where necessary, it will be reviewed and updated by the Planning and Finance Department.</p>
            </div>
        """,
        "sections_uz": [
            {
                "title": "Siyosat haqida",
                "paragraphs": [
                    "BARQAROR XARIDLAR SIYOSATI (2025-2030).",
                    "Ishlab chiquvchi: Reja-moliya bo'limi rahbari. Amal qilish muddati: 2025-2030 yillar. Qamrovi: Qarshi davlat universitetining barcha tuzilmaviy bo'linmalari.",
                    "Mazkur siyosat Qarshi davlat universiteti xarid faoliyatida iqtisodiy samaradorlik, ekologik mas'uliyat va ijtimoiy barqarorlik tamoyillarini joriy etishni maqsad qiladi.",
                    "Siyosat davlat xaridlari to'g'risidagi qonunning 111-moddasi, davlat xaridlarini amalga oshirish bilan bog'liq tartib-taomillarni tashkil etish va o'tkazish tartibi to'g'risidagi nizom, yashil iqtisodiyot, ESG tamoyillari, ISO 20400 Sustainable Procurement yondashuvi hamda BMTning barqaror rivojlanish maqsadlariga mos ravishda ishlab chiqilgan.",
                ],
            },
            {
                "title": "Maqsad va vazifalar",
                "paragraphs": [
                    "Qarshi davlat universitetining xarid faoliyatida ekologik ta'sirni kamaytirish, energiya samarador mahsulotlar ulushini oshirish, ijtimoiy mas'ul yetkazib beruvchilar bilan ishlash, xarid jarayonlarida shaffoflikni ta'minlash va Life Cycle Cost - hayot sikli qiymati (LCC) yondashuvini joriy qilish ushbu siyosatning asosiy vazifasi hisoblanadi.",
                    "Barqaror xaridlar orqali xarajatlarni optimallashtirish, atrof-muhitga salbiy ta'sirni kamaytirish va ijtimoiy qiymat yaratish, ekologik toza va energiya tejamkor mahsulotlar ulushini oshirish, mahalliy ishlab chiqaruvchilar hamda ijtimoiy mas'ul yetkazib beruvchilarni qo'llab-quvvatlash, korrupsiya xavflarini kamaytirish va shaffoflikni ta'minlash maqsadida davlat xaridlari elektron tizimi orqali amalga oshiriladi.",
                ],
            },
            {
                "title": "Tatbiq etiladigan yo'nalishlar",
                "paragraphs": [
                    "Siyosat quyidagi yo'nalishlarga tatbiq etiladi:",
                ],
                "bullets": [
                    "kapital qo'yilmalar",
                    "infratuzilma loyihalari",
                    "davlat-xususiy sheriklik loyihalari",
                    "xalqaro va milliy grantlar",
                    "xalqaro moliya institutlari ishtirokidagi investitsiyalar",
                    "texnologik va energetik modernizatsiya loyihalari",
                    "xalqaro moliyalashtirish ishtirokidagi loyihalar",
                ],
            },
            {
                "title": "Tamoyillar va xarid turlari",
                "paragraphs": [
                    "Ekologik tamoyillariga energiya samarador mahsulotlari, ekologik sertifikatlangan mahsulotlar, chiqindilarni kamaytirish, qayta ishlanadigan materiallardan foydalanish, karbon chiqindilarini kamaytirish va suv resurslaridan samarali foydalanish talablari kiradi.",
                    "Ijtimoiy tamoyillarga mehnat huquqlariga rioya qilish va xavfsiz mehnat sharoitlarini ta'minlash kiradi.",
                    "Boshqaruv tamoyillariga shaffof tender jarayonlari, korrupsiyaga qarshi mexanizmlar va hisobdorlik kiradi.",
                    "Mazkur siyosat quyidagi xarid turlariga tatbiq etiladi: tovarlar xaridi, xizmatlar xaridi, qurilish va infratuzilma loyihalari, IT uskunalar, laboratoriya jihozlari va ofis materiallari.",
                ],
            },
            {
                "title": "Xarid mezonlari va tender baholash",
                "paragraphs": [
                    "Xarid mezonlarida energiya samaradorligi va ekologik sertifikatlar (ISO, EcoLabel va h.k.), yashil texnologiyalar va raqamli yechimlardan foydalanganlik, qayta ishlanadigan yoki kam chiqindili materiallar yetkazib beruvchining ESG ko'rsatkichlari muhim hisoblanadi.",
                    "Tender jarayonida quyidagi mezonlar qo'llaniladi:",
                ],
                "tables": [
                    {
                        "headers": ["РІвЂћвЂ“", "Tender mezonlari", "Tender ball"],
                        "rows": [
                            ["1", "Narx", "50 ball"],
                            ["2", "Texnik sifat", "20 ball"],
                            ["3", "ESG ko'rsatkichlari", "30 ball"],
                        ],
                    }
                ],
            },
            {
                "title": "Yetkazib beruvchilar, monitoring va KPI",
                "paragraphs": [
                    "Yetkazib beruvchilar bilan ishlashda barqarorlik talablari kiritilgan shartnomalar, yetkazib beruvchilarni baholash va reytinglash, mahalliy va kichik biznesni rag'batlantirish hisobga olinadi. Supplier sustainability reyting tizimi joriy etiladi.",
                    "Monitoring va hisobot jarayonlarida yillik KPIlar va indikatorlar, ESG hisobotlari tayyorlash, hisobot kamchiliklari bo'yicha tuzatuv rejalari amalga oshiriladi.",
                    "Barqaror xaridlar samaradorligi quyidagi ko'rsatkichlar orqali baholanadi:",
                ],
                "tables": [
                    {
                        "headers": ["РІвЂћвЂ“", "Indikator", "2030 yilgacha"],
                        "rows": [
                            ["1", "Sustainable procurement share", "40%"],
                            ["2", "Eco-certified products", "30%"],
                            ["3", "Supplier ESG compliance", "70%"],
                            ["4", "Energy efficient equipment", "50%"],
                        ],
                    }
                ],
            },
            {
                "title": "2030 yilgacha ekologik natijalar",
                "paragraphs": [
                    "Izoh. Monitoring yiliga bir marta amalga oshiriladi.",
                    "Barqaror xaridlar siyosati orqali 2030 yilgacha ekologik barqarorlikka erishish maqsadlari quyidagi ko'rsatkichlar orqali baholanadi:",
                ],
                "tables": [
                    {
                        "headers": ["РІвЂћвЂ“", "Indikator", "2030 yilgacha"],
                        "rows": [
                            ["1", "Karbon emissiyasi", "РІв‚¬вЂ™40% kamaytirish"],
                            ["2", "Qayta tiklanuvchi energiya ulushi", "50%"],
                            ["3", "Suv iste'moli", "РІв‚¬вЂ™30% kamaytirish"],
                            ["4", "Chiqindilarni qayta ishlash", "70%"],
                        ],
                    }
                ],
            },
            {
                "title": "Boshqaruv va mas'uliyat",
                "paragraphs": [
                    "Reja-moliya bo'limi siyosatni amalga oshiradi va monitoring olib boradi. Xaridlar komissiyasi mezonlar va tender jarayonlarini nazorat qiladi. Ichki audit muvofiqlik va samaradorlikni baholash tizimini yuritadi.",
                    "Xatarlar va ularni boshqarishda moliyaviy va bozor xavflari, ta'minot zanjiridagi uzilishlar va regulyator o'zgarishlariga moslashuv muntazam tekshirilib boriladi.",
                ],
            },
            {
                "title": "Yakunlovchi qoidalar",
                "paragraphs": [
                    "Ushbu siyosat 2025 yildan kuchga kiradi va 2030 yilgacha amal qiladi.",
                    "Zarur hollarda Reja-moliya bo'limi tomonidan qayta ko'rib chiqiladi va yangilanadi.",
                ],
            },
        ],
        "sections_en": [
            {
                "title": "Procurement approach",
                "paragraphs": [
                    "Procurement decisions evaluate ESG performance alongside price and technical quality.",
                    "Priority is given to eco-certified products, energy-efficient equipment, and responsible suppliers.",
                ],
            },
            {
                "title": "2030 outcomes",
                "bullets": [
                    "increase the share of sustainable procurement",
                    "expand procurement of eco-certified products",
                    "raise supplier ESG compliance levels",
                    "grow the share of energy-efficient campus equipment",
                ],
            },
        ],
    },
    "sdg-committee": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Barqarorlik qo'mitasi",
        "title_en": "Sustainability Committee",
        "intro_uz": "Universitetda barqaror rivojlanish faoliyatlarini muvofiqlashtiruvchi, monitoring qiluvchi va kuchaytiruvchi markaziy boshqaruv organi.",
        "intro_en": "The University's central governance body for coordinating, monitoring, and strengthening sustainable development activities.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>Barqarorlik qo'mitasi</strong></p>
              <p>2025-yil 3-aprel kuni Qarshi davlat universitetida Universitet Kengashi qaroriga muvofiq Barqarorlik qo'mitasi rasmiy ravishda tashkil etildi. Ushbu qo'mita universitetda barqaror rivojlanish yo'nalishidagi faoliyatlarni muvofiqlashtirish va kuchaytirish uchun markaziy organ sifatida faoliyat yuritadi.</p>
              <p>Qo'mita universitetning ta'lim, ilmiy-tadqiqot va operatsion faoliyatlarida barqarorlik tashabbuslarini rivojlantirish, strategiyalar ishlab chiqish va amalga oshirishni nazorat qiladi. Shuningdek, ekologik mas'uliyatli amaliyotlarni targ'ib qiladi hamda barqarorlik tamoyillarini ta'lim, ilmiy izlanishlar, kampus boshqaruvi va jamoatchilik bilan hamkorlik faoliyatlariga integratsiya qilishni qo'llab-quvvatlaydi.</p>
              <p>Bundan tashqari, qo'mita akademik bo'limlar, ilmiy laboratoriyalar va ma'muriy tuzilmalar o'rtasida hamkorlikni ta'minlab, barqarorlik tashabbuslarini samarali amalga oshirishga xizmat qiladi.</p>
              <p>Ushbu faoliyatlarni muvofiqlashtirish va qo'llab-quvvatlash uchun maxsus xodimlar tayinlangan. Farrux Aminov Barqarorlik qo'mitasining ijrochi kotibi sifatida faoliyat yuritib, barqarorlik strategiyalarini muvofiqlashtirish va universitetdagi barqarorlik tashabbuslarini monitoring qilish uchun mas'ul hisoblanadi. Firuza Davronova esa qo'mita ijrochi kotibi o'rinbosari sifatida barqarorlik dasturlarini amalga oshirishda ko'maklashadi hamda universitet bo'limlari va ilmiy markazlar o'rtasidagi hamkorlikni ta'minlaydi.</p>
              <p>Mazkur boshqaruv tuzilmasi orqali universitet barqaror rivojlanishni ilgari surishda yetakchilik, javobgarlik va uzluksiz rivojlanishni ta'minlaydi.</p>
              <p><strong>Qarshi davlat universitetida "yashil" madaniyatni targ'ib qilishga mas'ul Barqarorlik qo'mitasi a'zolari:</strong></p>
              <ol>
                <li>Dilmurod Xamidullayevich Nabiyev - Qo'mita raisi (Rektor)</li>
                <li>Ilhom Rustamovich Bekpulatov - Ijrochi direktor (ilmiy ishlar va innovatsiyalar bo'yicha prorektor)</li>
                <li>Abdulxamid Erkinovich Xolmurodov - Ijrochi direktor (o'quv ishlari bo'yicha prorektor)</li>
                <li>Oybek Chuliyevich Kuziyev - Ijrochi direktor (yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor)</li>
                <li>Xurshid G'aybullayevich Jurayev - Ijrochi direktor (moliya-iqtisod ishlari bo'yicha prorektor)</li>
                <li>Farrux Aminov - Ijrochi kotib</li>
                <li>Firuza Davronova - Ijrochi kotib o'rinbosari</li>
                <li>Xalqaro bo'lim boshlig'i - xalqaro hamkorlik doirasida barqarorlik faoliyatlarini tashkil etish va hisobot tayyorlash uchun mas'ul</li>
                <li>Kasaba uyushmasi raisi - talabalar va xodimlar huquqlarini himoya qilish hamda statistik tahlillar uchun mas'ul</li>
                <li>Ma'naviy-ma'rifiy ishlar bo'limi boshlig'i - targ'ibot va tahliliy faoliyatlar uchun mas'ul</li>
                <li>Reja-moliya bo'limi boshlig'i - moliyaviy choralarni amalga oshirish uchun mas'ul</li>
                <li>Kadrlar bo'limi boshlig'i - kadrlar siyosatini yuritish uchun mas'ul</li>
                <li>O'quv ishlari va registrator bo'limi boshlig'i - statistik tahlillar uchun mas'ul</li>
                <li>Xotin-qizlar masalalari va psixologik maslahat markazi rahbari - tegishli faoliyatlar uchun mas'ul</li>
                <li>Korrupsiyaga qarshi kurash bo'limi boshlig'i - tegishli choralarni amalga oshirish uchun mas'ul</li>
                <li>Talabalar yetakchisi - talabalar ishtirokidagi faoliyatlarni tashkil etish uchun mas'ul</li>
                <li>Axborot xizmati boshlig'i - sayt, ijtimoiy tarmoqlar va hisobotlar uchun mas'ul</li>
                <li>Xalqaro nashrlar bo'yicha mutaxassis - ilmiy maqolalarni rag'batlantirish uchun mas'ul</li>
                <li>Inkubatsiya markazi rahbari - ta'limiy faoliyatlarni tashkil etish uchun mas'ul</li>
                <li>Geografiya va agronomiya fakulteti dekani - ta'limiy faoliyatlar uchun mas'ul</li>
                <li>Kimyo va biologiya fakulteti dekani - ta'limiy faoliyatlar uchun mas'ul</li>
                <li>Tibbiyot fakulteti dekani - ta'limiy faoliyatlar uchun mas'ul</li>
                <li>Sanoat muhandisligi kafedrasi mudiri - ta'limiy faoliyatlar uchun mas'ul</li>
                <li>Psixologiya kafedrasi mudiri - psixologik qo'llab-quvvatlash va tahlillar uchun mas'ul</li>
              </ol>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>Sustainability Committee</strong></p>
              <p>On April 3, 2025, Karshi State University formally established a Sustainability Committee in accordance with a decision of the University Committee to coordinate and strengthen institutional efforts related to sustainable development. The committee serves as the central body responsible for advancing sustainability initiatives across academic, research, and operational activities of the university.</p>
              <p>The committee oversees the development and implementation of sustainability strategies, promotes environmentally responsible practices, and supports the integration of sustainability principles into teaching, research, campus operations, and community engagement activities. It also facilitates cooperation between academic departments, research laboratories, and administrative units to ensure the effective implementation of sustainability initiatives.</p>
              <p>Dedicated staff members have been appointed to coordinate and support these activities. Farrukh Aminov serves as the Executive Secretary of the Sustainability Committee and is responsible for coordinating sustainability strategies and monitoring institutional sustainability initiatives. Firuza Davronova serves as the Deputy Executive Secretary of the Sustainability Committee and supports the implementation of sustainability programs while facilitating collaboration among university departments and research centers.</p>
              <p>Through this governance structure, the university ensures institutional leadership, accountability, and continuous progress in advancing sustainable development across the campus community.</p>
              <p><strong>Members of the sustainability committee responsible for promoting a "green" culture at Karshi State University:</strong></p>
              <ol>
                <li>Dilmurod Khamidullayevich Nabiyev - Chair of the committee (Rector of Karshi State University)</li>
                <li>Ilhom Rustamovich Bekpulatov - Executive director of the committee (Vice-Rector for Research and innovation)</li>
                <li>Abdulxamid Erkinovich Xolmurodov - Executive director of the committee (Vice-Rector for Academic affairs)</li>
                <li>Oybek Chuliyevich Kuziyev - Executive director of the committee (First Vice-Rector for Youth affairs and spiritual-educational work)</li>
                <li>Xurshid G'aybullayevich Djurayev - Executive director of the committee (Vice-Rector for Finance and economic affairs)</li>
                <li>Farrukh Aminov - Executive secretary of the committee (specialist of the International rankings department)</li>
                <li>Firuza Davronova - Deputy executive secretary of the committee (International rankings department staff member)</li>
                <li>Head of the International department - responsible for organizing sustainability-related activities within the framework of international cooperation and preparing relevant reports.</li>
                <li>Head of the Trade union - responsible for implementing measures aimed at protecting the rights of students and staff, conducting statistical analyses, and preparing relevant reports.</li>
                <li>Head of the department for Spiritual and educational work - responsible for organizing educational and awareness activities related to sustainability and preparing analytical reports.</li>
                <li>Head of the Planning and finance department - responsible for implementing financial measures related to sustainability and preparing analytical reports.</li>
                <li>Head of the Human resources department - responsible for implementing personnel policies related to sustainability and preparing analytical reports.</li>
                <li>Head of the Academic affairs and registrar office - responsible for conducting statistical analyses related to sustainability and preparing relevant reports.</li>
                <li>Head of the Women's affairs and psychological counseling center - responsible for organizing activities related to women's rights and sustainability and preparing analytical reports.</li>
                <li>Head of the Anti-corruption department - responsible for implementing anti-corruption activities related to sustainability and preparing analytical reports.</li>
                <li>Student leader - responsible for organizing sustainability activities involving students and preparing analytical reports.</li>
                <li>Head of the Information service department - responsible for managing the university's sustainability website, social media activities, and reporting on the Sustainable development goals.</li>
                <li>Specialist for International publications - responsible for encouraging faculty members to publish scientific articles related to sustainability.</li>
                <li>Head of the Incubation center - responsible for organizing educational activities related to sustainability and preparing relevant reports.</li>
                <li>Dean of the faculty of Geography and agronomy - responsible for implementing educational activities related to sustainability and preparing relevant reports.</li>
                <li>Dean of the faculty of Chemistry and biology - responsible for implementing educational activities related to sustainability and preparing relevant reports.</li>
                <li>Dean of the faculty of Medicine - responsible for implementing educational activities related to sustainability and preparing relevant reports.</li>
                <li>Head of the department of Industrial engineering - responsible for implementing sustainability-related educational activities and preparing reports.</li>
                <li>Head of the department of Psychology - responsible for organizing psychological support activities related to sustainability, conducting statistical analyses, and preparing reports.</li>
              </ol>
            </div>
        """,
    },
    "anti-corruption": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Korrupsiyaga qarshi siyosat",
        "title_en": "Anti-Corruption Policy",
        "intro_uz": "Universitetda halollik, shaffoflik va hisobdorlikni mustahkamlashga qaratilgan institutsional korrupsiyaga qarshi siyosat va komplayens nazorat tizimi.",
        "intro_en": "The University's institutional anti-corruption policy and compliance control framework designed to strengthen integrity, transparency, and accountability.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>QARSHI DAVLAT UNIVERSITETIDA KORRUPSIYAGA QARSHI SIYOSAT</strong></p>
              <p>O'zbekiston Respublikasi Prezidentining 2020-yil 27-maydagi PF-5927-sonli "O'zbekiston Respublikasida korrupsiyaga qarshi kurashish tizimini yanada takomillashtirish chora-tadbirlari to'g'risida"gi Farmoni, O'zbekiston Respublikasi Prezidenti Administratsiyasi rahbarining 2020-yil 4-sentabrdagi 22-2488-sonli topshirig'i, shuningdek, Oliy va o'rta maxsus ta'lim vazirligining 2020-2021-yillarga mo'ljallangan "yo'l xaritasi"da belgilangan yashirin iqtisodiyotga qarshi kurashish va korrupsiyaning oldini olishga qaratilgan vazifalar hamda 2021-yil 28-iyundagi 281-sonli "Oliy ta'lim tizimida 'Korrupsiyasiz soha' loyihasini amalga oshirishni tashkil etish to'g'risida"gi buyrug'iga muvofiq, Qarshi davlat universitetida 2021-yil 5-iyul kuni rektor buyrug'i bilan Korrupsiyaga qarshi kurashish bo'yicha komplayens nazorat bo'limi tashkil etildi.</p>
              <p>Universitet barcha akademik va ma'muriy faoliyatlarda shaffoflik, hisobdorlik va halollikni ta'minlashga qaratilgan kompleks korrupsiyaga qarshi siyosat tizimi hamda institutsional boshqaruv mexanizmlari orqali yaxlit etik tashkiliy madaniyatni rivojlantiradi. Ushbu siyosat oliy ta'lim tizimida korrupsiyaga qarshi kurashish amaliyotlarini mustahkamlashga qaratilgan milliy qonunchilik va davlat tashabbuslari asosida amalga oshiriladi.</p>
              <p>Mazkur choralarni amalga oshirish maqsadida universitetda rektor nazorati ostida faoliyat yurituvchi va muassasa bo'ylab korrupsiyaga qarshi tashabbuslarni muvofiqlashtiruvchi maxsus Korrupsiyaga qarshi komplayens nazorat bo'limi tashkil etilgan. Bo'lim korrupsiyaga qarshi qonunchilik va ichki me'yoriy hujjatlarga rioya etilishini nazorat qiladi, korrupsiya xavfi yuqori bo'lgan sohalarni aniqlaydi hamda tizimli xavflarni kamaytirish va korrupsion holatlarning ildiz sabablarini bartaraf etishga qaratilgan profilaktik strategiyalarni ishlab chiqadi.</p>
              <p>Amaliy jihatdan bo'lim qonunchilik va ichki tartib-qoidalarga rioya etilishini monitoring qiladi, profilaktik chora-tadbirlar rejalarini ishlab chiqadi va amalga oshiradi, shuningdek, universitetda "Korrupsiyasiz soha" loyihasi kabi milliy tashabbuslarni joriy etishda ishtirok etadi. Bo'lim korrupsiyaga qarshi siyosatga oid ichki me'yoriy hujjatlarni tayyorlaydi, ichki jarayonlardagi kamchiliklarni aniqlaydi va shaffoflik hamda hisobdorlikni kuchaytirishga qaratilgan institutsional islohotlar bo'yicha takliflar kiritadi.</p>
              <p>Shuningdek, bo'lim korrupsiyaga oid murojaatlar va xabarlarni, jumladan anonim murojaatlarni ham ko'rib chiqadi hamda korrupsiya bilan bog'liq holatlar bo'yicha ichki tekshiruvlar reyestrini yuritadi. Xaridlar va ma'muriy jarayonlarda yuzaga kelishi mumkin bo'lgan manfaatlar to'qnashuvini tahlil qiladi va qaror qabul qilishda halollik hamda adolatlilikni ta'minlash bo'yicha tavsiyalar beradi.</p>
              <p>Bundan tashqari, universitetda professor-o'qituvchilar, ma'muriy xodimlar va talabalar o'rtasida etik qadriyatlarni targ'ib qilish maqsadida muntazam ravishda seminarlar, davra suhbatlari, konferensiyalar va targ'ibot tadbirlari tashkil etiladi. Korrupsiya xavflarini baholash va amalga oshirilayotgan chora-tadbirlar samaradorligini aniqlash uchun so'rovnomalar va tahliliy tadqiqotlar o'tkaziladi. Bo'lim davlat organlari, fuqarolik jamiyati institutlari va hamkor tashkilotlar bilan hamkorlik qilib, nazoratni kuchaytirish va shaffoflikni ta'minlashga xizmat qiladi.</p>
              <p>Uzluksiz monitoring, hisobot berish, targ'ibot ishlari va institutsional hamkorlik orqali universitet shaffof boshqaruv tizimini ta'minlaydi hamda halollik, hisobdorlik va mas'uliyatli institutsional madaniyatni rivojlantiruvchi etik akademik muhitni shakllantiradi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>ANTI-CORRUPTION POLICY AT KARSHI STATE UNIVERSITY</strong></p>
              <p>In accordance with Presidential Decree No. PF-5927 dated May 27, 2020, "On Measures to Further Improve the System of Combating Corruption in the Republic of Uzbekistan," and Instruction No. 22-2488 of the Head of the Presidential Administration of the Republic of Uzbekistan dated September 4, 2020, as well as the tasks outlined in the 2020-2021 "Roadmap" of the Ministry of Higher and Secondary Specialized Education aimed at combatting the shadow economy and preventing corruption, and Order No. 281, dated June 28, 2021, "On the Organization of the Implementation of the 'Corruption-Free Sphere' Project in the Higher Education System," the Compliance Control Department for Anti-Corruption Efforts was established at Karshi State University by Rector's Order on July 5, 2021.</p>
              <p>The university promotes a holistic ethical organizational culture through a comprehensive anti-corruption policy framework and institutional governance mechanisms aimed at ensuring transparency, accountability, and integrity in all academic and administrative activities. The policy is implemented in accordance with national legislation and government initiatives designed to strengthen anti-corruption practices in the higher education system. To implement these measures, the university has established a dedicated Compliance control department for anti-corruption efforts that operates under the supervision of the Rector and coordinates anti-corruption initiatives across the institution. The department oversees compliance with anti-corruption laws and institutional regulations, identifies high-risk areas vulnerable to corruption, and develops preventive strategies to address systemic risks and eliminate the underlying causes of corrupt practices.</p>
              <p>Operationally, the department monitors compliance with legal and institutional regulations, develops and implements preventive action plans, and facilitates the implementation of national initiatives such as the "Corruption-Free Sphere" project within the university. It prepares internal regulatory documents related to anti-corruption policies, identifies weaknesses in internal procedures, and proposes institutional reforms to strengthen transparency and accountability.</p>
              <p>The department also considers complaints and reports related to corruption, including anonymous submissions, and maintains a registry of internal investigations concerning corruption-related incidents. It analyzes potential conflicts of interest in procurement and administrative processes and provides recommendations to ensure integrity and fairness in decision-making.</p>
              <p>In addition, the university regularly organizes seminars, roundtables, conferences, and awareness campaigns to promote ethical values among academic staff, administrative personnel, and students. Surveys and analytical studies are conducted to assess corruption risks and evaluate the effectiveness of anti-corruption initiatives. The department cooperates with government institutions, civil society organizations, and partner institutions to strengthen oversight and promote transparency.</p>
              <p>Through continuous monitoring, reporting, awareness activities, and institutional coordination, the university maintains a transparent governance structure and fosters an ethical academic environment that supports integrity, accountability, and responsible institutional culture.</p>
            </div>
        """,
    },
    "jamoatchilik": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Jamoa shartnomasi",
        "title_en": "Collective Agreement",
        "intro_uz": "Universitet ma'muriyati hamda xodimlar va talabalar kasaba uyushmasi o'rtasidagi 2023-2025-yillar uchun mehnat, ijtimoiy-iqtisodiy va kasbiy munosabatlarni tartibga soluvchi hujjat.",
        "intro_en": "A regulatory document governing labor, socio-economic, and professional relations between the university administration and the trade union of staff and students for 2023-2025.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>QARSHI DAVLAT UNIVERSITETI MA'MURIYATI HAMDA UNIVERSITET XODIMLARI VA TALABALARI KASABA UYUSHMA QO'MITASI JAMOA SHARTNOMASI</strong></p>
              <p>Qarshi davlat universiteti ma'muriyati hamda universitet xodimlari va talabalari kasaba uyushma qo'mitasi o'rtasida 2023-2025-yillar uchun jamoa shartnomasi tuzilgan bo'lib, u universitetdagi mehnat, ijtimoiy-iqtisodiy va kasbiy munosabatlarni tartibga soluvchi muhim normativ hujjat hisoblanadi.</p>
              <p>Mazkur shartnoma O'zbekiston Respublikasi qonunchiligi, xususan Mehnat kodeksi va boshqa tegishli normativ hujjatlarga asoslangan holda ishlab chiqilgan. Uning asosiy maqsadi universitet xodimlari va talabalarning huquq va manfaatlarini himoya qilish, mehnat sharoitlarini yaxshilash hamda ijtimoiy hamkorlikni rivojlantirishdan iborat.</p>

              <p><strong>Shartnoma quyidagi asosiy yo'nalishlarni qamrab oladi:</strong></p>
              <ul>
                <li>mehnat shartnomalari va bandlik kafolatlari</li>
                <li>ish vaqti va dam olish tartibi</li>
                <li>mehnatga haq to'lash, kompensatsiya va rag'batlantirish tizimi</li>
                <li>mehnatni muhofaza qilish va xavfsizlik</li>
                <li>ijtimoiy himoya, sug'urta va imtiyozlar</li>
                <li>xodimlarning malakasini oshirish va kasbiy rivojlanishi</li>
                <li>jamoaviy hamkorlik va kasaba uyushmasi faoliyati</li>
              </ul>

              <p>Shuningdek, shartnoma universitetda ochiqlik, adolat va o'zaro hamkorlik tamoyillarini mustahkamlashga xizmat qiladi. Unda ish beruvchi, xodimlar va kasaba uyushmasining majburiyatlari aniq belgilangan bo'lib, tomonlar o'rtasida barqaror ijtimoiy muhitni ta'minlashga qaratilgan.</p>

              <p><strong>Tenglik, xilma-xillik va inklyuziya</strong></p>
              <p>Universitet barcha xodimlar va talabalar uchun teng imkoniyatlarni ta'minlash, adolatli va inklyuziv muhit yaratish majburiyatini o'z zimmasiga oladi. Universitet yosh, jins, gender identifikatsiyasi, jinsni o'zgartirish holati, nogironlik, millat, etnik kelib chiqish, din yoki e'tiqod, jinsiy orientatsiya, nikoh va fuqarolik holati, qochqinlik yoki boshpana izlovchi maqomi, homiladorlik va onalik kabi belgilarga ko'ra har qanday kamsitishni taqiqlaydi.</p>
              <p>Universitet o'z faoliyatining barcha yo'nalishlarida tenglik, xilma-xillik va inklyuziya tamoyillariga rioya etilishini ta'minlaydi.</p>

              <p><strong>Nogironligi bo'lgan xodimlar va talabalar uchun qo'llab-quvvatlash</strong></p>
              <p>Universitet nogironligi bo'lgan xodimlar va talabalar uchun teng imkoniyatlar yaratish maqsadida zarur shart-sharoitlar va yordam xizmatlarini taqdim etadi. Bunga binolarga erkin kirish uchun panduslar va liftlar, moslashtirilgan auditoriyalar, maxsus o'quv materiallari, assistent va tarjimon xizmatlari, shuningdek psixologik, akademik va ijtimoiy maslahat xizmatlari kiradi.</p>

              <p><strong>Kasaba uyushmasiga a'zolik huquqi</strong></p>
              <p>Universitet barcha xodimlarning kasaba uyushmalariga a'zo bo'lish huquqini tan oladi va hurmat qiladi. Ushbu huquq barcha toifadagi xodimlarga, jumladan ayollar, yosh mutaxassislar va xalqaro xodimlarga nisbatan teng ravishda tatbiq etiladi. Universitet kasaba uyushmalari bilan ijtimoiy hamkorlik va konstruktiv muloqot tamoyillariga amal qiladi.</p>

              <p><strong>Diskriminatsiya va majburiy mehnatga qarshi siyosat</strong></p>
              <p>Universitet ish joyida har qanday shakldagi diskriminatsiyani qat'iyan taqiqlaydi. Xodimlar va talabalar jins, yosh, din, millat, nogironlik, jinsiy orientatsiya yoki boshqa shaxsiy belgilari asosida kamsitilmasligi kerak. Diskriminatsiya holatlari aniqlangan taqdirda, ular amaldagi ichki tartib-qoidalar va qonunchilikka muvofiq ko'rib chiqiladi hamda tegishli choralar ko'riladi.</p>
              <p>Universitet majburiy mehnat, zamonaviy qullik, odam savdosi va bolalar mehnatining barcha shakllarini keskin rad etadi. Universitet o'z faoliyatida ushbu tamoyillarga qat'iy amal qiladi hamda hamkor tashkilotlar, pudratchilar va tashqi xizmat ko'rsatuvchilardan ham xuddi shunday yondashuvni talab qiladi.</p>

              <p><strong>Uchinchi tomonlar bilan hamkorlik</strong></p>
              <p>Universitet uchinchi tomon tashkilotlari bilan hamkorlik qilgan hollarda ham xodimlarning mehnat huquqlari himoya qilinishini kafolatlashga intiladi. Outsourcing asosida jalb etilgan xodimlar uchun adolatli ish sharoiti, munosib va teng ish haqi, mehnat xavfsizligi va ijtimoiy himoya tamoyillari ta'minlanishi lozim.</p>

              <p><strong>Teng haq to'lash va gender monitoringi</strong></p>
              <p>Universitet erkaklar va ayollar uchun teng qiymatdagi mehnatga teng haq to'lash tamoyiliga amal qiladi. Ish haqi tizimida gender asosidagi tafovutlarning oldini olish, ularni aniqlash va bartaraf etish universitetning ustuvor yo'nalishlaridan biri hisoblanadi.</p>
              <p>Universitet xodimlar ish haqi bo'yicha muntazam statistik tahlil o'tkazadi hamda gender tengligi darajasini monitoring qiladi. Aniqlangan tafovutlarni bartaraf etish yuzasidan tegishli boshqaruv, tashkiliy va amaliy choralar ko'riladi.</p>

              <p><strong>Murojaat va shikoyatlar tartibi</strong></p>
              <p>Universitet xodimlari o'z mehnat huquqlari, ish haqi, mehnat sharoitlari yoki boshqa mehnatga oid masalalar yuzasidan rasmiy tarzda murojaat qilish va shikoyat berish huquqiga ega. Universitetda bunday murojaatlarni ko'rib chiqishning aniq, shaffof, adolatli va maxfiy tartibi joriy etiladi.</p>

              <p><strong>Asosiy mehnat huquqlari</strong></p>
              <p>Universitet barcha xodimlarning asosiy mehnat huquqlarini tan oladi va hurmat qiladi. Bunga kasaba uyushmalariga birlashish erkinligi, kollektiv muzokaralar olib borish huquqi, xavfsiz mehnat sharoiti va adolatli mehnat munosabatlari kiradi.</p>

              <p><strong>Diskriminatsiyadan holi muhit</strong></p>
              <p>Universitet xodimlar va talabalar uchun diskriminatsiyadan holi, xavfsiz va hurmatga asoslangan muhit yaratishni o'zining muhim vazifalaridan biri deb biladi. Universitet millat, jins, din, yosh, nogironlik yoki boshqa shaxsiy belgilar asosida kamsitishni taqiqlaydi va bunday holatlarning oldini olish choralarini ko'radi.</p>
              <p>Universitetda tenglik, xilma-xillik va inklyuziya masalalari bilan shug'ullanuvchi maxsus komissiya yoki mas'ul bo'linma faoliyat yuritadi. Ushbu tuzilma tegishli siyosatlarni ishlab chiqish, amalga oshirilishini monitoring qilish, xodimlar va talabalar o'rtasida tushuntirish ishlari hamda treninglar tashkil etish bilan shug'ullanadi.</p>

              <p><strong>Homiladorlik va onalikni qo'llab-quvvatlash</strong></p>
              <p>Universitet homiladorlik va onalik davrida ayollarni qo'llab-quvvatlash siyosatini amalga oshiradi. Bunga homiladorlik ta'tili, bola parvarishi ta'tili, ish joyini saqlab qolish kafolatlari va zarur hollarda moslashtirilgan mehnat sharoitlari kiradi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>COLLECTIVE AGREEMENT BETWEEN THE ADMINISTRATION OF KARSHI STATE UNIVERSITY AND THE TRADE UNION COMMITTEE OF UNIVERSITY STAFF AND STUDENTS</strong></p>
              <p>A collective agreement for the period 2023-2025 has been concluded between the administration of Karshi State University and the trade union committee representing the university's staff and students. This agreement serves as an important regulatory document governing labor, socio-economic, and professional relations within the university.</p>
              <p>The agreement has been developed in accordance with the legislation of the Republic of Uzbekistan, particularly the Labor Code and other relevant legal acts. Its main objective is to protect the rights and interests of university staff and students, improve working conditions, and promote social partnership.</p>

              <p><strong>The agreement covers the following key areas:</strong></p>
              <ul>
                <li>employment contracts and job security guarantees</li>
                <li>working hours and rest periods</li>
                <li>remuneration, compensation, and incentive systems</li>
                <li>occupational safety and labor protection</li>
                <li>social protection, insurance, and benefits</li>
                <li>professional development and capacity building of employees</li>
                <li>collective cooperation and trade union activities</li>
              </ul>

              <p>In addition, the agreement contributes to strengthening the principles of transparency, fairness, and mutual cooperation within the university. It clearly defines the responsibilities of the employer, employees, and the trade union, aiming to ensure a stable and supportive social environment.</p>

              <p><strong>Equality, diversity, and inclusion</strong></p>
              <p>The University is committed to ensuring equal opportunities and fostering a fair, inclusive, and respectful environment for all employees and students. Discrimination based on age, sex, gender identity, gender reassignment, disability, nationality or ethnic origin, religion or belief, sexual orientation, marital or civil status, refugee or asylum seeker status, pregnancy and maternity is strictly prohibited.</p>
              <p>The University shall ensure that equality, diversity, and inclusion principles are upheld across all areas of its activities.</p>

              <p><strong>Support for employees and students with disabilities</strong></p>
              <p>The University shall provide necessary support services and accessible conditions to ensure equal opportunities for employees and students with disabilities. These include, but are not limited to, accessible infrastructure (ramps and elevators), adapted classrooms, specialized learning materials, assistant and interpreter services, as well as psychological, academic, and social support.</p>

              <p><strong>Right to join trade unions</strong></p>
              <p>The University recognizes and respects the right of all employees to join trade unions. This right shall apply equally to all categories of staff, including women, early-career professionals, and international employees. The University shall maintain constructive engagement and social dialogue with trade unions.</p>

              <p><strong>Discrimination-free and safe workplace</strong></p>
              <p>The University strictly prohibits all forms of discrimination in the workplace. Employees and students shall not be subjected to discrimination based on sex, age, religion, nationality, disability, sexual orientation, or any other personal characteristic. Any cases of discrimination shall be addressed in accordance with internal regulations and applicable laws.</p>
              <p>The University firmly rejects all forms of forced labour, modern slavery, human trafficking, and child labour. The University shall adhere to these principles in its operations and require the same standards from its partners, contractors, and service providers.</p>

              <p><strong>Third-party relations</strong></p>
              <p>The University shall ensure that employees' labour rights are protected when engaging with third-party organizations. Workers involved through outsourcing arrangements shall be guaranteed fair working conditions, equitable remuneration, occupational safety, and social protection.</p>

              <p><strong>Equal pay and gender monitoring</strong></p>
              <p>The University shall adhere to the principle of equal pay for work of equal value, regardless of gender. Preventing, identifying, and eliminating gender-based pay disparities shall be a key institutional priority.</p>
              <p>The University shall conduct regular statistical analyses of employee remuneration to monitor gender pay equality. Where disparities are identified, appropriate corrective measures shall be implemented.</p>

              <p><strong>Grievance and complaint procedure</strong></p>
              <p>Employees shall have the right to submit formal complaints regarding labour rights, remuneration, working conditions, or other employment-related matters. The University shall maintain a transparent, fair, and confidential grievance mechanism.</p>

              <p><strong>Fundamental labour rights</strong></p>
              <p>The University recognizes and respects fundamental labour rights, including freedom of association, the right to collective bargaining, safe working conditions, and fair labour practices.</p>

              <p><strong>Equality, diversity, and inclusion structure</strong></p>
              <p>The University shall ensure a safe, respectful, and discrimination-free environment for all employees and students. Discrimination based on nationality, gender, religion, age, disability, or any other personal characteristic is strictly prohibited.</p>
              <p>The University shall establish a dedicated committee or unit responsible for equality, diversity, and inclusion. This body shall develop policies, monitor implementation, conduct awareness activities, and organize training programs.</p>

              <p><strong>Support during pregnancy and maternity</strong></p>
              <p>The University shall implement policies to support women during pregnancy and maternity. This includes maternity leave, childcare leave, job protection guarantees, and, where necessary, flexible or adapted working conditions.</p>
            </div>
        """,
    },
    "xotin-qizlar": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Xotin-qizlar",
        "title_en": "Women and Inclusion",
        "intro_uz": "Ta'lim, bandlik, yetakchilik va qaror qabul qilishdagi ishtirokni kuchaytirishga qaratilgan inklyuziv siyosat.",
        "intro_en": "An inclusive policy designed to strengthen participation in education, employment, leadership, and decision-making.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>QARSHI DAVLAT UNIVERSITETI<br>XOTIN-QIZLARNI QOРІР‚ВLLAB-QUVVATLASH VA GENDER TENGLIK SIYOSATI</strong></p>
              <p>Qarshi davlat universiteti xotin-qizlarning huquq va manfaatlarini himoya qilish, ularning taРІР‚в„ўlim, ilmiy faoliyat va ijtimoiy hayotdagi faol ishtirokini taРІР‚в„ўminlash hamda gender tenglik tamoyillarini mustahkamlashni oРІР‚Вzining ustuvor vazifalaridan biri sifatida belgilaydi. Mazkur siyosat OРІР‚Вzbekiston Respublikasi Oliy Majlis Senatining 2022-yil 28-dekabrdagi РІР‚Сљ2030-yilgacha OРІР‚Вzbekiston Respublikasida gender tenglikka erishish strategiyasining 2021РІР‚вЂњ2022-yillardagi ijrosi hamda uni amalga oshirish boРІР‚Вyicha 2023-yilga moРІР‚Вljallangan chora-tadbirlarni tasdiqlash toРІР‚ВgРІР‚ВrisidaРІР‚Сњgi SQ-682-IV-sonli qarori, OРІР‚Вzbekiston Respublikasi Oliy taРІР‚в„ўlim, fan va innovatsiyalar vazirligining 2023-yil 5-maydagi 126-sonli buyrugРІР‚Вi, shuningdek OРІР‚Вzbekiston Respublikasi Vazirlar Mahkamasining 2021-yil 6-oktabrdagi 625-sonli РІР‚СљZoРІР‚Вrlik ishlatishdan jabr koРІР‚Вrgan xotin-qizlarni reabilitatsiya qilish va moslashtirish hamda oРІР‚Вz joniga qasd qilishning oldini olish borasidagi ishlarni takomillashtirishga doir qoРІР‚Вshimcha chora-tadbirlar toРІР‚ВgРІР‚ВrisidaРІР‚Сњgi qarori asosida ishlab chiqilgan boРІР‚Вlib, universitetda xotin-qizlarga nisbatan har qanday diskriminatsiya, tazyiq va zoРІР‚Вravonlikka qarshi qatРІР‚в„ўiy nol darajadagi yondashuvni taРІР‚в„ўminlashga qaratilgan.</p>
              <p>Universitet hududida xotin-qizlar uchun teng imkoniyatlar yaratish nafaqat rasmiy siyosat va tartib-qoidalar orqali, balki kundalik taРІР‚в„ўlim jarayoni, ijtimoiy hayot va madaniy faoliyat orqali ham izchil amalga oshiriladi. Talaba-qizlar va ayol xodimlarning shaxsiy rivojlanishi, ilmiy salohiyatini oshirish, kasbiy kompetensiyalarini mustahkamlash hamda jamiyatda faol fuqarolik pozitsiyasini shakllantirish uchun zarur shart-sharoitlar yaratiladi. Shu bilan birga, universitetda sogРІР‚Вlom ijtimoiy-psixologik muhitni shakllantirish, oРІР‚Вzaro hurmat, tenglik va bagРІР‚Вrikenglik qadriyatlarini rivojlantirishga alohida eРІР‚в„ўtibor qaratiladi.</p>
              <p>Qarshi davlat universitetida xotin-qizlarga nisbatan zoРІР‚Вravonlik va tazyiqlarning oldini olish ustuvor yoРІР‚Вnalishlardan biri hisoblanadi. Shu maqsadda muntazam ravishda РІР‚СљZoРІР‚Вravonlik va tazyiqqa qarshimizРІР‚Сњ mavzusida davra suhbatlari, targРІР‚Вibot tadbirlari va maРІР‚в„ўrifiy uchrashuvlar tashkil etiladi. Ushbu jarayonlarda talabalar jinoyatchilikning oldini olish, huquqiy savodxonlikni oshirish, zoРІР‚Вravonlikning sabablari va oqibatlari haqida chuqur tushunchaga ega boРІР‚Вladilar, shuningdek bunday holatlarda qanday himoyalanish va qayerga murojaat qilish mumkinligi yuzasidan aniq tavsiyalar oladilar. Universitet psixologlari, inspektorlar va mutaxassislar ishtirokida oРІР‚Вtkaziladigan bunday tadbirlar xotin-qizlarda oРІР‚Вz huquqlarini anglash, ijtimoiy faollik va shaxsiy xavfsizlik madaniyatini shakllantirishga xizmat qiladi.</p>
              <p>Universitetda psixologik va ijtimoiy qoРІР‚Вllab-quvvatlash tizimi izchil yoРІР‚Вlga qoРІР‚Вyilgan boРІР‚Вlib, talaba-qizlar va ayol xodimlar uchun bepul maslahat xizmatlari taqdim etiladi. Psixologik xizmat markazi orqali stress, bosim, ijtimoiy muammolar yoki shaxsiy qiyinchiliklarga duch kelgan xotin-qizlarga individual yondashuv asosida yordam koРІР‚Вrsatiladi, bu esa ularning ruhiy barqarorligini mustahkamlash, taРІР‚в„ўlim va ish faoliyatida samaradorlikni oshirishga xizmat qiladi.</p>
              <p>Shuningdek, universitetda gender tenglik, oilaviy qadriyatlar va ijtimoiy masРІР‚в„ўuliyat masalalariga bagРІР‚Вishlangan taРІР‚в„ўlim va maРІР‚в„ўrifiy dasturlar muntazam amalga oshiriladi. Fakultetlar kesimida tashkil etiladigan seminarlar va uchrashuvlarda xotin-qizlarning jamiyatdagi oРІР‚Вrni, ularning ijtimoiy himoyasi, zamonaviy globallashuv sharoitida yuzaga kelayotgan muammolar va ularning yechimlari muhokama qilinadi. Bu jarayonlarda xotin-qizlar boРІР‚Вyicha maslahatchilar, psixologlar va mutaxassislar faol ishtirok etadi va talabalarga amaliy bilim hamda hayotiy koРІР‚Вnikmalar beriladi.</p>
              <p>Universitet xotin-qizlarning ijtimoiy faolligini oshirishga alohida eРІР‚в„ўtibor qaratadi. Turli tanlovlar, aksiyalar va madaniy tadbirlar, jumladan РІР‚СљZoРІР‚Вravonlikka qarshi 16 kunРІР‚Сњ kampaniyasi doirasidagi tashabbuslar xotin-qizlarning jamiyatdagi rolini mustahkamlash, ularning ijodiy va ijtimoiy salohiyatini namoyon etish uchun muhim platforma vazifasini bajaradi. Bunday tashabbuslar nafaqat xotin-qizlarni qoРІР‚Вllab-quvvatlashga, balki universitetda sogРІР‚Вlom, xavfsiz va inklyuziv muhitni shakllantirishga xizmat qiladi.</p>
              <p>Mazkur siyosat doirasida universitet har bir xotin-qiz uchun xavfsiz va himoyalangan muhitni kafolatlaydi. ZoРІР‚Вravonlik yoki tazyiq holatlari yuzaga kelgan taqdirda maxfiy murojaat qilish imkoniyati yaratilgan boРІР‚Вlib, har bir murojaat tezkor, xolis va adolatli tarzda koРІР‚Вrib chiqiladi, jabrlangan shaxslarni himoya qilish va ularga zarur yordam koРІР‚Вrsatish ustuvor vazifa sifatida qaraladi.</p>
              <p>Umuman olganda, Qarshi davlat universiteti xotin-qizlarni qoРІР‚Вllab-quvvatlash va gender tenglikni taРІР‚в„ўminlash orqali zamonaviy, inklyuziv va barqaror taРІР‚в„ўlim muhitini shakllantirishni maqsad qiladi. Ushbu siyosat universitet jamoasining barcha aРІР‚в„ўzolari uchun teng imkoniyatlar yaratish, inson qadr-qimmatini hurmat qilish va ijtimoiy adolatni taРІР‚в„ўminlashga xizmat qiladi hamda milliy va xalqaro barqaror rivojlanish maqsadlariga mos ravishda doimiy takomillashtirib boriladi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>KARSHI STATE UNIVERSITY<br>WOMENРІР‚в„ўS SUPPORT AND GENDER EQUALITY POLICY</strong></p>
              <p>Karshi State University recognizes the protection of womenРІР‚в„ўs rights and interests, the promotion of their active participation in education, research, and social life, and the strengthening of gender equality principles as one of its key institutional priorities. This policy has been developed in accordance with the Resolution of the Senate of the Republic of Uzbekistan dated December 28, 2022 (No. SQ-682-IV) on the implementation of the Gender Equality Strategy of the Republic of Uzbekistan until 2030, the Order of the Ministry of Higher Education, Science and Innovation dated May 5, 2023 (No. 126), as well as the Resolution of the Cabinet of Ministers dated October 6, 2021 (No. 625) on additional measures to improve the rehabilitation and adaptation of women affected by violence and the prevention of suicide. The policy is aimed at ensuring a strict zero-tolerance approach to any form of discrimination, harassment, or violence against women within the university.</p>
              <p>Within the university environment, equal opportunities for women are ensured not only through formal policies and regulations but also through the consistent integration of these principles into academic processes, social life, and cultural activities. Necessary conditions are created to support the personal development of female students and women staff, enhance their academic and professional competencies, and foster an active civic position in society. At the same time, particular attention is given to building a healthy socio-psychological environment based on mutual respect, equality, and tolerance.</p>
              <p>Preventing violence and harassment against women is one of the universityРІР‚в„ўs priority areas. For this purpose, regular roundtable discussions, awareness campaigns, and educational meetings are organized under themes such as РІР‚СљWe are against violence and harassment.РІР‚Сњ During these activities, students are provided with comprehensive knowledge on crime prevention, legal awareness, the causes and consequences of violence, as well as practical guidance on protection mechanisms and reporting procedures. Events conducted with the participation of university psychologists, inspectors, and specialists contribute to raising awareness among women about their rights, strengthening social engagement, and developing a culture of personal safety.</p>
              <p>The university has established a consistent system of psychological and social support, providing free counseling services to female students and women staff. Through the psychological service center, individualized support is offered to those experiencing stress, pressure, social challenges, or personal difficulties. This contributes to strengthening their emotional well-being and improving their academic and professional performance.</p>
              <p>In addition, the university regularly implements educational and awareness programs focused on gender equality, family values, and social responsibility. Seminars and meetings organized at the faculty level address the role of women in society, their social protection, as well as contemporary challenges emerging in the context of globalization and their possible solutions. These activities involve faculty advisors for womenРІР‚в„ўs issues, psychologists, and specialists, providing students with practical knowledge and life skills.</p>
              <p>The university also places strong emphasis on increasing the social engagement of women. Various competitions, campaigns, and cultural events, such as initiatives conducted within the framework of the РІР‚Сљ16 Days of Activism Against Violence,РІР‚Сњ serve as important platforms for strengthening womenРІР‚в„ўs role in society and showcasing their creative and social potential. These initiatives contribute not only to supporting women but also to fostering a safe, inclusive, and healthy university environment.</p>
              <p>Within the framework of this policy, the university guarantees a safe and protected environment for every woman. In cases of violence or harassment, confidential reporting mechanisms are available, and each case is reviewed promptly, fairly, and impartially. Protecting victims and providing them with the necessary support is considered a priority responsibility of the institution.</p>
              <p>Overall, Karshi State University aims to create a modern, inclusive, and sustainable educational environment by supporting women and ensuring gender equality. This policy contributes to providing equal opportunities for all members of the university community, promoting respect for human dignity, and ensuring social justice, while being continuously improved in alignment with national and international sustainable development goals.</p>
            </div>
        """,
    },
    "ethics-code": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Qarshi davlat universiteti odob-axloq kodeksi",
        "title_en": "Code of Ethics of Karshi State University",
        "intro_uz": "Universitet jamoasida yuksak ma'naviy-axloqiy muhitni shakllantirish, akademik halollikni ta'minlash va ijtimoiy mas'uliyatni rivojlantirishga qaratilgan etik me'yorlar tizimi.",
        "intro_en": "An ethical framework designed to foster a strong moral culture, ensure academic integrity, and promote social responsibility across the university community.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>Qarshi davlat universitetining odob-axloq kodeksi mazmuni va ahamiyati</strong></p>
              <p>Qarshi davlat universitetining odob-axloq kodeksi universitet jamoasida yuksak ma'naviy-axloqiy muhitni shakllantirish, akademik halollikni ta'minlash va ijtimoiy mas'uliyatni rivojlantirishga qaratilgan muhim normativ hujjat hisoblanadi. Ushbu kodeks milliy va umuminsoniy qadriyatlarga tayangan holda ishlab chiqilgan bo'lib, u universitetning barcha xodimlari, talabalari va doktorantlari uchun majburiy hisoblanadi.</p>
              <p><strong>Kodeksning asosiy maqsadi</strong></p>
              <p>Kodeksning bosh maqsadi - universitet jamoasida axloqiy me'yorlarni shakllantirish, o'zaro hurmat va mas'uliyatni mustahkamlash, ta'lim jarayonida intizom va madaniyatni ta'minlash hamda universitet obro'sini oshirishdan iborat.</p>
              <p>Shuningdek, kodeks yosh avlodni milliy qadriyatlarga hurmat ruhida tarbiyalash, huquqbuzarliklarning oldini olish va sog'lom ijtimoiy-psixologik muhit yaratishga xizmat qiladi.</p>
              <p><strong>Asosiy prinsiplar</strong></p>
              <p>Kodeks bir qator muhim axloqiy va huquqiy prinsiplar asosida qurilgan:</p>
              <ul>
                <li><strong>Qonuniylik</strong> - barcha faoliyat amaldagi qonunchilikka mos bo'lishi kerak</li>
                <li><strong>Adolat va halollik</strong> - har bir qaror va harakat xolislik asosida amalga oshiriladi</li>
                <li><strong>Huquq va erkinliklarning ustuvorligi</strong> - inson qadr-qimmati oliy qadriyat sifatida e'tirof etiladi</li>
                <li><strong>Vatanparvarlik va sadoqat</strong> - universitet manfaatlariga xizmat qilish muhim vazifa sifatida qaraladi</li>
                <li><strong>Samaradorlik va tejamkorlik</strong> - resurslardan oqilona foydalanish targ'ib qilinadi</li>
              </ul>
              <p>Mazkur prinsiplar universitetda etik boshqaruv (ethical governance) va barqaror rivojlanish tamoyillarini mustahkamlashga xizmat qiladi.</p>
              <p><strong>Korrupsiyaga qarshi qat'iy yondashuv</strong></p>
              <p>Kodeksda korrupsiyaning har qanday shakli qat'iyan rad etiladi. Universitet jamoasi korrupsion holatlarga qarshi kurashish, ochiqlik va shaffoflikni ta'minlash, halollik prinsiplariga amal qilish majburiyatini oladi. Bu yondashuv SDG maqsadlari, xususan, institutsional shaffoflik va adolatli boshqaruv (SDG 16) talablariga to'liq mos keladi.</p>
              <p><strong>Xulq-atvor va kasbiy madaniyat</strong></p>
              <p>Kodeks universitet a'zolarining kundalik xulq-atvoriga ham aniq talablar qo'yadi. Jumladan:</p>
              <ul>
                <li>tashqi ko'rinish va kiyinish madaniyati</li>
                <li>o'zaro hurmat va muomala odobi</li>
                <li>jamoat joylarida tartib-intizom</li>
                <li>rasmiy muloqot madaniyati</li>
              </ul>
              <p>Ayniqsa, ijtimoiy tarmoqlarda va ommaviy axborot vositalarida universitet sha'niga putur yetkazuvchi noto'g'ri yoki asossiz ma'lumotlarni tarqatmaslik muhim talab sifatida belgilangan.</p>
              <p><strong>Akademik muhit va o'zaro munosabatlar</strong></p>
              <p>Kodeks universitet ichida sog'lom akademik muhitni ta'minlashga alohida e'tibor qaratadi. Unda:</p>
              <ul>
                <li>pedagog va talaba o'rtasidagi hurmatli munosabat</li>
                <li>akademik halollik</li>
                <li>tazyiq va kamsitishlarga yo'l qo'ymaslik</li>
                <li>bilim berish jarayonida adolatli yondashuv</li>
              </ul>
              <p>kabi tamoyillar belgilangan. Bu esa zamonaviy ta'lim tizimida muhim bo'lgan inklyuziv va adolatli ta'lim muhitini shakllantirishga xizmat qiladi.</p>
              <p><strong>Taqiqlangan xatti-harakatlar</strong></p>
              <p>Kodeksda universitet hududida qat'iyan man etilgan xatti-harakatlar ham aniq ko'rsatilgan:</p>
              <ul>
                <li>huquqbuzarlik va zo'ravonlik</li>
                <li>giyohvand moddalar va alkogol iste'moli</li>
                <li>akademik insofsizlik</li>
                <li>ekstremistik yoki zararli kontent tarqatish</li>
                <li>boshqalarning sha'ni va qadr-qimmatini kamsitish</li>
              </ul>
              <p>Bu cheklovlar universitetda xavfsiz, sog'lom va barqaror muhitni ta'minlashga qaratilgan.</p>
              <p><strong>Rahbariyatning mas'uliyati</strong></p>
              <p>Kodeks rahbarlar zimmasiga ham muhim vazifalarni yuklaydi:</p>
              <ul>
                <li>adolatli va xolis boshqaruv</li>
                <li>favoritizm va diskriminatsiyaga yo'l qo'ymaslik</li>
                <li>xodimlar uchun qulay ish sharoitlarini yaratish</li>
                <li>manfaatlar to'qnashuvining oldini olish</li>
              </ul>
              <p>Bu esa universitetda yaxshi boshqaruv tizimini mustahkamlaydi.</p>
              <p>Qarshi davlat universitetining odob-axloq kodeksi nafaqat ichki tartib-qoidalarni belgilovchi hujjat, balki universitetning etik qadriyatlari va barqaror rivojlanish strategiyasining muhim qismidir. U axloqiy madaniyatni shakllantiradi, akademik halollikni ta'minlaydi, ijtimoiy mas'uliyatni oshiradi va universitetning xalqaro imidjini mustahkamlaydi.</p>
              <p>Mazkur kodeks orqali universitet jamoasi o'z faoliyatida halollik, adolat va hurmat kabi qadriyatlarga asoslangan barqaror va inklyuziv muhitni rivojlantirishga intiladi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>Code of ethics of Karshi State University content and significance</strong></p>
              <p>The code of ethics of Karshi State University is a key regulatory document aimed at fostering a strong ethical culture, ensuring academic integrity, and promoting social responsibility within the university community. Developed based on national and universal values, the Code applies to all academic staff, administrative personnel, students, and doctoral candidates of the university.</p>
              <p><strong>Purpose of the code</strong></p>
              <p>The primary purpose of the code is to:</p>
              <ul>
                <li>establish and strengthen ethical standards</li>
                <li>promote mutual respect and responsibility</li>
                <li>ensure discipline and professionalism in the educational environment</li>
                <li>enhance the institutional reputation of the university</li>
              </ul>
              <p>Additionally, the code contributes to nurturing students and staff in the spirit of respect for national values, preventing misconduct, and creating a healthy socio-psychological environment.</p>
              <p><strong>Core principles</strong></p>
              <p>The code is based on the following fundamental principles:</p>
              <ul>
                <li><strong>Legality</strong> - all activities must comply with national legislation</li>
                <li><strong>Justice and Integrity</strong> - all actions and decisions must be fair and impartial</li>
                <li><strong>Respect for Rights and Freedoms</strong> - human dignity is recognized as a highest value</li>
                <li><strong>Patriotism and Loyalty</strong> - commitment to institutional and societal responsibilities</li>
                <li><strong>Efficiency and Responsibility</strong> - rational and careful use of resources</li>
              </ul>
              <p>These principles support ethical governance and align with the university's commitment to sustainable development.</p>
              <p><strong>Zero tolerance for corruption</strong></p>
              <p>The code clearly establishes a zero-tolerance policy towards all forms of corruption. Members of the university community are required to actively combat corruption, ensure transparency and accountability, and adhere strictly to ethical and legal standards. This approach is fully aligned with sustainable development goal 16 (Peace, Justice, and Strong Institutions).</p>
              <p><strong>Standards of conduct and professional behavior</strong></p>
              <p>The code defines clear expectations for daily conduct, including:</p>
              <ul>
                <li>appropriate dress and professional appearance</li>
                <li>respectful communication and behavior</li>
                <li>adherence to discipline in university premises</li>
                <li>responsible communication in public and digital spaces</li>
              </ul>
              <p>Special attention is given to maintaining the university's reputation by avoiding the dissemination of misleading or unverified information, especially on social media platforms.</p>
              <p><strong>Academic environment and interpersonal relations</strong></p>
              <p>The code emphasizes the importance of a respectful and inclusive academic environment. It promotes:</p>
              <ul>
                <li>mutual respect between faculty and students</li>
                <li>academic honesty and fairness</li>
                <li>prohibition of harassment or discrimination</li>
                <li>a supportive and student-centered teaching approach</li>
              </ul>
              <p>These principles contribute to building an inclusive and equitable learning environment.</p>
              <p><strong>Prohibited actions</strong></p>
              <p>The code strictly prohibits actions that may harm individuals or the institution, including:</p>
              <ul>
                <li>any form of misconduct or violence</li>
                <li>use or distribution of drugs, alcohol, or harmful substances</li>
                <li>academic dishonesty</li>
                <li>dissemination of extremist or inappropriate content</li>
                <li>actions that undermine human dignity</li>
              </ul>
              <p>These restrictions ensure a safe, respectful, and sustainable campus environment.</p>
              <p><strong>Responsibilities of leadership</strong></p>
              <p>The code also outlines key responsibilities for university leadership, including:</p>
              <ul>
                <li>ensuring fair and transparent management</li>
                <li>preventing favoritism and discrimination</li>
                <li>providing supportive working conditions</li>
                <li>managing conflicts of interest effectively</li>
              </ul>
              <p>This strengthens good governance and institutional accountability.</p>
              <p>The code of ethics of Karshi State University is not only a regulatory framework but also a reflection of the university's commitment to ethical values and sustainable development. It plays a vital role in fostering a culture of integrity, ensuring academic excellence, promoting social responsibility, and enhancing the university's global reputation.</p>
              <p>Through the implementation of this code, the university strives to create a sustainable, inclusive, and ethically responsible academic environment grounded in respect, fairness, and integrity.</p>
            </div>
        """,
    },
    "talabalar-kengashi": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Talabalar kengashi",
        "title_en": "Student Union",
        "intro_uz": "Talaba-yoshlar huquqlari, faolligi va tashabbuslarini qo'llab-quvvatlashga qaratilgan universitet yoshlar kengashi faoliyati.",
        "intro_en": "University Youth Council activity focused on supporting student rights, engagement, and youth initiatives.",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>TALABALAR KENGASHI</strong></p>
              <p>OРІР‚Вzbekiston Yoshlar ittifoqining Qarshi davlat universitetida ham boshlangРІР‚Вich tashkiloti mavjud boРІР‚Вlib, Oliy taРІР‚в„ўlim fan va innovatsiyalar vazirligi hamda OРІР‚Вzbekiston Yoshlar ittifoqi Markaziy Kengashining 2023-yil 29-apreldagi 6-son QoРІР‚Вshma qaroriga asosan universitetda Yoshlar Kengashi faoliyat yuritadi. Yoshlar Kengashining aРІР‚в„ўzolari 6 ta yoРІР‚Вnalish va 12 ta fakultet koordinatorlaridan iborat boРІР‚Вlib ularning maqsad va vazifalari quydagicha:</p>
              <ul>
                <li>BoshlangРІР‚Вich tashkilotning asosiy maqsadi oliy taРІР‚в„ўlim muassasasida tahsil olayotgan talaba-yoshlarning huquq va qonuniy manfaatlarini himoya qilish, ularning maРІР‚в„ўnaviy-mafkuraviy dunyoqarashini mustahkamlash, iqtidorli yoshlarni har tomonlama qoРІР‚Вllab-quvvatlash hamda ijtimoiy faolligini oshirishdan iboratdir. Shuningdek, talaba-yoshlarning boРІР‚Вsh vaqtlarini mazmunli tashkil etish, ularning tashabbus va gРІР‚Вoyalarini roРІР‚Вyobga chiqarishga koРІР‚Вmaklashish tashkilot faoliyatining ustuvor yoРІР‚Вnalishlaridan biri hisoblanadi.</li>
                <li>Ekologiya va atrof-muhitni muhofaza qilish, tabiiy resurslardan oqilona foydalanishni targРІР‚Вib qilish orqali yoshlarning ekologik madaniyatini yuksaltirish va ekologik tashabbuslarini qoРІР‚Вllab-quvvatlash ham tashkilot faoliyatining ajralmas qismi hisoblanadi.</li>
                <li>BoshlangРІР‚Вich tashkilot oРІР‚Вz oldiga qator muhim vazifalarni qoРІР‚Вyadi. Avvalo, oliy taРІР‚в„ўlim muassasasida talaba-yoshlarni qoРІР‚Вllab-quvvatlash, ularning huquq va manfaatlarini himoya qilishga qaratilgan amaliy chora-tadbirlar yuzasidan takliflar ishlab chiqadi. Yoshlar oРІР‚Вrtasida tibbiy madaniyatni oshirish, sogРІР‚Вlom turmush tarzini targРІР‚Вib qilish, kasalliklarning oldini olish boРІР‚Вyicha tushuntirish ishlari olib boriladi. Shu bilan birga, ijtimoiy himoyaga muhtoj, yetim va ota-onasining qaramogРІР‚Вidan mahrum boРІР‚Вlgan talaba-yoshlarning ijtimoiy-huquqiy himoyasini taРІР‚в„ўminlashda faol ishtirok etadi. Huquqbuzarlikdan jabrlangan yoki bunday holatlarga moyil boРІР‚Вlgan yoshlarni ijtimoiy reabilitatsiya qilish va jamiyatga moslashtirish boРІР‚Вyicha ishlar ham tashkilot eРІР‚в„ўtiborida boРІР‚Вladi.</li>
                <li>Tashkilot talaba-yoshlarni Vatanga muhabbat va sadoqat ruhida tarbiyalash, ularning ongiga milliy istiqlol gРІР‚Вoyasi, milliy qadriyatlar, diniy bagРІР‚Вrikenglik, millatlararo totuvlik va oilaviy qadriyatlarni singdirishga alohida ahamiyat qaratadi. Shu bilan birga, yoshlarning OРІР‚Вzbekiston Respublikasi Konstitutsiyasi va qonunlarida belgilangan huquq va burchlarini anglab yetishlariga koРІР‚Вmaklashadi hamda mamlakatda yoshlarga oid davlat siyosati doirasida amalga oshirilayotgan islohotlarning mazmun-mohiyatini tushuntiradi.</li>
                <li>Talaba-yoshlarning murojaatlari va muammolarini oРІР‚Вrganish, ularni hal etishda amaliy yordam koРІР‚Вrsatish ham tashkilot faoliyatining muhim yoРІР‚Вnalishlaridan biridir. Bundan tashqari, yoshlarning sifatli taРІР‚в„ўlim olishi, chet tillarini oРІР‚Вrganishi, zamonaviy axborot-kommunikatsiya texnologiyalarini puxta egallashi va kasb-hunarga yoРІР‚Вnaltirilishiga qaratilgan tadbirlar muntazam amalga oshiriladi.</li>
                <li>IsteРІР‚в„ўdodli yoshlarni aniqlash, ularni ragРІР‚Вbatlantirish va har tomonlama qoРІР‚Вllab-quvvatlash maqsadida turli tanlovlar, intellektual oРІР‚Вyinlar, ijodiy loyihalar hamda klub va toРІР‚Вgaraklar faoliyati yoРІР‚Вlga qoРІР‚Вyiladi. Shuningdek, talaba-yoshlar oРІР‚Вrtasida kitobxonlikni keng targРІР‚Вib qilish, kitob oРІР‚Вqishga boРІР‚Вlgan qiziqishni oshirish va kitobxonlik madaniyatini rivojlantirishga alohida eРІР‚в„ўtibor qaratiladi.</li>
                <li>Tashkilot yoshlar ongida РІР‚Сљommaviy madaniyatРІР‚Сњ niqobi ostidagi zararli illatlarga, turli axborot xurujlariga, diniy aqidaparastlik, missionerlik va ekstremistik gРІР‚Вoyalarga qarshi mustahkam mafkuraviy immunitetni shakllantirishga xizmat qiladi.</li>
                <li>Bundan tashqari, yoshlar turizmini rivojlantirish, ularni oРІР‚Вz hududidagi tarixiy obidalar, muqaddas qadamjolar, muzeylar, teatrlar hamda mustaqillik yillarida barpo etilgan zamonaviy inshootlar bilan yaqindan tanishtirish maqsadida turli sayohatlar tashkil etiladi.</li>
                <li>Talaba-yoshlar, ayniqsa xotin-qizlar oРІР‚Вrtasida sportni keng targРІР‚Вib qilish, ularning sportga boРІР‚Вlgan qiziqishini qoРІР‚Вllab-quvvatlash hamda turli sport musobaqalarida ishtirok etishlari uchun zarur shart-sharoitlar yaratib berish ham muhim vazifalardan biri hisoblanadi.</li>
              </ul>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>STUDENT UNION</strong></p>
              <p>The Youth Union of Uzbekistan has an established primary organization at Karshi State University. In accordance with the Joint Resolution No. 6 dated April 29, 2023, adopted by the Ministry of Higher Education, Science and Innovation and the Central Council of the Youth Union of Uzbekistan, a Youth Council operates within the university. The Youth Council consists of members representing six directions and coordinators from twelve faculties. Its primary goals and responsibilities are as follows:</p>
              <ul>
                <li>The main objective of the primary organization is to protect the rights and legitimate interests of student youth studying at the higher education institution, strengthen their spiritual and ideological outlook, support talented young people in all aspects, and enhance their social activity. Additionally, organizing studentsРІР‚в„ў free time in a meaningful way and assisting in the realization of their initiatives and ideas are among the priority areas of the organizationРІР‚в„ўs activities.</li>
                <li>Promoting ecological culture among youth through environmental protection activities, rational use of natural resources, and support for environmental initiatives is an integral part of its work.</li>
                <li>The primary organization sets a number of important tasks. First of all, it develops proposals for practical measures aimed at supporting students and protecting their rights and interests within the higher education institution. The organization also works to improve medical awareness among young people, promote a healthy lifestyle, and conduct awareness campaigns aimed at preventing diseases. It also actively participates in ensuring the social and legal protection of students in need, including orphans and those deprived of parental care. Furthermore, it works on the social rehabilitation and reintegration of young people affected by or vulnerable to offenses.</li>
                <li>The organization places special emphasis on fostering patriotism and devotion to the homeland among students, instilling in them the ideas of national independence, national values, religious tolerance, interethnic harmony, and family values. It also helps young people understand their rights and responsibilities as defined by the Constitution and laws of the Republic of Uzbekistan and raises awareness about the essence of reforms being implemented within the framework of state youth policy.</li>
                <li>Studying student appeals and problems and providing practical assistance in resolving them is another key area of activity. In addition, regular activities are carried out to ensure that students receive quality education, learn foreign languages, master modern information and communication technologies, and are guided toward professional development.</li>
                <li>To identify, encourage, and support talented youth, various competitions, intellectual games, creative projects, as well as clubs and extracurricular groups are organized. Special attention is also given to promoting reading culture, increasing interest in books, and developing a strong reading habit among students.</li>
                <li>The organization contributes to forming a strong ideological immunity among young people against harmful influences disguised as РІР‚Сљmass culture,РІР‚Сњ as well as against various information attacks, religious extremism, missionary activities, and radical ideas.</li>
                <li>Moreover, to promote youth tourism, various excursions are organized to introduce students to historical monuments, sacred sites, museums, theaters, and modern structures built during the years of independence.</li>
                <li>Finally, special attention is given to promoting sports among students, especially women, supporting their interest in sports, and creating favorable conditions for their participation in various sports competitions.</li>
              </ul>
            </div>
        """,
    },
    "uglerod-emissiyalari": {
        "eyebrow_uz": "Barqarorlik boshqaruvi",
        "eyebrow_en": "Sustainability governance",
        "title_uz": "Uglerod emissiyalarini kamaytirish maqsadlari",
        "title_en": "Carbon Emission Reduction Targets",
        "intro_uz": "(Scope 1 va Scope 2) 2024РІР‚вЂњ2050",
        "intro_en": "(Scope 1 and Scope 2) 2024РІР‚вЂњ2050",
        "sections_uz": [],
        "sections_en": [],
        "single_card_raw_uz": """
            <div class="governance-richtext">
              <p><strong>QARSHI DAVLAT UNIVERSITETI<br>UGLEROD EMISSIYALARINI KAMAYTIRISH MAQSADLARI<br>(SCOPE 1 VA SCOPE 2)<br>2024РІР‚вЂњ2050</strong></p>
              <p>Qarshi davlat universitetining Scope 1 va Scope 2 toifalariga kiruvchi issiqxona gazlari (GHG) emissiyalarini kamaytirish boРІР‚Вyicha uzoq muddatli maqsadlari universitetning 2024РІР‚вЂњ2025 yillardagi tasdiqlangan emissiya maРІР‚в„ўlumotlariga asoslangan boРІР‚Вlib, xalqaro iqlim majburiyatlari, xususan Parij kelishuvi talablariga muvofiq ishlab chiqilgan. Hujjatda 2050 yilgacha uglerod neytralligiga (Net Zero) erishish yoРІР‚Вli bosqichma-bosqich koРІР‚Вrsatib berilgan.</p>
              <p>Mazkur maqsadlar universitet tasarrufidagi barcha asosiy infratuzilma obyektlarini, jumladan oРІР‚Вquv binolari, maРІР‚в„ўmuriy binolar, talabalar turar joylari, laboratoriyalar va boshqa yordamchi inshootlarni qamrab oladi.</p>
              <p>Scope 1 emissiyalariga tabiiy gaz, koРІР‚Вmir va universitetga tegishli transport vositalarida ishlatiladigan yoqilgРІР‚Вi natijasida hosil boРІР‚Вladigan toРІР‚ВgРІР‚Вridan-toРІР‚ВgРІР‚Вri emissiyalar kiradi. Scope 2 emissiyalariga esa universitet tomonidan isteРІР‚в„ўmol qilinadigan elektr energiyasi bilan bogРІР‚Вliq bilvosita emissiyalar kiradi.</p>
              <p>2024РІР‚вЂњ2025 yillar uchun boshlangРІР‚Вich emissiya koРІР‚Вrsatkichlari quyidagi jadvalda keltirilgan.</p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Scope</th><th>Emissiya manbasi</th><th>Emissiya (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>Scope 1</td><td>Tabiiy gaz, koРІР‚Вmir yoqilgРІР‚Вisi</td><td>1,159</td></tr>
                  <tr><td>Scope 2</td><td>Elektr energiyasi</td><td>617.31</td></tr>
                  <tr><td><strong>Jami</strong></td><td><strong>Scope 1 + Scope 2</strong></td><td><strong>1,776.31</strong></td></tr>
                </tbody>
              </table>
              </div>
              <p>Tahlillar shuni koРІР‚Вrsatadiki, Scope 1 emissiyalarining asosiy qismi isitish tizimlarida ishlatiladigan tabiiy gaz hissasiga toРІР‚ВgРІР‚Вri keladi. Scope 2 emissiyalari esa toРІР‚Вliq elektr energiyasi isteРІР‚в„ўmoli bilan bogРІР‚Вliq.</p>
              <p>Qarshi davlat universiteti 2050 yilga borib Scope 1 va Scope 2 emissiyalarini nol darajaga (Net Zero) tushirishni oРІР‚Вz oldiga strategik maqsad qilib qoРІР‚Вyadi. Ushbu yakuniy maqsadga erishish uchun oraliq bosqichlar quyidagicha belgilangan.</p>
              <p><strong>Emissiyalarni kamaytirish maqsadlari</strong></p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Yil</th><th>Kamaytirish (%)</th><th>Emissiya (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>2025</td><td>BoshlangРІР‚Вich</td><td>1,776</td></tr>
                  <tr><td>2030</td><td>30%</td><td>1,243</td></tr>
                  <tr><td>2035</td><td>50%</td><td>888</td></tr>
                  <tr><td>2040</td><td>70%</td><td>533</td></tr>
                  <tr><td>2045</td><td>90%</td><td>178</td></tr>
                  <tr><td>2050</td><td>Net Zero</td><td>~0</td></tr>
                </tbody>
              </table>
              </div>
              <p>Scope 1 emissiyalarini kamaytirish asosan isitish tizimlarini transformatsiya qilish, yuqori emissiyali yoqilgРІР‚Вilarni bosqichma-bosqich bekor qilish hamda transport tizimini modernizatsiya qilish orqali amalga oshiriladi. Tabiiy gazdan foydalanish hozirgi kunda asosiy emissiya manbasi boРІР‚Вlib, uni elektr asosidagi isitish texnologiyalari, xususan issiqlik nasoslari bilan almashtirish rejalashtirilgan. Shu bilan birga, binolarning issiqlik izolyatsiyasini yaxshilash orqali umumiy energiya talabi kamaytiriladi.</p>
              <p>KoРІР‚Вmir yuqori emissiya koeffitsientiga ega boРІР‚Вlganligi sababli, uni ishlatish 2030 yilga qadar toРІР‚Вliq toРІР‚Вxtatiladi. Bu qisqa muddat ichida sezilarli emissiya kamayishiga olib keladi.</p>
              <p>Transport vositalaridan kelib chiqadigan emissiyalarni kamaytirish maqsadida universitet bosqichma-bosqich elektr transport vositalariga oРІР‚Вtadi. Bu esa uzoq muddatda yoqilgРІР‚Вi asosidagi emissiyalarni deyarli toРІР‚Вliq yoРІР‚Вq qilish imkonini beradi.</p>
              <p>Scope 2 emissiyalarini kamaytirish elektr energiyasi isteРІР‚в„ўmolini optimallashtirish va qayta tiklanuvchi energiya manbalarini kengaytirish orqali amalga oshiriladi. Universitetda LED yoritish tizimlari joriy etilgan boРІР‚Вlib, bu energiya samaradorligini oshirishga xizmat qilmoqda. Keyingi bosqichda asosiy eРІР‚в„ўtibor quyosh energiyasidan foydalanishni kengaytirishga qaratiladi. Universitet hududida quyosh panellarini oРІР‚Вrnatish orqali elektr energiyasining muhim qismini qayta tiklanuvchi manbalardan olish rejalashtirilgan. Shu bilan birga, energiya isteРІР‚в„ўmolini nazorat qilish va optimallashtirish uchun zamonaviy monitoring tizimlari joriy etiladi.</p>
              <p><strong>Scope 1 va Scope 2 emissiyalarining umumiy kamayish dinamikasi quyidagi jadvalda keltirilgan.</strong></p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Yil</th><th>Scope 1</th><th>Scope 2</th><th>Jami (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>2025</td><td>1,159</td><td>617</td><td>1,776</td></tr>
                  <tr><td>2030</td><td>850</td><td>400</td><td>1,250</td></tr>
                  <tr><td>2035</td><td>600</td><td>300</td><td>900</td></tr>
                  <tr><td>2040</td><td>350</td><td>180</td><td>530</td></tr>
                  <tr><td>2045</td><td>120</td><td>60</td><td>180</td></tr>
                  <tr><td>2050</td><td>~0</td><td>~0</td><td>Net Zero</td></tr>
                </tbody>
              </table>
              </div>
              <p>Mazkur maqsadlarning amalga oshirilishi doimiy monitoring va boshqaruv tizimi orqali taРІР‚в„ўminlanadi. Universitet har yili ISO 14064-1 standartiga muvofiq issiqxona gazlari inventarizatsiyasini amalga oshiradi. Ichki auditlar muntazam ravishda oРІР‚Вtkazilib, tashqi auditlar orqali maРІР‚в„ўlumotlarning ishonchliligi taРІР‚в„ўminlanadi.</p>
              <p>Asosiy koРІР‚Вrsatkichlar sifatida umumiy emissiya hajmi, qayta tiklanuvchi energiya ulushi va energiya samaradorligi darajasi monitoring qilinadi. Ushbu natijalar universitetning barqarorlik hisobotlariga va xalqaro reyting tizimlariga integratsiya qilinadi.</p>
            </div>
        """,
        "single_card_raw_en": """
            <div class="governance-richtext">
              <p><strong>KARSHI STATE UNIVERSITY<br>CARBON EMISSION REDUCTION TARGETS<br>(SCOPE 1 AND SCOPE 2)<br>2024РІР‚вЂњ2050</strong></p>
              <p>The long-term targets of Karshi State University for reducing greenhouse gas (GHG) emissions under Scope 1 and Scope 2 are based on the universityРІР‚в„ўs verified emissions data for the years 2024РІР‚вЂњ2025 and have been developed in accordance with international climate commitments, particularly the requirements of the Paris Agreement. The document outlines a step-by-step pathway for achieving carbon neutrality (Net Zero) by 2050.</p>
              <p>These targets cover all major infrastructure facilities under the management of the university, including academic buildings, administrative buildings, student dormitories, laboratories, and other supporting structures.</p>
              <p>Scope 1 emissions include direct emissions resulting from the use of natural gas, coal, and fuel consumed by university-owned vehicles. Scope 2 emissions include indirect emissions associated with the electricity consumed by the university.</p>
              <p>The baseline emission figures for the years 2024РІР‚вЂњ2025 are presented in the table below.</p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Scope</th><th>Emission Source</th><th>Emissions (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>Scope 1</td><td>Natural gas, coal, fuel</td><td>1,159</td></tr>
                  <tr><td>Scope 2</td><td>Electricity</td><td>617.31</td></tr>
                  <tr><td><strong>Total</strong></td><td><strong>Scope 1 + Scope 2</strong></td><td><strong>1,776.31</strong></td></tr>
                </tbody>
              </table>
              </div>
              <p>Analysis shows that the majority of Scope 1 emissions are attributable to natural gas used in heating systems, while Scope 2 emissions are entirely associated with electricity consumption.<br>Karshi State University has set a strategic goal to reduce Scope 1 and Scope 2 emissions to net zero by 2050. To achieve this final target, the following interim milestones have been established.</p>
              <p><strong>Emission Reduction Targets</strong></p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Year</th><th>Reduction (%)</th><th>Emissions (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>2024</td><td>Baseline</td><td>1,776</td></tr>
                  <tr><td>2030</td><td>30%</td><td>1,243</td></tr>
                  <tr><td>2035</td><td>50%</td><td>888</td></tr>
                  <tr><td>2040</td><td>70%</td><td>533</td></tr>
                  <tr><td>2045</td><td>90%</td><td>178</td></tr>
                  <tr><td>2050</td><td>Net Zero</td><td>~0</td></tr>
                </tbody>
              </table>
              </div>
              <p>Scope 1 emissions will be reduced primarily through the transformation of heating systems, the gradual phase-out of high-emission fuels, and the modernization of the transport system. Natural gas is currently the main source of emissions, and it is planned to replace it with electric-based heating technologies, particularly heat pumps. At the same time, overall energy demand will be reduced through improvements in building thermal insulation.</p>
              <p>Due to its high emission factor, coal will be completely phased out by 2030. This measure will result in a significant reduction in emissions in the short term.</p>
              <p>To reduce emissions from transport, the university will gradually transition to electric vehicles. In the long term, this will enable the near-complete elimination of fuel-based emissions.</p>
              <p>Scope 2 emissions will be reduced through the optimization of electricity consumption and the expansion of renewable energy sources. The university has already implemented LED lighting systems, which contribute to improved energy efficiency. In the next phase, the primary focus will be on expanding the use of solar energy. By installing solar panels across the campus, a significant share of electricity demand will be met from renewable sources. In addition, modern monitoring systems will be introduced to control and optimize energy consumption.</p>
              <p><strong>The overall reduction trajectory of Scope 1 and Scope 2 emissions is presented in the table below.</strong></p>
              <div class="governance-table-wrap">
              <table class="governance-table">
                <thead>
                  <tr><th>Year</th><th>Scope 1 (tCOРІвЂљвЂљe)</th><th>Scope 2 (tCOРІвЂљвЂљe)</th><th>Total (tCOРІвЂљвЂљe)</th></tr>
                </thead>
                <tbody>
                  <tr><td>2024</td><td>1,159</td><td>617</td><td>1,776</td></tr>
                  <tr><td>2030</td><td>850</td><td>400</td><td>1,250</td></tr>
                  <tr><td>2035</td><td>600</td><td>300</td><td>900</td></tr>
                  <tr><td>2040</td><td>350</td><td>180</td><td>530</td></tr>
                  <tr><td>2045</td><td>120</td><td>60</td><td>180</td></tr>
                  <tr><td>2050</td><td>~0</td><td>~0</td><td>Net Zero</td></tr>
                </tbody>
              </table>
              </div>
              <p>The implementation of these targets will be ensured through a continuous monitoring and management system. The university will conduct annual greenhouse gas inventories in accordance with the ISO 14064-1 standard. Internal audits will be carried out regularly, while external audits will ensure the reliability and accuracy of the data.</p>
              <p>Key indicators such as total emissions, the share of renewable energy, and the level of energy efficiency will be monitored. These results will be integrated into the universityРІР‚в„ўs sustainability reports and international ranking systems.</p>
            </div>
        """,
    },
}

GOVERNANCE_PAGE_CONTENT["disability-support-policy"] = ANTI_CORRUPTION_CONTACT_CONTENT["disability-support-policy"]


DISABILITY_SUPPORT_ROADMAP_CONTENT = {
    "uz": {
        "eyebrow": "Barqarorlik boshqaruvi",
        "title": "Qarshi davlat universitetining nogironligi bo'lgan talabalar uchun inklyuziv ta'lim muhiti holatini baholab, kamchiliklarni bartaraf etish bo'yicha \"YO'L-XARITASI\"",
        "intro": "Nogironligi bo'lgan talabalar uchun ta'lim muhiti, infratuzilma va qo'llab-quvvatlash xizmatlarini bosqichma-bosqich yaxshilashga qaratilgan amaliy reja.",
        "table_headers": ["РІвЂћвЂ“", "Chora-tadbir nomi", "Amalga oshirish mexanizmi", "Muddat", "Mas'ullar"],
        "rows": [
            {
                "no": "1",
                "activity": "Ta'lim muhitini (auditoriya, TTJ, hudud) tahlil qilish.",
                "mechanism_steps": [
                    "Ishchi guruh tuzish.",
                    "Ishchi guruh xulosalari asosida tegishli chora-tadbirlarni amalga oshirib borish.",
                    "Ishchi guruh xulosalarini universitet Kengashlarida muhokama qilib borish.",
                ],
                "timeline": "2025-yil iyun",
                "responsible_people": [
                    "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor (O.Kuziyev)",
                    "O'quv ishlari bo'yicha prorektor",
                ],
            },
            {
                "no": "2",
                "activity": "Ta'lim dasturi bo'yicha maxsus o'quv materiallari (Brayl alifbosidagi kitoblar, ko'rgazmali materiallar), maxsus jihozlar va yordamchi texnik vositalar mavjudligi.",
                "mechanism_steps": [
                    "Tegishli fanlarni aniqlash.",
                    "Audio, elektron adabiyotlarni tayyorlash.",
                    "Tayyorlangan audio, elektron adabiyotlarni talabalarga yetkazish.",
                ],
                "timeline": "O'quv yili davomida",
                "responsible_people": [
                    "O'quv ishlari bo'yicha prorektor",
                    "Axborot-resurs markazi direktori K.Dusyorova",
                ],
            },
            {
                "no": "3",
                "activity": "Nogironligi bo'lgan talabalarni qiziqish va imkoniyatlaridan kelib chiqib to'garaklarga jalb etish.",
                "mechanism_steps": [
                    "Nogironligi bo'lgan talabalar ro'yxatini shakllantirish.",
                    "Ushbu talabalarni qiziqish va imkoniyatlaridan kelib chiqib \"Ustoz-shogird\" an'anasi asosida professor-o'qituvchilarga biriktirish.",
                    "To'garaklarda ishtirokini ta'minlash.",
                ],
                "timeline": "2025-yil may",
                "responsible_people": [
                    "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor (O.Kuziyev)",
                    "Fakultet dekanlari",
                ],
            },
            {
                "no": "4",
                "activity": "Nogironligi bo'lgan talabalarni rag'batlantirish va moddiy qo'llab-quvvatlash.",
                "mechanism_steps": [
                    "Nogironligi bo'lgan talabalar ro'yxati asosida tegishli hujjatlarni jamlash.",
                    "Tegishli hujjatlar asosida universitet rektori buyrug'i loyihasini tayyorlash.",
                    "Nogironligi bo'lgan talabalarni moddiy qo'llab-quvvatlash.",
                ],
                "timeline": "Alohida reja asosida",
                "responsible_people": [
                    "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor O.Kuziyev",
                    "Moliya-iqtisod ishlari bo'yicha prorektor",
                    "Fakultet dekanlari",
                ],
            },
            {
                "no": "5",
                "activity": "3-dekabr РІР‚вЂњ РІР‚СљXalqaro nogironlar kuniРІР‚Сњ munosabati bilan universitetda РІР‚СљHech kim mehr va eРІР‚в„ўtibordan chetda qolmasin!РІР‚Сњ shiori ostida tadbirlar tashkil etish.",
                "mechanism_steps": [
                    "Tadbirlar rejasini ishlab chiqib, tasdiqlash.",
                    "Tadbirlar ssenariysini ishlab chiqish.",
                ],
                "timeline": "2025-yil dekabr",
                "responsible_people": [
                    "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor O.Kuziyev",
                    "Fakultet dekanlari",
                ],
            },
            {
                "no": "6",
                "activity": "Nogironligi bo'lgan shaxslar uchun qulay muhit va to'siqsiz harakatlanish imkoniyatini yaratish.",
                "mechanism_steps": [
                    "Universitet bino-inshootlarini nogironligi bo'lgan shaxslarning to'siqsiz harakatlanishi va ta'lim olish imkoniyatini yaratish uchun rekonstruksiya qilish va jihozlash choralarini ko'rish.",
                    "Yangi qurilayotgan o'quv binosida nogironlar yo'lakchalari va boshqa infratuzilmalarni yaratish.",
                ],
                "timeline": "2025-yil davomida",
                "responsible_people": [
                    "Moliya-iqtisod ishlari bo'yicha prorektor.",
                ],
            },
            {
                "no": "7",
                "activity": "Inklyuziv ta'lim uchun AKT, elektron resurslar, dasturiy ta'minotdan foydalanish imkoniyati (audio-video resurslar, Brayl yozuvi alifbosi, subtitr va boshqalar) yaratish.",
                "mechanism_steps": [
                    "Inklyuziv ta'lim uchun AKT, elektron resurslar va dasturiy ta'minot (audio-video resurslar, Brayl yozuvi, subtitr va boshqalar) yaratish.",
                    "Ushbu resurslar nogironligi bo'lgan talabalar uchun o'quv jarayonida qo'llash va ta'lim dasturi maqsadlariga erishishga xizmat qilishi.",
                    "AKT va elektron resurslardan foydalanish samaradorligini monitoring qilish, yangilash va qo'llab-quvvatlash mexanizmlari tashkil qilish.",
                ],
                "timeline": "O'quv yili davomida",
                "responsible_people": [
                    "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor (O.Kuziyev)",
                    "Moliya-iqtisod ishlari bo'yicha prorektor",
                    "O'quv ishlari bo'yicha prorektor",
                    "Axborot-resurs markazi direktori K.Dusyorova",
                ],
            },
        ],
    },
    "en": {
        "eyebrow": "Sustainability governance",
        "title": "Assessment of the Inclusive Education Environment for Students with Disabilities at Karshi State University and a \"Roadmap\" for Eliminating Identified Shortcomings",
        "intro": "A practical roadmap for improving the learning environment, infrastructure, and support services for students with disabilities.",
        "table_headers": ["No.", "Name of Activity", "Implementation mechanism", "Timeline", "Responsible persons"],
        "rows": [
            {
                "no": "1",
                "activity": "Assessment of the educational environment (classrooms, dormitories, campus area).",
                "mechanism_steps": [
                    "Establish a working group.",
                    "Implement appropriate measures based on the conclusions of the working group.",
                    "Regularly discuss the working group's conclusions at University Council meetings.",
                ],
                "timeline": "June 2025",
                "responsible_people": [
                    "First Vice-Rector for Youth Affairs (O. Kuziyev)",
                    "Vice-Rector for Academic Affairs",
                ],
            },
            {
                "no": "2",
                "activity": "Availability of specialized learning materials (Braille books, visual materials), equipment, and assistive technologies.",
                "mechanism_steps": [
                    "Identify relevant subjects.",
                    "Prepare audio and electronic materials.",
                    "Deliver materials to students.",
                ],
                "timeline": "Throughout academic year",
                "responsible_people": [
                    "Vice-Rector for Academic Affairs",
                    "Director of Information Resource Center (K. Dusyorova)",
                ],
            },
            {
                "no": "3",
                "activity": "Engagement of students with disabilities in extracurricular clubs.",
                "mechanism_steps": [
                    "Compile list of students.",
                    "Assign mentors based on interests (mentor-mentee system).",
                    "Ensure participation in clubs.",
                ],
                "timeline": "May 2025",
                "responsible_people": [
                    "First Vice-Rector (O. Kuziyev)",
                    "Faculty Deans",
                ],
            },
            {
                "no": "4",
                "activity": "Encouragement and financial support for students with disabilities.",
                "mechanism_steps": [
                    "Collect required documents.",
                    "Prepare Rector's order draft.",
                    "Provide financial support.",
                ],
                "timeline": "Based on separate plan",
                "responsible_people": [
                    "First Vice-Rector (O. Kuziyev)",
                    "Vice-Rector for Finance",
                    "Faculty Deans",
                ],
            },
            {
                "no": "5",
                "activity": "Organization of events for International Day of Persons with Disabilities.",
                "mechanism_steps": [
                    "Develop and approve plan.",
                    "Prepare event program/script.",
                ],
                "timeline": "December 2025",
                "responsible_people": [
                    "First Vice-Rector (O. Kuziyev)",
                    "Faculty Deans",
                ],
            },
            {
                "no": "6",
                "activity": "Creating an accessible and barrier-free environment.",
                "mechanism_steps": [
                    "Reconstruct and equip buildings.",
                    "Create accessible infrastructure in new buildings.",
                ],
                "timeline": "Throughout 2025",
                "responsible_people": [
                    "Vice-Rector for Finance and Economic Affairs",
                ],
            },
            {
                "no": "7",
                "activity": "Use of ICT, electronic resources, and software for inclusive education.",
                "mechanism_steps": [
                    "Develop ICT tools and resources.",
                    "Integrate into learning process.",
                    "Monitor and update effectiveness.",
                ],
                "timeline": "Throughout academic year",
                "responsible_people": [
                    "First Vice-Rector (O. Kuziyev)",
                    "Vice-Rectors",
                    "Director of Information Resource Center (K. Dusyorova)",
                ],
            },
        ],
    },
}


SDG_CONTENT = [
    {
        "number": 1,
        "image_en": "images/goals/E_WEB_01.png",
        "image_uz": "images/goals/E_WEB_01.png",
        "gif": "images/goals/gifs/E_GIF_01.gif",
        "title_en": "No Poverty",
        "title_uz": "Kambag'allikka barham berish",
        "description_en": "End poverty in all its forms everywhere through inclusive protection systems, access to services, and resilient livelihoods.",
        "description_uz": "Har qanday ko'rinishdagi kambag'allikka barham berish, himoya tizimlari, xizmatlar va barqaror turmush manbalari orqali aholining imkoniyatlarini kengaytirish.",
    },
    {
        "number": 2,
        "image_en": "images/goals/E_WEB_02.png",
        "image_uz": "images/goals/E_WEB_02.png",
        "gif": "images/goals/gifs/E_GIF_02.gif",
        "title_en": "Zero Hunger",
        "title_uz": "Ochlikka barham berish",
        "description_en": "Achieve food security, improve nutrition, and promote sustainable agriculture for healthier communities.",
        "description_uz": "Oziq-ovqat xavfsizligini ta'minlash, ovqatlanish sifatini yaxshilash va barqaror qishloq xo'jaligini rivojlantirish.",
    },
    {
        "number": 3,
        "image_en": "images/goals/E_WEB_03.png",
        "image_uz": "images/goals/E_WEB_03.png",
        "gif": "images/goals/gifs/E_GIF_03.gif",
        "title_en": "Good Health and Well-being",
        "title_uz": "Sog'lik va farovonlik",
        "description_en": "Ensure healthy lives and promote well-being for all at all ages with equitable access to health services.",
        "description_uz": "Har bir yoshdagi insonlar uchun sog'lom turmush va farovonlikni ta'minlash, tibbiy xizmatlardan teng foydalanishni kengaytirish.",
    },
    {
        "number": 4,
        "image_en": "images/goals/E_WEB_04.png",
        "image_uz": "images/goals/E_WEB_04.png",
        "gif": "images/goals/gifs/E_GIF_04.gif",
        "title_en": "Quality Education",
        "title_uz": "Sifatli ta'lim",
        "description_en": "Deliver inclusive and equitable quality education and promote lifelong learning opportunities for all.",
        "description_uz": "Inklyuziv va adolatli sifatli ta'limni ta'minlash hamda umrbod o'qish imkoniyatlarini kengaytirish.",
    },
    {
        "number": 5,
        "image_en": "images/goals/E_WEB_05.png",
        "image_uz": "images/goals/E_WEB_05.png",
        "gif": "images/goals/gifs/E_GIF_05.gif",
        "title_en": "Gender Equality",
        "title_uz": "Gender tenglik",
        "description_en": "Achieve gender equality and empower all women and girls in leadership, education, and economic life.",
        "description_uz": "Gender tengligini ta'minlash va barcha ayollar hamda qizlarning ta'lim, boshqaruv va iqtisodiy hayotdagi imkoniyatlarini oshirish.",
    },
    {
        "number": 6,
        "image_en": "images/goals/E_WEB_06.png",
        "image_uz": "images/goals/E_WEB_06.png",
        "gif": "images/goals/gifs/E_GIF_06.gif",
        "title_en": "Clean Water and Sanitation",
        "title_uz": "Toza suv va sanitariya",
        "description_en": "Ensure availability and sustainable management of water and sanitation for all communities.",
        "description_uz": "Barcha uchun xavfsiz ichimlik suvi va sanitariya xizmatlaridan foydalanishni hamda ularning barqaror boshqaruvini ta'minlash.",
    },
    {
        "number": 7,
        "image_en": "images/goals/E_WEB_07.png",
        "image_uz": "images/goals/E_WEB_07.png",
        "gif": "images/goals/gifs/E_GIF_07.gif",
        "title_en": "Affordable and Clean Energy",
        "title_uz": "Arzon va toza energiya",
        "description_en": "Ensure access to affordable, reliable, sustainable, and modern energy for all.",
        "description_uz": "Arzon, ishonchli, zamonaviy va ekologik toza energiyadan foydalanish imkonini kengaytirish.",
    },
    {
        "number": 8,
        "image_en": "images/goals/E_WEB_08.png",
        "image_uz": "images/goals/E_WEB_08.png",
        "gif": "images/goals/gifs/E_GIF_08.gif",
        "title_en": "Decent Work and Economic Growth",
        "title_uz": "Munosib mehnat va iqtisodiy o'sish",
        "description_en": "Promote sustained, inclusive economic growth, productive employment, and decent work for all.",
        "description_uz": "Barqaror va inklyuziv iqtisodiy o'sishni, samarali bandlikni va munosib mehnat sharoitlarini rivojlantirish.",
    },
    {
        "number": 9,
        "image_en": "images/goals/E_WEB_09.png",
        "image_uz": "images/goals/E_WEB_09.png",
        "gif": "images/goals/gifs/E_GIF_09.gif",
        "title_en": "Industry, Innovation and Infrastructure",
        "title_uz": "Sanoat, innovatsiya va infratuzilma",
        "description_en": "Build resilient infrastructure, promote inclusive industrialization, and foster innovation.",
        "description_uz": "Chidamli infratuzilmani rivojlantirish, inklyuziv sanoatlashuvni qo'llab-quvvatlash va innovatsiyalarni kuchaytirish.",
    },
    {
        "number": 10,
        "image_en": "images/goals/E_WEB_10.png",
        "image_uz": "images/goals/E_WEB_10.png",
        "gif": "images/goals/gifs/E_GIF_10.gif",
        "title_en": "Reduced Inequalities",
        "title_uz": "Tengsizlikni qisqartirish",
        "description_en": "Reduce inequality within and among countries through inclusive policy and equal opportunity.",
        "description_uz": "Mamlakat ichida va mamlakatlar o'rtasidagi tengsizlikni kamaytirish, teng imkoniyat va inklyuziv siyosatni kuchaytirish.",
    },
    {
        "number": 11,
        "image_en": "images/goals/E_WEB_11.png",
        "image_uz": "images/goals/E_WEB_11.png",
        "gif": "images/goals/gifs/E_GIF_11.gif",
        "title_en": "Sustainable Cities and Communities",
        "title_uz": "Barqaror shaharlar va aholi yashash joylari",
        "description_en": "Make cities and human settlements inclusive, safe, resilient, and sustainable.",
        "description_uz": "Shaharlar va aholi yashash joylarini xavfsiz, inklyuziv, chidamli va barqaror qilish.",
    },
    {
        "number": 12,
        "image_en": "images/goals/E_WEB_12.png",
        "image_uz": "images/goals/E_WEB_12.png",
        "gif": "images/goals/gifs/E_GIF_12.gif",
        "title_en": "Responsible Consumption and Production",
        "title_uz": "Mas'uliyatli iste'mol va ishlab chiqarish",
        "description_en": "Ensure sustainable consumption and production patterns across institutions and communities.",
        "description_uz": "Muassasalar va jamoalarda barqaror iste'mol va ishlab chiqarish madaniyatini shakllantirish.",
    },
    {
        "number": 13,
        "image_en": "images/goals/E_WEB_13.png",
        "image_uz": "images/goals/E_WEB_13.png",
        "gif": "images/goals/gifs/E_GIF_13.gif",
        "title_en": "Climate Action",
        "title_uz": "Iqlim o'zgarishiga qarshi kurashish",
        "description_en": "Take urgent action to combat climate change and its impacts through adaptation and mitigation.",
        "description_uz": "Iqlim o'zgarishi va uning oqibatlariga qarshi tezkor choralar ko'rish, moslashuv va kamaytirish strategiyalarini kuchaytirish.",
    },
    {
        "number": 14,
        "image_en": "images/goals/E_WEB_14.png",
        "image_uz": "images/goals/E_WEB_14.png",
        "gif": "images/goals/gifs/E_GIF_14.gif",
        "title_en": "Life Below Water",
        "title_uz": "Suv osti hayoti",
        "description_en": "Conserve and sustainably use oceans, seas, and marine resources for sustainable development.",
        "description_uz": "Okeanlar, dengizlar va suv resurslarini asrash va ulardan barqaror foydalanishni rivojlantirish.",
    },
    {
        "number": 15,
        "image_en": "images/goals/E_WEB_15.png",
        "image_uz": "images/goals/E_WEB_15.png",
        "gif": "images/goals/gifs/E_GIF_15.gif",
        "title_en": "Life on Land",
        "title_uz": "Quruqlikdagi hayot",
        "description_en": "Protect, restore, and promote sustainable use of terrestrial ecosystems and biodiversity.",
        "description_uz": "Quruqlik ekotizimlarini asrash, tiklash va biologik xilma-xillikni qo'llab-quvvatlash.",
    },
    {
        "number": 16,
        "image_en": "images/goals/E_WEB_16.png",
        "image_uz": "images/goals/E_WEB_16.png",
        "gif": "images/goals/gifs/E_GIF_16.gif",
        "title_en": "Peace, Justice and Strong Institutions",
        "title_uz": "Tinchlik, adolat va samarali boshqaruv",
        "description_en": "Promote peaceful societies, provide access to justice, and build effective, accountable institutions.",
        "description_uz": "Tinch va inklyuziv jamiyatlarni rivojlantirish, adolatga erishishni kengaytirish va samarali, hisobdor institutlarni mustahkamlash.",
    },
    {
        "number": 17,
        "image_en": "images/goals/E_WEB_17.png",
        "image_uz": "images/goals/E_WEB_17.png",
        "gif": "images/goals/gifs/E_GIF_17.gif",
        "title_en": "Partnerships for the Goals",
        "title_uz": "Maqsadlar yo'lida hamkorlik",
        "description_en": "Strengthen implementation and revitalize global partnerships for sustainable development.",
        "description_uz": "Barqaror rivojlanish uchun milliy va global hamkorliklarni kuchaytirish va birgalikdagi amalga oshirish mexanizmlarini rivojlantirish.",
    },
]


SDG_1_DETAIL_UZ = {
    "hero_title": "OРІР‚Вta qashshoqlikka barham berish",
    "idea_title": "Asosiy gРІР‚Вoya",
    "idea_text": "Butun dunyoda barcha turdagi qashshoqlikni butkul yoРІР‚Вq qilish",
    "sections": [
        {
            "title": "Umumiy maРІР‚в„ўlumot",
            "paragraphs": [
                "2015-yilda Birlashgan Millatlar Tashkiloti tomonidan belgilangan Barqaror rivojlanish maqsadlarining birinchi yoРІР‚Вnalishi РІР‚вЂќ qashshoqlikning barcha shakllariga barham berishdir (SDG 1).",
                "Davlatlar quyidagi prinsipni qabul qilgan: РІР‚СљHech kimni ortda qoldirmaslikРІР‚Сњ.",
                "Bu maqsad oziq-ovqat yetishmovchiligi, toza ichimlik suvi muammosi va sanitariya yetishmasligi kabi muammolarni ham qamrab oladi.",
                "Shuningdek, iqlim oРІР‚Вzgarishi va mojarolar keltirib chiqaradigan xavflarni ham hal qilishni talab qiladi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 1 doirasida 7 ta maqsad va 13 ta koРІР‚Вrsatkich mavjud.",
                "Natijada quyidagilar amalga oshiriladi:",
            ],
            "bullets": [
                "OРІР‚Вta qashshoqlikni yoРІР‚Вq qilish",
                "Qashshoqlikni kamida 50% ga qisqartirish",
                "Ijtimoiy himoya tizimini yaratish",
                "Resurs va xizmatlarga teng kirishni taРІР‚в„ўminlash",
                "Ofatlarga chidamlilikni oshirish",
            ],
        },
        {
            "title": "Global holat",
            "paragraphs": ["Hozirgi kunda quyidagi koРІР‚Вrsatkichlar dolzarb hisoblanadi:"],
            "bullets": [
                "Dunyo aholisining taxminan 10% qashshoqlikda yashaydi",
                "2015-yilda 736 million odam oРІР‚Вta qashshoqlikda yashagan",
                "Eng katta ulush Afrika hududiga toРІР‚ВgРІР‚Вri keladi",
                "Qishloqlarda qashshoqlik darajasi 17.2%",
                "Shaharlarda qashshoqlik darajasi 5.3%",
            ],
        },
        {
            "title": "Muammolar va xavflar",
            "paragraphs": [
                "Qashshoqlikka qarshi kurashni qiyinlashtirayotgan omillar quyidagilar:",
            ],
            "bullets": [
                "iqtisodiy tengsizlik",
                "siyosiy beqarorlik",
                "iqlim oРІР‚Вzgarishi",
                "urush va mojarolar",
            ],
        },
        {
            "title": "Bolalar va qashshoqlik",
            "bullets": [
                "385 millionga yaqin bola kuniga $1.90 dan kam daromad bilan yashaydi",
                "KoРІР‚Вplab mamlakatlarda bolalar qashshoqligi boРІР‚Вyicha aniq statistika yoРІР‚Вq",
                "97% mamlakatda yetarli data mavjud emas",
            ],
        },
        {
            "title": "Ijobiy oРІР‚Вzgarishlar",
            "paragraphs": [
                "1990РІР‚вЂњ2015 oraligРІР‚Вida qashshoqlikda yashovchilar soni 1.8 milliarddan 776 milliongacha kamaydi.",
                "Ammo muammo hali toРІР‚Вliq hal boРІР‚Вlmagan va erishilgan natijalarni saqlab qolish uchun izchil siyosat zarur.",
            ],
        },
        {
            "title": "Hukumatlar roli",
            "paragraphs": ["Mahalliy va global hukumatlar quyidagi yoРІР‚Вnalishlarda faol ishlaydi:"],
            "bullets": [
                "kam taРІР‚в„ўminlanganlarni qoРІР‚Вllab-quvvatlash",
                "shaffof boshqaruvni taРІР‚в„ўminlash",
                "bandlikni oshirish",
                "taРІР‚в„ўlim va iqtisodiy imkoniyatlarni kengaytirish",
            ],
        },
    ],
}


SDG_1_DETAIL_UZ_CLEAN = {
    "hero_title": "O'ta qashshoqlikka barham berish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Butun dunyoda barcha turdagi qashshoqlikni butkul yo'q qilish",
    "article_mode": True,
    "article_blocks": [
        {
            "type": "paragraph",
            "content": "2015-yilda Birlashgan Millatlar Tashkiloti tomonidan belgilangan Barqaror rivojlanish maqsadlarining birinchi maqsadi Qashshoqlikning barcha shakllariga barham berish (keyingi o'rinlarda SDG 1 deb yuritiladi) deyiladi. BRM ga a'zo davlatlar \"Hech kimni ortda qoldirmaslik va eng uzoq hududlardagi aholiga birinchi navbatda yordamga borish\" majburiyatini o'z zimmalariga oldilar. SDG 1 o'ta qashshoqlikning barcha shakllariga, jumladan oziq-ovqat, toza ichimlik suvi va sanitariya yetishmasligiga barham berishga qaratilgan. Ushbu maqsadga erishish iqlim o'zgarishi va mojarolar keltirib chiqaradigan yangi tahdidlarga yechim topishni o'z ichiga oladi.",
        },
        {
            "type": "paragraph",
            "content": "SDG 1ni amalga oshirish uchun 7 maqsad va taraqqiyot yo'lini belgilash uchun 13 ko'rsatkich mavjud. Yuqoridagi vazifalarni amalga oshirgandan so'ng quyidagi natijaga erishiladi:",
        },
        {
            "type": "list",
            "items": [
                "o'ta qashshoqlikni yo'q qilish",
                "barcha turdagi qashshoqliklarni yarmiga qisqartirish",
                "ijtimoiy himoya tizimlarini joriy etish",
                "mulk, asosiy xizmatlar, texnologiyalar va iqtisodiy resurslardan foydalanishga teng huquqlarni ta'minlash",
                "ekologik, iqtisodiy va ijtimoiy ofatlarga chidamlilikni oshirish",
            ],
        },
        {
            "type": "paragraph",
            "content": "Taraqqiyot davom etayotganiga qaramay, dunyo aholisining 10 foizi qashshoqlikda yashaydi va sog'liqni saqlash, ta'lim, suv va kanalizatsiya kabi asosiy ehtiyojlarni qondirish uchun kurashmoqda. Haddan tashqari qashshoqlik daromadi past mamlakatlarda, ayniqsa, mojarolar va siyosiy g'alayonlardan jabrlangan mamlakatlarda hamon keng tarqalgan. 2015-yilgi statistika shuni ko'rsatadiki, o'ta qashshoqlikda yashovchi 736 million aholining yarmidan ko'pi Sahroi Kabir va janubiy Afrika hududlariga to'g'ri keladi. Bunday holatda, ijtimoiy siyosat jarayonida sezilarli siljishlarsiz, 2030-yilga kelib qashshoqlik keskin ortadi. 2016 yilgi statistikaga ko'ra, qishloqlarda qashshoqlik darajasi 17,2 foizni, shaharlarda esa 5,3 foizni tashkil etadi.",
        },
        {
            "type": "paragraph",
            "content": "Kambag'allikni o'lchaydigan asosiy ko'rsatkichlardan biri bu xalqaro va milliy qashshoqlik chegarasidan pastda yashaydigan aholi ulushidir. Ijtimoiy himoya tizimlari bilan qamrab olingan va asosiy xizmatlardan foydalana oladigan uy xo'jaliklarida yashovchi aholi ulushini o'lchash ham qashshoqlik darajasini ko'rsatib beruvchi ko'rsatkichlardan biridir. 2020-yildagi COVID-19 pandemiyasi qashshoqlikka barham berishni qiyinlashtirdi. 2020-yil sentabrida chop etilgan tadqiqot shuni ko'rsatdiki, qashshoqlik oxirgi 20 yil ichida barqaror ravishda pasayib borayotgan bo'lsa-da, bir necha oy ichida 7 foizga oshgan.",
        },
        {
            "type": "paragraph",
            "content": "Qashshoqlik bolalarni ham chetlab o'tmadi. Har yil qancha bola ochlik va muhtojlikda yashayotgani haqida statistika qilinib boriladi. Lekin bu statistikalar doim ham to'g'ri chiqavermaydi. Misol uchun, 2013-yildagi ma'lumotlarga qaraydigan bo'lsak, taxminan 385 million bola kuniga 1,90 AQSh dollaridan kam pul bilan yashagan. Dunyo bo'ylab bolalarning ahvoli to'g'risidagi to'liq ma'lumotlar mavhumligi tufayli bu raqamlar ishonchsizdir. O'rtacha 97 foiz mamlakatlarda kam ta'minlangan bolalarning ahvolini aniqlash va SDG 1ga erishish yo'llarini ishlab chiqish uchun yetarlicha ma'lumotlar yo'q. Mamlakatlarning 63 foizida esa bolalar qashshoqligi haqida hech qanday statistika yo'q.",
        },
        {
            "type": "paragraph",
            "content": "1990-yildan buyon dunyo mamlakatlari qashshoqlikni kamaytirish uchun turli chora-tadbirlarni amalga oshirib, samarali natijalarga erishdi. 2013-yilda o'ta qashshoqlikda yashovchi odamlar soni 1,8 milliarddan 776 milliongacha kamaydi. Biroq, quyori natijalarga qaramasadan odamlar qashshoqlikda yashashda davom etmoqda. Jahon bankining hisob-kitoblariga ko'ra, 2020-yilda 40 dan 60 milliongacha odam o'ta qashshoqlikka tushib qoladi",
        },
        {
            "type": "paragraph",
            "content": "Dunyoning eng qashshoq mamlakatlarida iqtisodiy o'sishning yo'qligi, tengsizlikning kuchayishi, davlatchilikning tobora zaiflashib borayotgani va iqlim o'zgarishi kabi oqibatlar SDG 1ga erishishga to'sqinlik qilmoqda. Mahalliy hukumatlar qashshoqlik bilan bog'liq masalalarni yechishda muhim rol o'ynaydi. Butun dunyoda mahalliy hukumatni vazifalari turlicha bo'lib, quyidagi vazifalar bajaradilar:",
        },
        {
            "type": "list",
            "items": [
                "kam ta'minlanganlarning ehtiyojlarini qondirish",
                "hisobdorlik va shaffoflikni ta'minlash uchun yaxshi boshqaruv",
                "bandlikni yaxshilash uchun inklyuziv ta'limni yaxshi yo'lga qo'yish",
                "ehtiyojmand aholi va qishloq jamoalariga ta'sir ko'rsatadigan davlat korxonalarining biznes etikasi ustida ishlash",
            ],
        },
    ],
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "2015-yilda Birlashgan Millatlar Tashkiloti tomonidan belgilangan Barqaror rivojlanish maqsadlarining birinchi maqsadi Qashshoqlikning barcha shakllariga barham berish (keyingi o'rinlarda SDG 1 deb yuritiladi) deyiladi.",
                "BRM ga a'zo davlatlar \"Hech kimni ortda qoldirmaslik va eng uzoq hududlardagi aholiga birinchi navbatda yordamga borish\" majburiyatini o'z zimmalariga oldilar.",
                "SDG 1 o'ta qashshoqlikning barcha shakllariga, jumladan oziq-ovqat, toza ichimlik suvi va sanitariya yetishmasligiga barham berishga qaratilgan.",
                "Ushbu maqsadga erishish iqlim o'zgarishi va mojarolar keltirib chiqaradigan yangi tahdidlarga yechim topishni o'z ichiga oladi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va kutiladigan natijalar",
            "paragraphs": [
                "SDG 1ni amalga oshirish uchun 7 maqsad va taraqqiyot yo'lini belgilash uchun 13 ko'rsatkich mavjud.",
                "Yuqoridagi vazifalarni amalga oshirgandan so'ng quyidagi natijaga erishiladi:",
            ],
            "bullets": [
                "o'ta qashshoqlikni yo'q qilish",
                "barcha turdagi qashshoqliklarni yarmiga qisqartirish",
                "ijtimoiy himoya tizimlarini joriy etish",
                "mulk, asosiy xizmatlar, texnologiyalar va iqtisodiy resurslardan foydalanishga teng huquqlarni ta'minlash",
                "ekologik, iqtisodiy va ijtimoiy ofatlarga chidamlilikni oshirish",
            ],
        },
        {
            "title": "Global holat",
            "paragraphs": [
                "Taraqqiyot davom etayotganiga qaramay, dunyo aholisining 10 foizi qashshoqlikda yashaydi va sog'liqni saqlash, ta'lim, suv va kanalizatsiya kabi asosiy ehtiyojlarni qondirish uchun kurashmoqda.",
                "Haddan tashqari qashshoqlik daromadi past mamlakatlarda, ayniqsa, mojarolar va siyosiy g'alayonlardan jabrlangan mamlakatlarda hamon keng tarqalgan.",
                "2015-yilgi statistika shuni ko'rsatadiki, o'ta qashshoqlikda yashovchi 736 million aholining yarmidan ko'pi Sahroi Kabir va janubiy Afrika hududlariga to'g'ri keladi.",
                "Bunday holatda, ijtimoiy siyosat jarayonida sezilarli siljishlarsiz, 2030-yilga kelib qashshoqlik keskin ortadi.",
                "2016 yilgi statistikaga ko'ra, qishloqlarda qashshoqlik darajasi 17,2 foizni, shaharlarda esa 5,3 foizni tashkil etadi.",
            ],
        },
        {
            "title": "Qashshoqlikni o'lchash va pandemiya ta'siri",
            "paragraphs": [
                "Kambag'allikni o'lchaydigan asosiy ko'rsatkichlardan biri bu xalqaro va milliy qashshoqlik chegarasidan pastda yashaydigan aholi ulushidir.",
                "Ijtimoiy himoya tizimlari bilan qamrab olingan va asosiy xizmatlardan foydalana oladigan uy xo'jaliklarida yashovchi aholi ulushini o'lchash ham qashshoqlik darajasini ko'rsatib beruvchi ko'rsatkichlardan biridir.",
                "2020-yildagi COVID-19 pandemiyasi qashshoqlikka barham berishni qiyinlashtirdi.",
                "2020-yil sentabrida chop etilgan tadqiqot shuni ko'rsatdiki, qashshoqlik oxirgi 20 yil ichida barqaror ravishda pasayib borayotgan bo'lsa-da, bir necha oy ichida 7 foizga oshgan.",
            ],
        },
        {
            "title": "Bolalar va qashshoqlik",
            "paragraphs": [
                "Qashshoqlik bolalarni ham chetlab o'tmadi. Har yil qancha bola ochlik va muhtojlikda yashayotgani haqida statistika qilinib boriladi. Lekin bu statistikalar doim ham to'g'ri chiqavermaydi.",
                "Misol uchun, 2013-yildagi ma'lumotlarga qaraydigan bo'lsak, taxminan 385 million bola kuniga 1,90 AQSh dollaridan kam pul bilan yashagan.",
                "Dunyo bo'ylab bolalarning ahvoli to'g'risidagi to'liq ma'lumotlar mavhumligi tufayli bu raqamlar ishonchsizdir.",
                "O'rtacha 97 foiz mamlakatlarda kam ta'minlangan bolalarning ahvolini aniqlash va SDG 1ga erishish yo'llarini ishlab chiqish uchun yetarlicha ma'lumotlar yo'q.",
                "Mamlakatlarning 63 foizida esa bolalar qashshoqligi haqida hech qanday statistika yo'q.",
            ],
        },
        {
            "title": "Ijobiy siljishlar va saqlanib qolayotgan xavflar",
            "paragraphs": [
                "1990-yildan buyon dunyo mamlakatlari qashshoqlikni kamaytirish uchun turli chora-tadbirlarni amalga oshirib, samarali natijalarga erishdi.",
                "2013-yilda o'ta qashshoqlikda yashovchi odamlar soni 1,8 milliarddan 776 milliongacha kamaydi.",
                "Biroq, yuqori natijalarga qaramasadan odamlar qashshoqlikda yashashda davom etmoqda.",
                "Jahon bankining hisob-kitoblariga ko'ra, 2020-yilda 40 dan 60 milliongacha odam o'ta qashshoqlikka tushib qoladi.",
                "Dunyoning eng qashshoq mamlakatlarida iqtisodiy o'sishning yo'qligi, tengsizlikning kuchayishi, davlatchilikning tobora zaiflashib borayotgani va iqlim o'zgarishi kabi oqibatlar SDG 1ga erishishga to'sqinlik qilmoqda.",
            ],
        },
        {
            "title": "Mahalliy hukumatlarning roli",
            "paragraphs": [
                "Mahalliy hukumatlar qashshoqlik bilan bog'liq masalalarni yechishda muhim rol o'ynaydi.",
                "Butun dunyoda mahalliy hukumatni vazifalari turlicha bo'lib, quyidagi vazifalar bajaradilar:",
            ],
            "bullets": [
                "kam ta'minlanganlarning ehtiyojlarini qondirish",
                "hisobdorlik va shaffoflikni ta'minlash uchun yaxshi boshqaruv",
                "bandlikni yaxshilash uchun inklyuziv ta'limni yaxshi yo'lga qo'yish",
                "ehtiyojmand aholi va qishloq jamoalariga ta'sir ko'rsatadigan davlat korxonalarining biznes etikasi ustida ishlash",
            ],
        },
    ],
}


SDG_2_DETAIL_UZ_CLEAN = {
    "hero_title": "Ochlikka barham berish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Ochlikni tugatish, oziq-ovqat xavfsizligini ta'minlash va oziqlanishni yaxshilash hamda qishloq xo'jaligining barqaror rivojlanishiga ko'maklashish",
    "article_mode": True,
    "article_blocks": [
        {
            "type": "paragraph",
            "content": "Barqaror rivojlanishning 2-maqsadi Ochlikni tugatish, oziq-ovqat xavfsizligini ta'minlash va oziqlanishni yaxshilash hamda qishloq xo'jaligining barqaror rivojlanishiga ko'maklashish (keying o'rinlarda SDG 2 deb yuritiladi) deyiladi. SDG 2 oziq-ovqat xavfsizligi, ovqatlanish patsioniga foydali mahsulotlarni qo'shish, qishloq hayotini tubdan o'zgartirish va barqaror qishloq xo'jaligi o'rtasida uzviy o'zaro bog'liqlik borligini ko'rsatadi. Birlashgan Millatlar Tashkilotining ma'lumotlariga ko'ra, 690 millionga yaqin odam och qolmoqda, bu dunyo aholisining 10 foizdan sal kamrog'ini tashkil etadi. Har to'qqiz kishidan biri har kecha och uxlab yotadi, jumladan, hozirda Janubiy Sudan, Somali, Yaman va Nigeriyada ochlikdan o'lish xavfi ostida bo'lgan 20 million kishi borligi aytilmoqda.",
        },
        {
            "type": "paragraph",
            "content": "2-maqsadni amalga oshirish uchun 8 maqsad va taraqqiyot yo'lini belgilash uchun 14 ko'rsatkich mavjud Yuqoridagi vazifalarni amalga oshirgandan so'ng quyidagi natijaga erishiladi:",
        },
        {
            "type": "list",
            "items": [
                "ochlikni yo'q qilish va oziq-ovqat bilan ta'minlashni yaxshilash",
                "to'yib ovqatlanmaslikning barcha shakllarini yo'q qilish",
                "qishloq xo'jaligi hosildorligini oshirish",
                "barqaror oziq-ovqat ishlab chiqarish tizimlari va barqaror qishloq xo'jaligi amaliyoti kengaytirish",
                "urug'lar, ekinlar, qishloq xo'jaligi va uy hayvonlarining genetik xilma-xilligi ko'paytirish",
                "investitsiyalar, tadqiqot va texnologiya olib kirish",
            ],
        },
        {
            "type": "paragraph",
            "content": "To'yib ovqatlanmaslik darajasi ko'p yillar davomida ma'lum bir foizda kamaydi. Lekin 2015-yildan boshlab och qolish darajasini yana ortib bordi. Buning asosiy sababi, oziq-ovqat tizimlaridagi turli xil yetishmovchiliklar, iqlim o'zgarishlari, chigirtkalar invaziyasi va COVID-19 pandemiyasi hisoblanadi. Bu oqibatlar bilvosita xarid qobiliyatini, oziq-ovqat mahsulotlarini ishlab chiqarish va tarqatish qobiliyatini pasaytiradi. Bu esa aholining eng zaif qatlamlariga ta'sir qiladi va qo'shimcha ravishda ularning oziq-ovqat mahsulotlaridan foydalanishini cheklaydi. Statistik ma'lumotga ko'ra, 2020-yilda 142 milliongacha odam COVID-19 pandemiyasi natijasida to'yib ovqatlanmaslikdan aziyat chekkan. Bundan tashqari, COVID-19 pandemiyasi davrida iqtisodiy o'sish darajasi sust bo'lganligi sababli, 2020-yil oxiriga kelib, dunyoda to'yib ovqatlanmaydigan odamlarning umumiy soniga 83 dan 132 milliongacha oshdi.",
        },
        {
            "type": "paragraph",
            "content": "Bunday holatda dunyo 2030-yilga borib ocharchilikni yo'qota olmaydi. Ayniqsa, Afrikadagi aholi ochlikdan qutilishi dargumon. BRM ga a'zo davlatlarni ochlik va oziq-ovqat yetishmovchiligini yo'q qilish uchun hali ko'p ish qilish kerakligidan ogohlantiradi.",
        },
        {
            "type": "paragraph",
            "content": "2-maqsad 2030-yilga kelib to'yib ovqatlanmaslik va ochlikning barcha shakllariga barham berish va yil davomida har bir kishi, ayniqsa bolalar uchun yetarli ovqatlanishni ta'minlashni maqsad qilgan. Dunyo bo'ylab taxminan 155 million bolaga yomon ta'sir ko'rsatadigan to'yib ovqatlanmaslikdir. Bu bolalarning aqliy va jismoniy rivojlanishini sekinlashtiradi, ularda o'lim va kasallik xavfini oshiradi.",
        },
        {
            "type": "paragraph",
            "content": "2017-yil holatiga ko'ra, BMTga a'zo 202 ta davlatdan faqat 26 tasi to'yib ovqatlanmaslikni tugatish bo'yicha BRM maqsadiga erishish yo'lida ketayotgan edi. 20 foizi esa hech qanday muvaffaqiyatga erisha olmadi, deyarli 70 foizida hech qanday strategik ish amalga oshirilmagan.",
        },
        {
            "type": "paragraph",
            "content": "Noto'g'ri ovqatlanish va haddan tashqari ochlik barqaror rivojlanish yo'lidagi asosiy to'siqdir. Ikki to'siq odamlar uchun qiyinchilik tug'diradi. Och odamlar unumdorligi past bo'ladi va kasalliklarga ko'proq moyil bo'ladi. Shunday qilib, ular o'z hayotlarini yaxshilay olmaydilar. 2-maqsad dunyo aholisini saqlab qolish va hech kim hech qachon ochlikdan aziyat chekmasligini ta'minlash uchun asos yaratadi. Bu zamonaviy texnologiyalar va adolatli taqsimlash tizimlaridan foydalangan holda barqaror qishloq xo'jaligini rivojlantirish orqali amalga oshirilishi kerak. Qishloq xo'jaligidagi innovatsiyalar oziq-ovqat ishlab chiqarishni ko'paytirish va chiqindilarini kamaytirish uchun mo'ljallangan.",
        },
        {
            "type": "paragraph",
            "content": "2-maqsadda aytilishicha, 2030-yilgacha odamlar ochlik va to'yib ovqatlanmaslikning barcha shakllariga barham berish orqali oziq-ovqat xavfsizligiga erishishlari kerak. Bunga qishloq xo'jaligi mahsuldorligini va kichik oziq-ovqat ishlab chiqaruvchilarning (ayniqsa, ayollar va mahalliy xalqlar) daromadlarini ikki baravar oshirish, oziq-ovqat ishlab chiqarishning barqaror tizimlarini ta'minlash, yer va tuproq sifatini izchil yaxshilash orqali erishiladi. Qishloq xo'jaligi dunyodagi eng yirik ish beruvchi bo'lib, dunyo aholisining 40 foizini tirikchilik bilan ta'minlaydi. Bu ehtiyojmand qishloq uy xo'jaliklari uchun eng katta daromad manbai hisoblanadi. Rivojlanayotgan mamlakatlarda qishloq xo'jaligi ishchi kuchining qariyb 43%, Osiyo va Afrikaning ayrim qismlarida esa 50% dan ortig'ini ayollar tashkil qiladi. Biroq, ayollar yerning atigi 20 foiziga egalik qiladi.",
        },
    ],
}


SDG_2_DETAIL_UZ = {
    "hero_title": "Ochlikka barham berish",
    "idea_title": "Asosiy gРІР‚Вoya",
    "idea_text": "Ochlikni tugatish, oziq-ovqat xavfsizligini taРІР‚в„ўminlash va oziqlanishni yaxshilash hamda qishloq xoРІР‚Вjaligining barqaror rivojlanishiga koРІР‚Вmaklashish.",
    "sections": [
        {
            "title": "Umumiy maРІР‚в„ўlumot",
            "paragraphs": [
                "Barqaror rivojlanishning 2-maqsadi ochlikni tugatish, oziq-ovqat xavfsizligini taРІР‚в„ўminlash, oziqlanishni yaxshilash hamda qishloq xoРІР‚Вjaligining barqaror rivojlanishiga koРІР‚Вmaklashishni nazarda tutadi.",
                "SDG 2 oziq-ovqat xavfsizligi, ovqatlanish sifatini yaxshilash va qishloq xoРІР‚Вjaligi bilan barqaror iqtisodiy rivojlanish oРІР‚Вrtasidagi uzviy bogРІР‚Вliqlikni koРІР‚Вrsatadi.",
                "Birlashgan Millatlar Tashkiloti maРІР‚в„ўlumotlariga koРІР‚Вra, dunyoda yuz millionlab odamlar ochlik va toРІР‚Вyib ovqatlanmaslik xavfi ostida yashamoqda.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 2 doirasida 8 ta maqsad va 14 ta koРІР‚Вrsatkich mavjud.",
                "Mazkur vazifalarni amalga oshirish natijasida quyidagilarga erishish koРІР‚Вzda tutiladi:",
            ],
            "bullets": [
                "ochlikni yoРІР‚Вq qilish va oziq-ovqat bilan taРІР‚в„ўminlashni yaxshilash",
                "toРІР‚Вyib ovqatlanmaslikning barcha shakllarini yoРІР‚Вq qilish",
                "qishloq xoРІР‚Вjaligi hosildorligini oshirish",
                "barqaror oziq-ovqat ishlab chiqarish tizimlari va qishloq xoРІР‚Вjaligi amaliyotini kengaytirish",
                "urugРІР‚Вlar, ekinlar va uy hayvonlarining genetik xilma-xilligini koРІР‚Вpaytirish",
                "investitsiyalar, tadqiqot va texnologiyalarni keng joriy etish",
            ],
        },
        {
            "title": "Bugungi global holat",
            "paragraphs": [
                "ToРІР‚Вyib ovqatlanmaslik darajasi ayrim davrlarda kamaygan boРІР‚Вlsa-da, 2015-yildan keyin och qolish koРІР‚Вrsatkichlari yana oРІР‚Вsishni boshladi.",
                "Bunga oziq-ovqat tizimlaridagi uzilishlar, iqlim oРІР‚Вzgarishi, mojarolar va iqtisodiy beqarorlik sabab boРІР‚Вlmoqda.",
                "COVID-19 pandemiyasi esa xarid qobiliyati va mahsulot tarqatish zanjirlariga salbiy taРІР‚в„ўsir koРІР‚Вrsatib, vaziyatni keskinlashtirdi.",
            ],
        },
        {
            "title": "Xavflar va muammolar",
            "paragraphs": [
                "Dunyo 2030-yilgacha ocharchilikni toРІР‚Вliq yoРІР‚Вqotish yoРІР‚Вlida jiddiy sinovlarga duch kelmoqda.",
            ],
            "bullets": [
                "iqlim oРІР‚Вzgarishi va qurgРІР‚Вoqchilik",
                "urush va mojarolar",
                "oziq-ovqat narxlarining oshishi",
                "qishloq xoРІР‚Вjaligida texnologik orqada qolish",
                "taqsimot tizimidagi zaifliklar",
            ],
        },
        {
            "title": "Bolalar va ovqatlanish",
            "paragraphs": [
                "Bolalar orasidagi toРІР‚Вyib ovqatlanmaslik jismoniy va aqliy rivojlanishga bevosita salbiy taРІР‚в„ўsir koРІР‚Вrsatadi.",
                "Dunyoda millionlab bolalar yetarli ovqatlanmaslik tufayli sogРІР‚Вliq, taРІР‚в„ўlim va kelajakdagi iqtisodiy imkoniyatlardan mahrum boРІР‚Вlish xavfi ostida qolmoqda.",
            ],
        },
        {
            "title": "Qishloq xoРІР‚Вjaligi va rivojlanish",
            "paragraphs": [
                "Rivojlanayotgan mamlakatlarda qishloq xoРІР‚Вjaligi millionlab oilalar uchun asosiy daromad manbai hisoblanadi.",
                "Zamonaviy texnologiyalar, adolatli taqsimlash tizimlari va samarali investitsiyalar orqali oziq-ovqat ishlab chiqarishni koРІР‚Вpaytirish va chiqindilarni kamaytirish mumkin.",
                "Ayollar va kichik ishlab chiqaruvchilarni qoРІР‚Вllab-quvvatlash bu yoРІР‚Вnalishda alohida ahamiyatga ega.",
            ],
        },
        {
            "title": "Hukumatlar va institutlar roli",
            "paragraphs": [
                "Davlatlar va xalqaro institutlar SDG 2 ga erishish uchun quyidagi yoРІР‚Вnalishlarda ishlaydi:",
            ],
            "bullets": [
                "oziq-ovqat xavfsizligi siyosatini kuchaytirish",
                "mahalliy ishlab chiqaruvchilarni qoРІР‚Вllab-quvvatlash",
                "innovatsion agrotexnologiyalarni joriy etish",
                "barqaror suv va yer resurslarini boshqarish",
                "zaif qatlamlar uchun oziq-ovqat va ijtimoiy yordam dasturlarini kengaytirish",
            ],
        },
    ],
}


SDG_3_DETAIL_UZ = {
    "hero_title": "SogРІР‚Вlik va farovonlik",
    "idea_title": "Asosiy gРІР‚Вoya",
    "idea_text": "SogРІР‚Вlom turmush tarzini taРІР‚в„ўminlash va barcha yoshdagi kishilarning farovonligiga koРІР‚Вmaklashish.",
    "sections": [
        {
            "title": "Umumiy maРІР‚в„ўlumot",
            "paragraphs": [
                "Barqaror rivojlanishning 3-maqsadi sogРІР‚Вlom turmush tarzini taРІР‚в„ўminlash va barcha yoshdagi kishilarning farovonligiga koРІР‚Вmaklashishni nazarda tutadi.",
                "SDG 3 sogРІР‚Вlom turmush tarzining turli jihatlarini qamrab oladi va unga doimiy eРІР‚в„ўtibor qaratadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va koРІР‚Вrsatkichlar",
            "paragraphs": [
                "SDG 3ni amalga oshirish uchun 13 maqsad va taraqqiyot yoРІР‚Вlini belgilash uchun 28 koРІР‚Вrsatkich mavjud.",
                "Birinchi 9 maqsad РІР‚Сљmaqsadli natijalarРІР‚Сњ boРІР‚Вlib, ularga quyidagilar kiradi:",
            ],
            "bullets": [
                "onalar oРІР‚Вlimini kamaytirish",
                "yangi tugРІР‚Вilgan chaqaloqlar va besh yoshgacha boРІР‚Вlgan bolalar oРІР‚Вlimini kamaytirish",
                "yuqumli kasalliklarga qarshi kurashish",
                "yuqumli boРІР‚Вlmagan kasalliklardan oРІР‚Вlimni kamaytirish va ruhiy salomatlikni yaxshilash",
                "giyohvandlikning oldini olish va davolash",
                "yoРІР‚Вl-transport hodisalarida jarohatlar va oРІР‚Вlimlarni kamaytirish",
                "jinsiy va reproduktiv salomatlik xizmatlaridan foydalanishni kengaytirish",
                "umumiy sogРІР‚Вliqni saqlash qamroviga erishish",
                "xavfli kimyoviy moddalardan kasallanish va oРІР‚Вlimni kamaytirish",
            ],
        },
        {
            "title": "Erishish vositalari",
            "paragraphs": [
                "SDG 3 maqsadlarining qolgan toРІР‚Вrttasi erishish vositalari boРІР‚Вlib, ular quyidagi yoРІР‚Вnalishlarni qamrab oladi:",
            ],
            "bullets": [
                "tamaki nazorati boРІР‚Вyicha xalqaro konvensiyalarni amalga oshirish",
                "tadqiqot, dori vositalari va vaksinalardan universal foydalanishni qoРІР‚Вllab-quvvatlash",
                "rivojlanayotgan mamlakatlarda sogРІР‚Вliqni saqlashni moliyalashtirish va tizimni mustahkamlash",
                "global sogРІР‚Вliq xavflari boРІР‚Вyicha erta ogohlantirish tizimlarini takomillashtirish",
            ],
        },
        {
            "title": "Global sogРІР‚Вliq kun tartibi",
            "paragraphs": [
                "SDG 3 barcha erkaklar va ayollar uchun tibbiy xizmatlardan teng foydalanishni taРІР‚в„ўminlaydigan universal tibbiy qamrovga erishishga qaratilgan.",
                "U yangi tugРІР‚Вilgan chaqaloqlar, besh yoshgacha boРІР‚Вlgan bolalar oРІР‚Вlimining oldini olish va epidemiyalarni tugatish bilan birga iqtisodiy hamda ijtimoiy tengsizlik, urbanizatsiya, iqlim inqirozi va boshqa yuqumli kasalliklar xavfiga ham eРІР‚в„ўtibor qaratadi.",
                "2030-yil kun tartibidagi asosiy masala salomatlikka eРІР‚в„ўtiborni oshirish boРІР‚Вlib, COVID-19 pandemiyasi hisobga olinganda global miqyosda salomatlik va farovonlikni taРІР‚в„ўminlashga jiddiy eРІР‚в„ўtibor qaratish zarur.",
            ],
        },
        {
            "title": "Bolalar salomatligi",
            "paragraphs": [
                "Har bir bolaning omon qolishi va rivojlanishini taРІР‚в„ўminlash yuqori taРІР‚в„ўsirli chora-tadbirlarni koРІР‚Вrishni talab qiladi.",
                "Bunga yangi tugРІР‚Вilgan chaqaloqlarni sifatli prenatal, tugРІР‚Вruq va tugРІР‚Вruqdan keyingi parvarish bilan qamrab olish, yuqumli kasalliklardan himoya qilish hamda yetarli va toРІР‚Вyimli oziq-ovqatdan foydalanish imkoniyatini kengaytirish kiradi.",
            ],
        },
        {
            "title": "Asosiy statistika va xavflar",
            "paragraphs": [
                "UNDP maРІР‚в„ўlumotlariga koРІР‚Вra, har 2 soniyada 30 yoshdan 70 yoshgacha boРІР‚Вlgan bir kishi yurak-qon tomir kasalliklari, surunkali nafas yoРІР‚Вllari kasalliklari, diabet yoki saraton kabi yuqumli boРІР‚Вlmagan kasalliklardan bevaqt vafot etadi.",
                "Dunyo boРІР‚Вylab 2019-yilda 2.4 million chaqaloq bevaqt vafot etgan, kuniga taxminan 6,700 neonatal oРІР‚Вlim qayd etilgan.",
                "OРІР‚Вrtacha umr koРІР‚Вrish davomiyligini oshirish va ona-bola salomatligini yaxshilash borasida sezilarli yutuqlar boРІР‚Вlsa-da, koРІР‚Вplab mamlakatlarda bu maqsadlarga erishish uchun hali jiddiy ishlar talab etiladi.",
            ],
        },
        {
            "title": "Kelajak uchun ustuvor yoРІР‚Вnalishlar",
            "paragraphs": [
                "Onalar oРІР‚Вlimini kamaytirish, toza suv va sanitariya xizmatlaridan foydalanishni kengaytirish, bezgak, sil, poliomiyelit va OIV/OITS tarqalishini qisqartirish SDG 3ning muhim yoРІР‚Вnalishlari boРІР‚Вlib qolmoqda.",
                "Internet va texnologiyalarning rivojlanishi tibbiy yozuvlarni raqamlashtirish, shifokorlar va tibbiyot xodimlari uchun onlayn resurslardan foydalanish imkonini kengaytirib, bemorlarni parvarish qilish va natijalarni yaxshilashga xizmat qilmoqda.",
            ],
        },
    ],
}


SDG_3_DETAIL_UZ_CLEAN = {
    "hero_title": "Sog'liq va farovonlik",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Sog'lom turmush tarzini ta'minlash va barcha yoshdagi kishilarning farovonligiga ko'maklashish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 3-maqsadi sog'lom turmush tarzini ta'minlash va barcha yoshdagi kishilarning farovonligiga ko'maklashishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 3 deb yuritiladi.",
                "SDG 3 sog'lom turmushning turli jihatlarini qamrab oladi. Unda onalar salomatligi, bolalar omon qolishi, yuqumli va yuqumli bo'lmagan kasalliklar, ruhiy salomatlik hamda sifatli tibbiy xizmatlardan teng foydalanish masalalari markaziy o'rin tutadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va ko'rsatkichlar",
            "paragraphs": [
                "SDG 3 ni amalga oshirish uchun 13 maqsad va 28 ta ko'rsatkich belgilangan. Birinchi 9 tasi natijaviy maqsadlar bo'lib, ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "onalar o'limini kamaytirish",
                "yangi tug'ilgan chaqaloqlar va 5 yoshgacha bo'lgan bolalar o'limini kamaytirish",
                "yuqumli kasalliklarga qarshi kurashish",
                "yuqumli bo'lmagan kasalliklardan o'limni kamaytirish va ruhiy salomatlikni yaxshilash",
                "giyohvandlikning oldini olish va davolash",
                "yo'l-transport hodisalari oqibatidagi o'lim va jarohatlarni kamaytirish",
                "jinsiy va reproduktiv salomatlik xizmatlaridan foydalanishni kengaytirish",
                "umumiy sog'liqni saqlash qamroviga erishish",
                "xavfli kimyoviy moddalar va ifloslanish oqibatidagi kasallanishni kamaytirish",
            ],
        },
        {
            "title": "Amalga oshirish vositalari",
            "paragraphs": [
                "SDG 3 maqsadlarining qolgan to'rttasi uni amalga oshirish vositalari bo'lib, sog'liqni saqlash tizimining barqarorligini mustahkamlashga xizmat qiladi.",
            ],
            "bullets": [
                "JSSTning tamaki nazorati bo'yicha xalqaro konvensiyalarini amalga oshirish",
                "tadqiqot, dori vositalari va vaksinalardan universal foydalanishni qo'llab-quvvatlash",
                "rivojlanayotgan mamlakatlarda sog'liqni saqlashni moliyalashtirish va tizimni mustahkamlash",
                "global sog'liq xavflari bo'yicha erta ogohlantirish tizimlarini takomillashtirish",
            ],
        },
        {
            "title": "Global holat va dolzarb muammolar",
            "paragraphs": [
                "SDG 3 barcha erkaklar va ayollar uchun tibbiy xizmatlardan teng foydalanishni ta'minlaydigan universal tibbiy qamrovga erishishga qaratilgan. U yangi tug'ilgan chaqaloqlar va 5 yoshgacha bo'lgan bolalar o'limining oldini olish, epidemiyalarni tugatish, iqtisodiy va ijtimoiy tengsizlik, urbanizatsiya hamda iqlim inqirozi bilan bog'liq xavflarga ham e'tibor qaratadi.",
                "2030-yil kun tartibidagi asosiy masalalardan biri salomatlik va farovonlikni ta'minlashdir. COVID-19 pandemiyasi global sog'liq tizimlari qanchalik sezgir ekanini ko'rsatib berdi va bu yo'nalishda jiddiy investitsiyalar zarurligini yana bir bor tasdiqladi.",
            ],
        },
        {
            "title": "Bolalar va onalar salomatligi",
            "paragraphs": [
                "Har bir bolaning omon qolishi va rivojlanishini ta'minlash yuqori ta'sirli chora-tadbirlarni talab qiladi. Bunga sifatli prenatal, tug'ruq va tug'ruqdan keyingi parvarish, immunizatsiya, yuqumli kasalliklardan himoya qilish hamda yetarli va to'yimli oziq-ovqatdan foydalanish imkoniyatini kengaytirish kiradi.",
                "Onalar o'limini kamaytirish ham ushbu maqsadning eng muhim yo'nalishlaridan biridir. Malakali tibbiy yordam, shoshilinch akusherlik xizmati va ayollar salomatligi bo'yicha xabardorlikni oshirish bu jarayonda hal qiluvchi omil hisoblanadi.",
            ],
        },
        {
            "title": "Asosiy statistika va xavflar",
            "paragraphs": [
                "UNDP ma'lumotlariga ko'ra, har 2 soniyada 30 yoshdan 70 yoshgacha bo'lgan bir kishi yurak-qon tomir kasalliklari, surunkali nafas yo'llari xastaliklari, diabet yoki saraton kabi yuqumli bo'lmagan kasalliklar sababli bevaqt vafot etadi.",
                "Dunyo bo'ylab 2019-yilda 2.4 million chaqaloq bevaqt vafot etgan va kuniga taxminan 6 700 ta neonatal o'lim qayd etilgan. O'rtacha umr ko'rish davomiyligi oshayotganiga qaramay, ko'plab mamlakatlarda ona-bola salomatligi bo'yicha SDG ko'rsatkichlariga erishish uchun hali katta ishlar talab etiladi.",
            ],
        },
        {
            "title": "Kelajak uchun ustuvor yo'nalishlar",
            "paragraphs": [
                "Onalar o'limini kamaytirish, toza suv va sanitariya xizmatlaridan foydalanishni kengaytirish, bezgak, sil, poliomiyelit va OIV/OITS tarqalishini qisqartirish SDG 3ning ustuvor yo'nalishlari bo'lib qolmoqda.",
                "Raqamli texnologiyalar, elektron tibbiy yozuvlar va onlayn tibbiy resurslar esa sog'liqni saqlash tizimining samaradorligini oshirib, bemorlar parvarishini yaxshilashga xizmat qilmoqda.",
            ],
        },
    ],
}

SDG_4_DETAIL_UZ_CLEAN = {
    "hero_title": "Sifatli ta'lim",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Barchani qamrab oluvchi, teng huquqli hamda sifatli ta'limni ta'minlash va barcha uchun uzluksiz ta'lim olish imkoniyatini kengaytirish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 4-maqsadi barchani qamrab oluvchi, teng huquqli hamda sifatli ta'limni ta'minlash va barcha uchun uzluksiz ta'lim olish imkoniyatini kengaytirishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 4 deb yuritiladi.",
                "SDG 4 ni amalga oshirish uchun 10 ta maqsad va taraqqiyot yo'lini belgilash uchun 11 ta ko'rsatkich mavjud. Birinchi 7 ta maqsad natijaga asoslangan maqsadlar bo'lib, ular ta'limning barcha bosqichlarida sifat va tenglikni ta'minlashni ko'zda tutadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 4 doirasida quyidagi yo'nalishlarga alohida e'tibor qaratiladi:",
            ],
            "bullets": [
                "bepul boshlang'ich va o'rta ta'limdan foydalanish imkoniyati",
                "sifatli maktabgacha ta'limdan teng foydalanish",
                "texnikum, kasb-hunar va oliy ta'lim imkoniyatlarini kengaytirish",
                "mehnat bozorida muvaffaqiyatga erishish uchun zarur ko'nikmalarga ega shaxslar sonini ko'paytirish",
                "ta'lim sohasidagi har qanday kamsitishlarga barham berish",
                "umumiy savodxonlik va hisoblash qobiliyatini shakllantirish",
                "barqaror rivojlanish va fuqarolik ta'limidan foydalanish imkoniyatini yaratish",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Sifatli ta'limga erishish uchun faqat o'quv dasturlarini yangilash yetarli emas. Ta'lim muhitini xavfsiz, inklyuziv va zamonaviy qilish bo'yicha tizimli yondashuv talab etiladi.",
            ],
            "bullets": [
                "inklyuziv va xavfsiz maktablarni qurish hamda modernizatsiya qilish",
                "rivojlanayotgan mamlakatlar uchun oliy ta'lim stipendiyalarini kengaytirish",
                "malakali o'qituvchilar sonini oshirish va ularni muntazam tayyorlash",
            ],
        },
        {
            "title": "Tenglik va kirish imkoniyati",
            "paragraphs": [
                "SDG 4 bolalar va yoshlarning sifatli, oson va teng ta'lim olishiga e'tibor beradi. Maqsadlardan yana biri umumiy savodxonlikka erishish bo'lib, bu bilim va amaliy ko'nikmalarning keng ommaga yetib borishini anglatadi.",
                "O'ta qashshoqlik, qo'zg'olonlar, mojarolar va boshqa omillar ko'plab rivojlanayotgan mamlakatlarda ta'lim tizimining izchil rivojlanishini sekinlashtiradi. Ehtiyojmand oilalar farzandlari ko'pincha tengdoshlarga qaraganda maktabni tark etish xavfiga ko'proq duch keladi.",
                "Qishloq va shahar hududlari o'rtasidagi nomutanosiblik ham ta'limda tengsizlikni kuchaytiradi. Ayrim hududlarda maktabga qatnashish ko'rsatkichlari sezilarli darajada yaxshilangan bo'lsa-da, oradagi tafovutlar hanuz saqlanib qolmoqda.",
            ],
        },
        {
            "title": "Ta'lim tizimini takomillashtirish",
            "paragraphs": [
                "Ta'lim hamma uchun tamoyili asosida dunyo bo'ylab ta'lim tizimini takomillashtirish bo'yicha keng qamrovli ishlar olib borilmoqda. 1990-yildan boshlab ta'limda xalqaro rivojlanish kurslariga e'tibor kuchaydi va BRM doirasida SDG 4 ta'limni barqaror rivojlanish, davlat qurilishi va tinchlik uchun muhim vosita sifatida mustahkamladi.",
                "O'qish, yozish va hisoblash kabi ko'nikmalarga ega bo'lish bolalar va yoshlarning kelajak imkoniyatlarini sezilarli kengaytiradi. Globallashuv va texnologik o'zgarishlar sharoitida ta'lim faqat maktabga qatnashish bilan emas, balki zamonaviy ko'nikmalarni egallash bilan ham o'lchanadi.",
                "Shu bois SDG 4 ning asosiy maqsadi o'quvchilar hayot sifatini va jamiyat kelajagini yaxshilaydigan inklyuziv, sifatli ta'lim tizimini yaratishdan iborat.",
            ],
        },
        {
            "title": "COVID-19 va ta'limga ta'siri",
            "paragraphs": [
                "COVID-19 pandemiyasi ta'lim tizimiga jiddiy salbiy ta'sir ko'rsatdi. 2020-yilda maktablarning ommaviy yopilishi dunyo bo'ylab o'quv natijalarini pasaytirdi va milliardlab bolalar hamda yoshlarni ta'lim olish imkoniyatidan vaqtincha mahrum qildi.",
                "Masofaviy ta'limga o'tish jarayonida ko'plab oilalarda internet, qurilma va texnologik imkoniyatlar yetishmadi. Bu ayniqsa kam ta'minlangan qatlamlar uchun ta'limdagi nomutanosiblikni yanada kuchaytirdi.",
                "Pandemiya shuni ko'rsatdiki, sifatli ta'limga erishish uchun raqamli infratuzilma, o'qituvchilarni tayyorlash va moslashuvchan o'quv tizimlari zarur.",
            ],
        },
    ],
}

SDG_5_DETAIL_UZ_CLEAN = {
    "hero_title": "Gender tengligi",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Gender tengligini ta'minlash, barcha ayol va qiz bolalarning huquq va imkoniyatlarini kengaytirish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 5-maqsadi gender tengligini ta'minlash va barcha ayollar hamda qiz bolalarning huquq va imkoniyatlarini kengaytirishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 5 deb yuritiladi.",
                "Barqaror rivojlanish maqsadlari o'zaro chambarchas bog'liq bo'lib, gender tengligi ham ijtimoiy, iqtisodiy va ekologik barqarorlikning asosiy tayanchlaridan biri hisoblanadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va ko'rsatkichlar",
            "paragraphs": [
                "SDG 5 ni amalga oshirish uchun 9 maqsad va 14 ko'rsatkich belgilangan. Birinchi 6 ta maqsad natijaga yo'naltirilgan maqsadlar bo'lib, ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "hamma joyda barcha ayollar va qizlarga nisbatan kamsitishning barcha shakllarini tugatish",
                "ayollar va qizlarning zo'ravonligi, ekspluatatsiyasi va tazyiqlariga chek qo'yish",
                "erta va majburiy nikoh, ayollar jinsiy a'zolarini kesish kabi zararli amaliyotlarga barham berish",
                "tug'ruqdan keyingi bolalarni parvarish qilish qiymatini oshirish va onalarni har tomonlama rag'batlantirish",
                "xotin-qizlarning yetakchilik va qarorlar qabul qilishdagi to'liq ishtirokini ta'minlash",
                "universal reproduktiv huquq va salomatlik xizmatlaridan foydalanishni kengaytirish",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Gender tengligiga erishish tizimli va uzoq muddatli siyosatni talab qiladi. SDG 5 doirasida quyidagi vositalar muhim hisoblanadi:",
            ],
            "bullets": [
                "ayollarning iqtisodiy resurslar, mulk va moliyaviy xizmatlarga teng huquqlarini ta'minlash",
                "texnologiyalar orqali ayollarning imkoniyatlarini kengaytirishga ko'maklashish",
                "gender tengligi bo'yicha siyosatni qabul qilish, kuchaytirish va qonunchilikni amalda oshirish",
            ],
        },
        {
            "title": "Global holat va dolzarb muammolar",
            "paragraphs": [
                "Р’В«Hech kimni ortda qoldirmaslikР’В» tamoyili asosida davlatlar eng uzoqda qolayotgan hududlar va ijtimoiy qatlamlar uchun taraqqiyotni tezlashtirish majburiyatini oldilar. Bu gender tengligiga erishish va barcha ayol-qizlarning imkoniyatlarini kengaytirish uchun alohida ahamiyatga ega.",
                "Barqaror rivojlanish maqsadlari BMT tomonidan belgilangan 17 ta global maqsaddan iborat bo'lib, gender tengligi ularning ko'pchiligiga bevosita ta'sir qiladi. Bu qashshoqlik, ochlik, sog'liqni saqlash, ta'lim, iqlim o'zgarishi va ijtimoiy adolat bilan chambarchas bog'langan yo'nalishdir.",
            ],
        },
        {
            "title": "COVID-19 va ayollar holati",
            "paragraphs": [
                "COVID-19 pandemiyasi ayollar va qizlarga salbiy ta'sir ko'rsatdi. Himoya, sog'liqni saqlash va iqtisodiy imkoniyatlar cheklangani sababli ko'plab hududlarda ayollarga nisbatan zo'ravonlik va ijtimoiy bosim kuchaydi.",
                "Pandemiya davridagi ma'lumotlar ayollarning norasmiy mehnat, parvarishlash ishlari va oilaviy mas'uliyat yukining ortganini ko'rsatdi. Bu esa ularning ta'lim, bandlik va yetakchilikdagi ishtirokini qiyinlashtirdi.",
            ],
        },
        {
            "title": "Ta'lim, iqtisodiyot va yetakchilik",
            "paragraphs": [
                "Ayollar va qizlarning ta'lim olishi, sog'lig'ini saqlashi, munosib mehnat, siyosiy hamda iqtisodiy qarorlarni qabul qilish jarayonlarida teng ishtiroki barqaror iqtisodiyotga, ijtimoiy taraqqiyotga va butun insoniyat farovonligiga hissa qo'shadi.",
                "Gender tengligiga erishish yo'lida huquqiy, ijtimoiy va iqtisodiy to'siqlarni, jumladan raqamli imkoniyatlardan foydalanishdagi tafovutlarni kamaytirish ham muhim vazifa bo'lib qolmoqda.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "2030-yilgacha gender tengligiga erishish ayollar huquqlariga putur yetkazuvchi kamsitishning asosiy sabablarini bartaraf etish, gender asosidagi zo'ravonlikka barham berish va inson huquqlarini to'liq ta'minlashni talab qiladi.",
                "Bu yo'lda ta'lim tizimi, mehnat bozori, sog'liqni saqlash va raqamli texnologiyalar sohasida ayollar va qizlar uchun teng imkoniyatlarni yaratish asosiy vazifa bo'lib qoladi.",
            ],
        },
    ],
}

SDG_6_DETAIL_UZ_CLEAN = {
    "hero_title": "Toza suv va sanitariya",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Suv resurslarining mavjudligi, ulardan oqilona foydalanish va har bir insonning sanitariya vositalaridan foydalanish imkoniyatini ta'minlash.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 6-maqsadi barcha uchun toza ichimlik suvi va sanitariya xizmatlaridan foydalanishni ta'minlash hamda suv resurslarini barqaror boshqarishga qaratilgan.",
                "Mazkur maqsad nafaqat ichimlik suvi bilan ta'minlash, balki oqava suvlarni tozalash, sanitariya infratuzilmasini rivojlantirish va suvdan oqilona foydalanish madaniyatini shakllantirishni ham o'z ichiga oladi.",
            ],
        },
        {
            "title": "Universitet tajribasi va tashabbuslar",
            "paragraphs": [
                "O'tgan yillar davomida Qarshi davlat universiteti suvdan samarali foydalanishga ko'maklashish va aholining suvni tejash bo'yicha xabardorligini oshirishga qaratilgan ko'plab tashabbuslarni amalga oshirdi.",
                "Keng qamrovli targ'ibot va amaliy dasturlar orqali universitet talabalar hamda keng jamoatchilikka suv sarfini kamaytirish, resurslarni asrash va barqaror suv boshqaruvi tamoyillarini tushuntirib bordi.",
            ],
        },
        {
            "title": "Suv tanqisligi va moslashuv",
            "paragraphs": [
                "Suv tanqisligi bilan bog'liq xavflarga javoban universitet kampus bo'ylab qurg'oqchilikka chidamli o'simliklarni joriy qildi. Minimal suv talab qiladigan ushbu yashil hududlar obodonlashtirish uchun namunaviy yechim bo'lib xizmat qildi.",
                "Bu yondashuv qimmatbaho suv resurslarini asrashga yordam berish bilan birga, talabalar va xodimlar uchun ham ekologik mas'uliyat madaniyatini mustahkamladi.",
            ],
        },
        {
            "title": "Oqava suvlarni boshqarish",
            "paragraphs": [
                "Universitet oqava suvlarni boshqarish sohasida ham muhim yutuqlarga erishdi. Oqava suvlarni biologik tozalashning zamonaviy usullari orqali atrof-muhitga salbiy ta'sirni kamaytirish va suvni xavfsiz qayta ishlash bo'yicha innovatsion yechimlar sinovdan o'tkazildi.",
                "Bunday amaliyotlar nafaqat kampus barqarorligini kuchaytiradi, balki talabalar va o'qituvchilar uchun tadqiqot, tajriba va o'rganish imkoniyatlarini ham kengaytiradi.",
            ],
        },
        {
            "title": "Talabalar va jamoatchilik ishtiroki",
            "paragraphs": [
                "Qarshi davlat universiteti qoshidagi ekologik to'garaklar va talabalar guruhi ushbu yo'nalishda muhim rol o'ynaydi. Ular suv ifloslanishining oldini olish, ekologik toza amaliyotlarni targ'ib qilish va suvni tejashga qaratilgan aksiyalarni tashkil etib keladi.",
                "Talabalarning faol ishtiroki universitet jamoasida ekologik boshqaruv va ijtimoiy mas'uliyat madaniyatini rivojlantirishga xizmat qiladi.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "SDG 6 ga erishish uchun suv resurslaridan oqilona foydalanish, sanitariya infratuzilmasini yangilash, oqava suvlarni qayta ishlash va ekologik ta'limni kuchaytirish bo'yicha izchil siyosat olib borish zarur.",
                "Universitet darajasida esa ilmiy tadqiqotlar, kampus boshqaruvi va jamoatchilik bilan ishlash faoliyatlari suv xavfsizligi masalasini hal etishda muhim o'rin tutadi.",
            ],
        },
    ],
}

SDG_7_DETAIL_UZ_CLEAN = {
    "hero_title": "Arzon va toza energiya",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Barcha uchun energiyaning arzon, ishonchli, barqaror va zamonaviy manbalaridan foydalanish imkoniyatini ta'minlash.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 7-maqsadi barcha uchun energiyaning arzon, ishonchli, barqaror va zamonaviy manbalaridan foydalanish imkoniyatini ta'minlashga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 7 deb yuritiladi.",
                "Ushbu maqsad energiyadan foydalanish farovonligi, iqtisodiy rivojlanish va qashshoqlikka qarshi kurashish uchun juda muhim ustun hisoblanadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 7 ni amalga oshirish uchun 5 ta maqsad va taraqqiyot yo'lini belgilash uchun 6 ta ko'rsatkich mavjud. 5 maqsaddan 3 tasi yakuniy maqsadlar bo'lib, ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "zamonaviy energiyadan universal foydalanish",
                "qayta tiklanadigan energiya manbalarining global ulushini oshirish",
                "energiya samaradorligini ikki baravar oshirish",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Qolgan ikki maqsadga erishish uchun vosita sifatida quyidagi yo'nalishlar muhim hisoblanadi:",
            ],
            "bullets": [
                "tadqiqot, texnologiya va toza energiyaga sarmoya kiritishni rag'batlantirish",
                "rivojlanayotgan mamlakatlar uchun energiya xizmatlarini kengaytirish va modernizatsiya qilish",
            ],
        },
        {
            "title": "Global vaziyat va iqlim bilan bog'liqlik",
            "paragraphs": [
                "2019-yilgi hisobotga ko'ra, dunyo SDG 7 ga erishish yo'lida harakat qilmoqda, biroq 2030-yilgacha hozirgi rivojlanish sur'atlarida maqsadlarga to'liq erishish mushkul bo'lib qolmoqda.",
                "SDG 7 va iqlim o'zgarishini yumshatish bo'yicha maqsadlar bir-biri bilan chambarchas bog'liq. Uzoq muddatli iqlim barqarorligiga erishish uchun dunyo qayta tiklanadigan energiya bilan ko'proq ishlashi kerak.",
            ],
        },
        {
            "title": "Energiya va taraqqiyot",
            "paragraphs": [
                "Energiyadan foydalanish insoniyat sivilizatsiyasining rivojlanishini anglatadi. Sanoat inqilobidan boshlab ko'mir, neft va gaz kabi yoqilg'ilarga tayanish kuchaydi, bu esa iqtisodiy o'sish bilan birga atrof-muhitga salbiy ta'sirni ham kuchaytirdi.",
                "Bugungi kunda energiya masalasi iqlim o'zgarishi, oziq-ovqat xavfsizligi, sog'liqni saqlash, ta'lim, bandlik, transport va barqaror shaharlar kabi ko'plab sohalarning markaziy masalalaridan biri bo'lib qolmoqda.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Dunyo aholisi o'sishda davom etar ekan, elektr energiyasini sotib olishga qodir bo'lganlar va imkoniyati yo'q qatlamlar o'rtasidagi tafovut ham oshib bormoqda. Shu sababli toza energiyani eng chekka hududlargacha yetkazish muhim vazifaga aylandi.",
                "SDG 7 ga erishish uchun qayta tiklanadigan energiya manbalarini kengaytirish, energiya infratuzilmasini modernizatsiya qilish va iqlim bo'yicha xalqaro majburiyatlarni izchil amalga oshirish zarur.",
            ],
        },
    ],
}

SDG_9_DETAIL_UZ_CLEAN = {
    "hero_title": "Munosib ish o'rinlari va iqtisodiy o'sish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Keng qamrovli va barqaror iqtisodiy o'sish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini ta'minlashga ko'maklashish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 8-maqsadi keng qamrovli va barqaror iqtisodiy o'sish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini ta'minlashga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 8 deb yuritiladi.",
                "SDG 8 ni amalga oshirish uchun 12 maqsad va taraqqiyot yo'lini belgilash uchun 17 ko'rsatkich mavjud.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va ko'rsatkichlar",
            "paragraphs": [
                "Birinchi o'ntalik maqsadlar maqsadli natijalar sifatida qaraladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "barqaror iqtisodiy o'sish",
                "iqtisodiy samaradorlikni oshirish uchun diversifikatsiya, innovatsiyalar va modernizatsiya",
                "ish o'rinlari yaratish va korxonalar o'sishini qo'llab-quvvatlash siyosatini rag'batlantirish",
                "iste'mol va ishlab chiqarishda resurslardan foydalanish samaradorligini oshirish",
                "to'liq bandlik va teng haq to'lanadigan munosib mehnat",
                "bandlikka ko'maklashish",
                "yoshlarni ta'lim va tarbiyalash",
                "zamonaviy qullik, odam savdosi va bolalar mehnatiga barham berish",
                "mehnat huquqlarini himoya qilish va xavfsiz mehnat muhitini yaratish",
                "sog'lom va barqaror turizmni rivojlantirish, bank, sug'urta va moliyaviy xizmatlardan hamma teng foydalanishini ta'minlash",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Qolgan ikki maqsad yutuq vositalari hisoblanadi va ular quyidagilardan iborat:",
            ],
            "bullets": [
                "savdoni rivojlantirish uchun yordam hajmini oshirish",
                "yoshlar bandligining global strategiyasini ishlab chiqish",
            ],
        },
        {
            "title": "Global iqtisodiy holat",
            "paragraphs": [
                "Dunyo aholisining qariyb yarmi hali ham kuniga taxminan 2 AQSh dollari ekvivalentida yashaydi. Ko'p joylarda ish bilan band bo'lish qashshoqlikdan xalos bo'lishni kafolatlamaydi.",
                "2018-yilda aholi jon boshiga real YalMning global o'sish sur'ati 2 foizni tashkil etdi. Kam rivojlangan mamlakatlar uchun esa bu ko'rsatkich 2018-yilda 4,5 foizni, 2019-yilda 4,8 foizni tashkil etdi, biroq bu SDG 8 da ko'zda tutilgan 7 foizlik o'sish sur'atidan kamroq edi.",
            ],
        },
        {
            "title": "Inqirozlar va bandlik bozori",
            "paragraphs": [
                "COVID-19 pandemiyasi dunyoni Buyuk Depressiyadan keyingi eng yomon global iqtisodiy inqirozga olib keldi.",
                "2008-yilgi iqtisodiy inqiroz va global retsessiyaning uzoq davom etgan ta'siriga qaramay, bir muddat davomida rivojlanayotgan mamlakatlarda bandlikning o'sishi kuzatilgan bo'lsa-da, so'nggi yillarda o'sish sur'atlari sekinlashdi va tengsizlik kuchaydi.",
                "2008-yildan beri bandlikning o'sishi yiliga o'rtacha 0,1 foizni tashkil etib, 2000 va 2007-yillardagi 0,9 foizlik ko'rsatkichdan ancha past bo'ldi. Barcha xodimlarning 60 foizdan ortig'i mehnat shartnomasiga ega emas.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "SDG 8 irqi va jinsidan qat'i nazar barcha ishchilar uchun barqaror va adolatli iqtisodiy o'sishni rag'batlantirishga qaratilgan. Bu diversifikatsiya, texnologik yangilash va innovatsiyalar, jumladan yuqori qo'shilgan qiymatga ega va mehnatni ko'p talab qiluvchi tarmoqlarga e'tibor qaratish orqali iqtisodiy samaradorlikni oshirishni anglatadi.",
                "Kelgusida ish o'rinlarini ko'paytirish, yoshlar va ayollar bandligini kuchaytirish, xavfsiz mehnat muhitini yaratish va ijtimoiy himoyani mustahkamlash ushbu maqsadga erishishning asosiy yo'nalishlari bo'lib qoladi.",
            ],
        },
    ],
}

SDG_8_DETAIL_UZ_CLEAN = {
    "hero_title": "Munosib ish oРІР‚Вrinlari va iqtisodiy oРІР‚Вsish",
    "idea_title": "Asosiy gРІР‚Вoya",
    "idea_text": "Keng qamrovli va barqaror iqtisodiy oРІР‚Вsish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini taРІР‚в„ўminlashga koРІР‚Вmaklashish.",
    "sections": [
        {
            "title": "Umumiy maРІР‚в„ўlumot",
            "paragraphs": [
                "Barqaror rivojlanishning 8-maqsadi keng qamrovli va barqaror iqtisodiy oРІР‚Вsish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini taРІР‚в„ўminlashga koРІР‚Вmaklashishga qaratilgan. Keyingi oРІР‚Вrinlarda bu maqsad SDG 8 deb yuritiladi.",
                "SDG 8 ni amalga oshirish uchun 12 maqsad va taraqqiyot yoРІР‚Вlini belgilash uchun 17 ta koРІР‚Вrsatkich mavjud.",
            ],
        },
        {
            "title": "Asosiy maqsadlar",
            "paragraphs": [
                "Birinchi oРІР‚Вntalik maqsadlar maqsadli natijalar deb yuritiladi va ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "barqaror iqtisodiy oРІР‚Вsish",
                "iqtisodiy samaradorlikni oshirish uchun diversifikatsiya, innovatsiyalar va modernizatsiya",
                "ish oРІР‚Вrinlari yaratish va korxonalar oРІР‚Вsishini qoРІР‚Вllab-quvvatlash siyosatini ragРІР‚Вbatlantirish",
                "isteРІР‚в„ўmol va ishlab chiqarishda resurslardan foydalanish samaradorligini oshirish",
                "toРІР‚Вliq bandlik va teng haq toРІР‚Вlanadigan munosib mehnat",
                "bandlikka koРІР‚Вmaklashish",
                "yoshlarni taРІР‚в„ўlim va tarbiyalash",
                "zamonaviy qullik, odam savdosi va bolalar mehnatiga barham berish",
                "mehnat huquqlarini himoya qilish va xavfsiz mehnat muhitini yaratish",
                "sogРІР‚Вlom va barqaror turizmni rivojlantirish, bank, sugРІР‚Вurta va moliyaviy xizmatlardan hamma teng foydalanishi",
            ],
        },
        {
            "title": "Yutuq vositalari",
            "paragraphs": [
                "Bundan tashqari, qolgan ikki maqsad yutuq vositalari hisoblanadi va ular quyidagilarni oРІР‚Вz ichiga oladi:",
            ],
            "bullets": [
                "savdoni rivojlantirish uchun yordam berish hajmini oshirish",
                "yoshlar bandligining global strategiyasini ishlab chiqish",
            ],
        },
        {
            "title": "Global holat va iqtisodiy xatarlar",
            "paragraphs": [
                "Mazkur maqsad har bir mamlakatning iqtisodiy sektoridan, irqi va madaniyatidan qatРІР‚в„ўi nazar, fuqarolarning yaxshi hayot uchun zarur ehtiyojlarini taРІР‚в„ўminlashga qaratilgan. Dunyo aholisining qariyb yarmi hali ham kuniga taxminan 2 AQSh dollari ekvivalenti bilan yashaydi.",
                "KoРІР‚Вp joylarda ish bilan band boРІР‚Вlish qashshoqlikdan xalos boРІР‚Вlishni kafolatlamaydi. NotoРІР‚ВgРІР‚Вri taraqqiyot va nomutanosib iqtisodiy siyosat qashshoqlikni bartaraf etishga toРІР‚Вsqinlik qilishi mumkin.",
                "COVID-19 pandemiyasi esa dunyoni Buyuk Depressiyadan keyingi eng yomon global iqtisodiy inqirozlardan biriga olib keldi va oРІР‚Вsish surРІР‚в„ўatlariga salbiy taРІР‚в„ўsir koРІР‚Вrsatdi.",
            ],
        },
        {
            "title": "Bandlik va mehnat bozori",
            "paragraphs": [
                "2008-yilgi iqtisodiy inqiroz va global retsessiyaning uzoq davom etgan taРІР‚в„ўsiriga qaramay, oРІР‚Вtgan oРІР‚Вn yilliklarda ayrim hududlarda ishchilarning oРІР‚Вta qashshoqlikda yashashi kamaydi. Shunga qaramay, bandlikning oРІР‚Вsish darajasi koРІР‚Вplab mamlakatlarda sekinlashib bormoqda.",
                "Barcha xodimlarning katta qismi hali ham rasmiy mehnat shartnomasiga ega emas. Bu esa ijtimoiy himoya, munosib daromad va mehnat xavfsizligi bilan bogРІР‚Вliq muammolarni kuchaytiradi.",
            ],
        },
        {
            "title": "Kelajak ustuvor yoРІР‚Вnalishlari",
            "paragraphs": [
                "SDG 8 kelib chiqishi, irqi va jinsidan qatРІР‚в„ўi nazar, barcha ishchilar uchun barqaror va adolatli iqtisodiy oРІР‚Вsishni ragРІР‚Вbatlantirishga qaratilgan. Bu diversifikatsiya, texnologik yangilanish va innovatsiyalar orqali iqtisodiy samaradorlikni oshirishni anglatadi.",
                "Kelgusida yuqori qoРІР‚Вshilgan qiymatga ega, mehnatni koРІР‚Вp talab qiluvchi tarmoqlarga eРІР‚в„ўtibor qaratish, yoshlar bandligini kuchaytirish va munosib mehnat standartlarini mustahkamlash asosiy vazifa boРІР‚Вlib qoladi.",
            ],
        },
    ],
}

SDG_10_DETAIL_UZ_CLEAN = {
    "hero_title": "Tengsizlikni kamaytirish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Mamlakatlar o'rtasidagi va ichida mavjud bo'lgan tengsizlikni qisqartirish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 10-maqsadi mamlakatlararo va ichki tengsizlik darajasini qisqartirishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 10 deb yuritiladi.",
                "SDG 10 ni amalga oshirish uchun 10 maqsad va taraqqiyot yo'lini belgilash uchun ko'rsatkichlar mavjud.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 7 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "daromadlar tengsizligini kamaytirish",
                "umumjahon ijtimoiy, iqtisodiy va siyosiy inklyuziyaga ko'maklashish",
                "teng imkoniyatlarni ta'minlash va kamsitishlarni tugatish",
                "tenglikni ta'minlovchi fiskal va ijtimoiy siyosatni qabul qilish",
                "jahon moliya bozorlari va institutlarini tartibga solishni takomillashtirish",
                "rivojlanayotgan mamlakatlarning moliya institutlarida vakolatlarini kuchaytirish",
                "mas'uliyatli va yaxshi boshqariladigan migratsiya siyosatini rivojlantirish",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Qolgan 3 maqsad erish vositasi bo'lib, ular quyidagilardan iborat:",
            ],
            "bullets": [
                "rivojlanayotgan mamlakatlar uchun maxsus va differentsial rejimni joriy qilish",
                "kam rivojlangan mamlakatlarda rivojlanishga yordam berish va investitsiyalarni rag'batlantirish",
                "migrantlarning pul o'tkazmalari uchun tranzaksiya xarajatlarini kamaytirish",
            ],
        },
        {
            "title": "Daromad va ijtimoiy tafovutlar",
            "paragraphs": [
                "SDG 10 aholining eng quyi 40 foizi daromadlari o'sishini milliy o'rtacha ko'rsatkichdan yuqori sur'atlarga chiqarishni maqsad qiladi. Bu maqsad SDG 1 bilan chambarchas bog'liq bo'lib, o'ta qashshoqlikka barham berish jarayonini to'ldiradi.",
                "2012-2017-yillarda 73 mamlakatda aholining eng quyi 40 foizi daromadlari o'sgani qayd etilgan. Shunga qaramay, ma'lumotlarga ega bo'lgan ko'plab mamlakatlarda ushbu qatlam umumiy daromad yoki iste'molning 25 foizidan kam ulushga ega bo'lib qolmoqda.",
            ],
        },
        {
            "title": "Tengsizlikning ko'rinishlari",
            "paragraphs": [
                "Tengsizlik iqtisodiy holat, jins, nogironlik, irqiy mansublik, ijtimoiy maqom va kamsitishning turli shakllarida namoyon bo'ladi.",
                "Salomatlik, ifloslanish va atrof-muhit bilan bog'liq muammolar ko'pincha tengsizlik bilan uzviy bog'liq bo'ladi. Ba'zan bu muammolar mahalliy va aborigen jamoalar, etnik ozchiliklar hamda past ijtimoiy-iqtisodiy maqomga ega qatlamlarga kuchliroq ta'sir qiladi.",
            ],
        },
        {
            "title": "Migratsiya va global xavflar",
            "paragraphs": [
                "Atrof-muhitni muhofaza qilish bo'yicha tadqiqotlar shuni ko'rsatadiki, ayrim jamoalar sog'liq va atrof-muhit uchun uzoq muddatli xavf tug'diradigan ifloslanish va toksik muhitlarda yashashga ko'proq duch keladi.",
                "Globallashuv jarayonida migratsiya, ko'chish va mulkdan mahrum bo'lish bilan bog'liq holatlar ko'pincha marginallashgan guruhlarning zaifligini oshiradi. Shu sababli tartibli, xavfsiz, muntazam va mas'uliyatli migratsiya siyosatini takomillashtirish muhim yo'nalish bo'lib qoladi.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Tengsizlik ruhiy va jismoniy salomatlik, ijtimoiy kapital, ijtimoiy singdirish va birlashish kabi yo'nalishlar bilan chambarchas bog'liq.",
                "Kelgusida inklyuziv siyosatlarni kuchaytirish, kamsitishning barcha shakllarini bartaraf etish, iqtisodiy imkoniyatlarni kengaytirish va zaif guruhlar manfaatlarini tizimli qo'llab-quvvatlash SDG 10 ga erishishning asosiy shartlaridan bo'lib qoladi.",
            ],
        },
    ],
}

SDG_11_DETAIL_UZ_CLEAN = {
    "hero_title": "Barqaror shaharlar va aholi yashash joylari",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Shahar va aholi yashash joylarining ochiqligi, xavfsizligi, mustahkamligi va ekologik barqarorligini ta'minlash.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 11-maqsadi shahar va aholi yashash joylarining ochiqligi, xavfsizligi, mustahkamligi va ekologik barqarorligini ta'minlashga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 11 deb yuritiladi.",
                "2015-yilda Birlashgan Millatlar Tashkiloti Bosh Assambleyasi tomonidan belgilangan barqaror rivojlanish maqsadlaridan biri sifatida SDG 11 shaharlardagi rivojlanish ijtimoiy, iqtisodiy va ekologik barqarorlikni muvozanatlashtirishi kerakligini ta'kidlaydi.",
                "SDG 11 ni amalga oshirish uchun 11 maqsad va taraqqiyot yo'lini belgilash uchun 14 ko'rsatkich mavjud.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 7 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "qulay, xavfsiz va arzon uy-joy, asosiy xizmatlar hamda xarobalarni obodonlashtirish",
                "xavfsiz, arzon, qulay va barqaror transport tizimlarini rivojlantirish",
                "inklyuziv, barqaror urbanizatsiya va barcha mamlakatlarda aholi punktlarini birgalikda, integratsiyalashgan va barqaror rejalashtirish hamda boshqarish imkoniyatlarini oshirish",
                "jahon madaniy va tabiiy merosini himoya qilish va saqlash bo'yicha sa'y-harakatlarni kuchaytirish",
                "favqulodda vaziyatlarda halok bo'lganlar va jabrlanganlar sonini kamaytirish, global yalpi ichki mahsulotga nisbatan to'g'ridan-to'g'ri iqtisodiy yo'qotishlarni kamaytirish",
                "havo sifati, shahar va boshqa chiqindilarni boshqarishga alohida e'tibor berish orqali shaharlarda aholi jon boshiga atrof-muhitga salbiy ta'sirni kamaytirish",
                "xavfsiz, inklyuziv va qulay, yashil hamda jamoat joylariga universal kirishni ta'minlash",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Maqsadga erishish uchun quyidagi vositalardan foydalaniladi:",
            ],
            "bullets": [
                "milliy va mintaqaviy rivojlanishni rejalashtirishni kuchaytirish orqali shaharlar, shahar atrofi va qishloqlar o'rtasidagi ijobiy iqtisodiy, ijtimoiy va ekologik aloqalarni qo'llab-quvvatlash",
                "inklyuziv, resurslardan samarali foydalanish, iqlim o'zgarishini yumshatish va unga moslashish, ofatlarga chidamlilik hamda favqulodda vaziyatlar bo'yicha Senday asosiga muvofiq vazifalar ishlab chiqish va amalga oshirish bo'yicha integratsiyalashgan siyosat va rejalarni qabul qiladigan hamda amalga oshiradigan shaharlar va aholi punktlari sonini ko'paytirish",
                "kam rivojlangan mamlakatlarni mahalliy materiallardan foydalangan holda ularga barqaror va bardoshli binolarni qurishda moliyaviy va texnik yordam orqali qo'llab-quvvatlash",
            ],
        },
        {
            "title": "Urbanizatsiya va resurs bosimi",
            "paragraphs": [
                "Dunyo bo'ylab shaharlar yer maydonining atigi 3 foizini egallaydi, lekin ular energiya iste'molining 60-80 foizini va uglerod chiqindilarining 75 foizini tashkil qiladi.",
                "Urbanizatsiyaning kuchayishi oziq-ovqat, energiya va suv kabi asosiy resurslarga kirishni kengaytirish va yaxshilashni talab qiladi. Bundan tashqari sanitariya, sog'liqni saqlash, ta'lim, mobillik va axborot kabi asosiy xizmatlarga ehtiyoj ham oshib bormoqda.",
            ],
        },
        {
            "title": "Global muammolar",
            "paragraphs": [
                "Shaharlardagi talablar global miqyosda to'liq qondirilmayapti va bu o'sib borayotgan kelajakdagi ehtiyojlarni qondirish uchun shaharlarning hayotiyligi va xavfsizligi oldida jiddiy muammolarni yuzaga keltiradi.",
                "Shu sababli barqaror shaharlarni shakllantirish nafaqat infratuzilma masalasi, balki ijtimoiy tenglik, ekologik himoya va xavfsiz turmush sifatini ta'minlash bilan ham bog'liqdir.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Kelgusida arzon uy-joy, barqaror transport, chiqindilarni samarali boshqarish, yashil hududlarni kengaytirish va ofatlarga chidamli infratuzilmani rivojlantirish SDG 11 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Shaharlar va aholi yashash joylarini inklyuziv, xavfsiz va ekologik jihatdan barqaror qilish uchun davlat, mahalliy hamjamiyat va xalqaro hamkorlar o'rtasida uzviy hamkorlik zarur.",
            ],
        },
    ],
}

SDG_12_DETAIL_UZ_CLEAN = {
    "hero_title": "Mas'uliyatli iste'mol va ishlab chiqarish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Oqilona iste'mol qilish va ishlab chiqarish modellariga o'tishni ta'minlash.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 12-maqsadi oqilona iste'mol qilish va ishlab chiqarish modellariga o'tishni ta'minlashga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 12 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 12 resurslardan unumli foydalanish, energiya samaradorligini oshirish, barqaror infratuzilmani ta'minlash, asosiy xizmatlardan foydalanish, yashil va munosib ish o'rinlarini ta'minlash hamda hamma uchun yaxshi hayot sifatini yaxshilashga xizmat qiladi.",
                "SDG 12 ni amalga oshirish uchun 2030-yilgacha 11 maqsad va taraqqiyot yo'lini belgilash uchun 13 ko'rsatkich mavjud.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 8 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "barqaror iste'mol va ishlab chiqarish namunalari bo'yicha 10 yillik dasturlarni amalga oshirish",
                "tabiiy resurslarni barqaror boshqarish va ulardan samarali foydalanishga erishish",
                "chakana va iste'molchi darajasida aholi jon boshiga to'g'ri keladigan global oziq-ovqat chiqindilarini yarmiga kamaytirish hamda ishlab chiqarish va ta'minot zanjirlarida oziq-ovqat yo'qotishlarini, shu jumladan hosildan keyingi yo'qotishlarni kamaytirish",
                "kimyoviy moddalar va barcha chiqindilarni butun hayot aylanishi davomida ekologik jihatdan oqilona boshqarishga erishish",
                "oldini olish, kamaytirish, qayta ishlash va qayta foydalanish orqali chiqindilarni ishlab chiqarishni kamaytirish",
                "kompaniyalarni barqaror amaliyotlarni qabul qilishga undash",
                "barqaror davlat xaridlari amaliyotini ilgari surish",
                "hamma joyda odamlar barqaror rivojlanish uchun tegishli ma'lumot va xabardorlikka ega bo'lishini ta'minlash",
            ],
        },
        {
            "title": "Maqsadga erishish vositalari",
            "paragraphs": [
                "Maqsadga erishish uchun quyidagi vositalardan foydalaniladi:",
            ],
            "bullets": [
                "rivojlanayotgan mamlakatlarning ilmiy va texnologik salohiyatini mustahkamlashda qo'llab-quvvatlash",
                "barqaror rivojlanish ta'sirini monitoring qilish vositalarini ishlab chiqish va joriy etish",
                "isrofgarchilikni rag'batlantiradigan qazib olinadigan yoqilg'i subsidiyalari kabi bozor buzilishlarini bartaraf etish",
            ],
        },
        {
            "title": "Global holat va xavflar",
            "paragraphs": [
                "Dunyo aholisining ortib borayotgani tabiiy resurslardan beqaror foydalanish bilan birga sayyoramizga halokatli ta'sir ko'rsatmoqda. Bu iqlim o'zgarishi, ekotizimlarning buzilishi va ifloslanish darajasining oshishiga olib keladi.",
                "Shu bois barqaror iste'mol va ishlab chiqarish hukumatlarni, korxonalarni va fuqarolarni kamroq xarajat bilan ko'proq va yaxshiroq ishlashga ilhomlantiradi, chunki u atrof-muhitni buzmasdan iqtisodiy o'sishga yordam beradi.",
            ],
        },
        {
            "title": "Iqtisodiyot va jamiyat uchun ahamiyati",
            "paragraphs": [
                "Resurslar samaradorligini oshirish barqaror turmush tarzini targ'ib qiladi. Bundan tashqari, barqaror iste'mol va ishlab chiqarish ham qashshoqlikni kamaytirishga, ham uglerodli, yashil iqtisodiyotga o'tishga hissa qo'shishi mumkin.",
                "Shu sababli ishlab chiqarishning ekologik toza usullaridan foydalanish, chiqindilarni kamaytirish va qayta ishlash ko'rsatkichlarini oshirish bilan birga kompaniyalarning barqaror amaliyotlarni qo'llashi va barqarorlik hisobotlarini nashr etishi muhimdir.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "2030-yilga kelib qayta ishlangan materiallar ulushini oshirish, chiqindilarni kamaytirish, oziq-ovqat yo'qotishlarini qisqartirish va davlat hamda xususiy sektorda mas'uliyatli xarid siyosatini kuchaytirish SDG 12 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Bu maqsadga erishish uchun hukumatlar, biznes sektori, ilmiy doira va aholi o'rtasida xabardorlikni oshirish hamda amaliy hamkorlikni kengaytirish zarur.",
            ],
        },
    ],
}

SDG_13_DETAIL_UZ_CLEAN = {
    "hero_title": "Iqlim o'zgarishiga qarshi kurashish",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Iqlim o'zgarishi va uning oqibatlariga qarshi kurashish bo'yicha tezkor choralar ko'rish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 13-maqsadi iqlim o'zgarishi va uning oqibatlariga qarshi kurashish bo'yicha tezkor choralar ko'rishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 13 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 13 2030-yilgacha erishilishi kerak bo'lgan beshta maqsadni o'z ichiga oladi va iqlim bilan bog'liq keng ko'lamli masalalarni qamrab oladi.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Dastlabki 3 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "iqlim bilan bog'liq tabiiy ofatlarga chidamlilik va moslashish qobiliyatini kuchaytirish",
                "iqlim o'zgarishi bo'yicha chora-tadbirlarni siyosat va rejalashtirishga integratsiya qilish",
                "iqlim o'zgarishiga qarshi kurashish uchun bilim va salohiyatni shakllantirish",
            ],
        },
        {
            "title": "Amalga oshirish mexanizmlari",
            "paragraphs": [
                "Qolgan ikkita maqsadda BMTning iqlim o'zgarishi bo'yicha doiraviy konventsiyasini amalga oshirish, rejalashtirish va boshqarish salohiyatini oshirish mexanizmlari ilgari surilgan.",
                "Bu yo'nalishlar ayniqsa rivojlanayotgan mamlakatlar va iqlim xavfiga ko'proq duch kelayotgan hududlar uchun muhim ahamiyatga ega.",
            ],
        },
        {
            "title": "Global ta'sirlar",
            "paragraphs": [
                "Hozirgi vaqtda iqlim o'zgarishi dunyoning barcha mamlakatlarida global hamjamiyatga ta'sir ko'rsatmoqda. Uning ta'siri nafaqat milliy iqtisodiyotlarga, balki hayot va yashash vositalariga, ayniqsa zaif sharoitlarda bo'lgan aholiga ham kuchli ta'sir qiladi.",
                "2018-yilda iqlim o'zgarishi bilan bog'liq tabiiy ofatlar, masalan katta o'rmon yong'inlari, qurg'oqchilik, bo'ronlar va toshqinlar chastotasi kuchaydi.",
            ],
        },
        {
            "title": "Energiya va iqlim bog'liqligi",
            "paragraphs": [
                "Toza energiya bo'yicha SDG 13 va SDG 7 bir-biri bilan chambarchas bog'liq va o'zaro bir-birini to'ldiradi.",
                "Parij kelishuvi bo'yicha majburiyatlarni bajarish uchun mamlakatlar issiqxona gazlarini qisqartirishning yetakchi yo'nalishlari sifatida yoqilg'idan qayta tiklanadigan energiyaga o'tish va yakuniy energiya samaradorligini oshirishga e'tibor qaratishi kerak.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Kelgusida iqlim xavflariga moslashuvchan infratuzilma qurish, favqulodda vaziyatlarga tayyorgarlikni kuchaytirish, ekologik ta'limni kengaytirish va milliy siyosatlarni iqlim maqsadlari bilan uyg'unlashtirish SDG 13 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Iqlim o'zgarishiga qarshi samarali kurashish uchun hukumatlar, biznes, ilmiy muassasalar va mahalliy hamjamiyatlarning uzviy hamkorligi zarur.",
            ],
        },
    ],
}

SDG_14_DETAIL_UZ_CLEAN = {
    "hero_title": "Dengiz ekotizimlarini asrash",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Barqaror taraqqiyot yo'lida okeanlar, dengizlar va dengiz zaxiralarini asrash va ulardan oqilona foydalanish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 14-maqsadi okeanlar, dengizlar va dengiz zaxiralarini asrash hamda ulardan oqilona foydalanishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 14 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 14 ni amalga oshirish uchun 2030-yilgacha 10 maqsad va taraqqiyot yo'lini belgilashga xizmat qiluvchi ko'rsatkichlar mavjud.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 7 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "dengiz ifloslanishini kamaytirish",
                "ekotizimlarni himoya qilish va tiklash",
                "okeanning kislotaliligini kamaytirish",
                "barqaror baliq ovlash",
                "qirg'oq va dengiz hududlarini saqlab qolish",
                "ortiqcha baliq ovlashga hissa qo'shadigan subsidiyalarni tugatish",
                "dengiz resurslaridan barqaror foydalanishdan olingan iqtisodiy foydani oshirish",
            ],
        },
        {
            "title": "Qo'llab-quvvatlovchi vositalar",
            "paragraphs": [
                "Qolgan 3 maqsad quyidagi yo'nalishlarga qaratilgan:",
            ],
            "bullets": [
                "okean salomatligi uchun ilmiy bilimlar, tadqiqotlar va texnologiyalarni oshirish",
                "kichik baliqchilarni qo'llab-quvvatlash",
                "xalqaro dengiz huquqini qo'llash va amalga oshirish",
            ],
        },
        {
            "title": "Okeanlarning hayotiy ahamiyati",
            "paragraphs": [
                "Okeanlar va baliqchilik dunyo aholisining iqtisodiy, ijtimoiy va ekologik ehtiyojlarini qo'llab-quvvatlaydi. Okeanlar sayyoramizning hayot manbai va global iqlim tizimining regulyatori hisoblanadi.",
                "Ular dunyodagi eng katta ekotizim bo'lib, millionga yaqin tur yashash muhiti bilan bog'liq. Okeanlar yer yuzasining uchdan ikki qismini egallaydi va sayyoradagi suvning 97 foizini o'z ichiga oladi.",
                "Yomg'ir suvi, ichimlik suvi, iqlim, issiqlik miqdori va oqimlar bilan bog'liq ko'plab tabiiy jarayonlar okeanlar orqali boshqariladi. 3 milliarddan ortiq odamning turmush manbai dengiz hayoti bilan bog'langan.",
            ],
        },
        {
            "title": "Xavflar va muammolar",
            "paragraphs": [
                "Sanoat inqilobidan keyin okeanlar kislotaliligi sezilarli darajada oshdi va bu barqaror foydalanish hamda bioxilma-xillik uchun jiddiy xavf tug'dirmoqda.",
                "Okeanlardan barqaror foydalanishni ta'minlash uchun ularning kislotaliligi oshishining salbiy oqibatlarini yumshatish bo'yicha samarali strategiyalar zarur.",
                "2020-yilgi Barqaror rivojlanish maqsadlari bo'yicha hisobotga ko'ra, okeanlarni, dengiz muhitini va kichik baliqchilikni muhofaza qilish bo'yicha qilinayotgan sa'y-harakatlar resurslarni muhofaza qilish ehtiyojlarini to'liq qondirmayapti.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Kelgusida dengiz ifloslanishini kamaytirish, qirg'oq hududlarini muhofaza qilish, ilmiy monitoringni kuchaytirish va baliqchilik resurslarini oqilona boshqarish SDG 14 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Okeanlar salomatligini saqlash uchun xalqaro hamkorlik, ilmiy innovatsiyalar va mahalliy jamoalarni qo'llab-quvvatlash birgalikda olib borilishi kerak.",
            ],
        },
    ],
}

SDG_15_DETAIL_UZ_CLEAN = {
    "hero_title": "Quruqlikdagi ekotizimlarni asrash",
    "idea_title": "Asosiy g'oya",
    "idea_text": "O'rmonlardan oqilona foydalanish, cho'llashishga qarshi kurashish, yer tanazzuli holatlariga chek qo'yish va yer unumdorligini qayta tiklash hamda biologik xilma-xillikning yo'qolib ketish xavfini bartaraf etish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 15-maqsadi o'rmonlardan oqilona foydalanish, cho'llashishga qarshi kurashish, yer tanazzuli holatlariga chek qo'yish va yer unumdorligini qayta tiklash hamda biologik xilma-xillikning yo'qolib ketish xavfini bartaraf etishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 15 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 15 2030-yilgacha erishilishi kerak bo'lgan 12 ta maqsaddan iborat bo'lib, 14 ko'rsatkich bilan o'lchanadi.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 9 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "quruqlik va chuchuk suv ekotizimlarini saqlash va tiklash",
                "o'rmonlarni kesishni tugatish va buzilgan o'rmonlarni tiklash",
                "cho'llanishni tugatish va degradatsiyaga uchragan yerlarni tiklash",
                "tog' ekotizimlarining saqlanishini ta'minlash, biologik xilma-xillik va tabiiy yashash joylarini muhofaza qilish",
                "genetik resurslardan foydalanishni va imtiyozlarni adolatli taqsimlashni himoya qilish",
                "muhofaza qilinadigan turlarning brakonerlik va savdosiga barham berish",
                "quruqlikda va suv ekotizimlarida invaziv begona turlarning paydo bo'lishining oldini olish",
                "ekotizim va biologik xilma-xillikni hukumat rejalashtirishiga integratsiya qilish",
            ],
        },
        {
            "title": "Qo'llab-quvvatlovchi maqsadlar",
            "paragraphs": [
                "Qolgan 3 maqsad quyidagi yo'nalishlarga qaratilgan:",
            ],
            "bullets": [
                "ekotizim va bioxilma-xillikni saqlash hamda undan barqaror foydalanish uchun moliyaviy resurslarni oshirish",
                "o'rmonlarni barqaror boshqarishni moliyalashtirish va rag'batlantirish",
                "global brakonerlik va odam savdosiga qarshi kurashish",
            ],
        },
        {
            "title": "Quruqlik ekotizimlarining ahamiyati",
            "paragraphs": [
                "Inson hayoti quruqlik va okeanlarga bog'liq. SDG 15 kelajak avlodlar uchun barqaror turmush tarzini ta'minlashga qaratilgan.",
                "Inson ratsionining katta qismi o'simlik hayotiga bog'liq bo'lib, qishloq xo'jaligi asosiy iqtisodiy resurslardan biri hisoblanadi. O'rmonlar Yer yuzasining qariyb 30 foizini egallaydi va millionlab turlarning hayotiy muhitini ta'minlaydi.",
                "Toza havo va suvning muhim manbai sifatida quruqlik ekotizimlari iqlim o'zgarishiga qarshi kurashda ham muhim ahamiyatga ega.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Kelgusida o'rmonlarni tiklash, degradatsiyaga uchragan yerlarni qayta jonlantirish, bioxilma-xillikni himoya qilish va brakonerlikka qarshi kurashni kuchaytirish SDG 15 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Quruqlikdagi ekotizimlarni saqlash uchun hukumatlar, mahalliy hamjamiyatlar, ilmiy muassasalar va xalqaro tashkilotlar o'rtasidagi hamkorlikni kengaytirish zarur.",
            ],
        },
    ],
}

SDG_16_DETAIL_UZ_CLEAN = {
    "hero_title": "Tinchlik, adolat va samarali boshqaruv",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Barqaror rivojlanish manfaatlari yo'lida tinchliksevar va ochiq jamiyatlar qurilishiga ko'maklashish, barcha uchun odil sudlov imkoniyatidan foydalanishni ta'minlash va barcha darajalarda samarali, hisobdor va keng ishtirokka asoslangan muassasalarni tashkil etish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 16-maqsadi tinchliksevar va ochiq jamiyatlar qurilishiga ko'maklashish, barcha uchun odil sudlov imkoniyatidan foydalanishni ta'minlash va barcha darajalarda samarali, hisobdor hamda keng ishtirokka asoslangan muassasalarni tashkil etishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 16 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 16 2030-yilgacha erishilishi kerak bo'lgan 12 ta maqsad va 23 ko'rsatkichdan iborat.",
            ],
        },
        {
            "title": "Maqsadli natijalar",
            "paragraphs": [
                "Birinchi 10 ta maqsad maqsadli natijalar deb yuritiladi va ular quyidagilarni o'z ichiga oladi:",
            ],
            "bullets": [
                "zo'ravonlikni kamaytirish",
                "bolalarni zo'ravonlik, ekspluatatsiya, odam savdosi va zo'ravonlikdan himoya qilish",
                "qonun ustuvorligini ta'minlash",
                "odil sudlovdan teng foydalanishni ta'minlash",
                "uyushgan jinoyatchilikka, noqonuniy moliyaviy va qurol-yarog' oqimiga qarshi kurashish, korrupsiya va poraxo'rlikni sezilarli darajada kamaytirish",
                "samarali, hisob beruvchi va shaffof institutlarni rivojlantirish",
                "sezgir, inklyuziv va vakillik qarorlarini qabul qilishni ta'minlash",
                "global boshqaruvdagi ishtirokni kuchaytirish",
                "universal yuridik shaxsni ta'minlash",
                "aholining axborotdan foydalanishini ta'minlash va asosiy erkinliklarni himoya qilish",
            ],
        },
        {
            "title": "Institutsional yo'nalishlar",
            "paragraphs": [
                "Keyingi ikki maqsad zo'ravonlikning oldini olish, jinoyatchilik va terrorizmga qarshi kurashish bo'yicha milliy institutlarni mustahkamlash hamda kamsituvchi qonunlar va siyosatlarni bartaraf etishga qaratilgan.",
                "Zo'ravonlik jinoyatlarini kamaytirish, jinsiy savdo, majburiy mehnat va bolalarni zo'ravonlikdan qaytarish bo'yicha aniq global choralar ushbu maqsadning muhim tarkibiy qismidir.",
            ],
        },
        {
            "title": "Tinchlik va adolatning ahamiyati",
            "paragraphs": [
                "Xalqaro hamjamiyat tinchlik va adolatni barqaror rivojlanishning muhim asosi deb biladi. Qonunlar ijrosini ta'minlaydigan, tinch va adolatli jamiyat yaratishga yordam beradigan kuchli sud tizimlari bu maqsadga erishishda markaziy o'rin tutadi.",
                "Shaffof boshqaruv, hisobdor institutlar va keng jamoatchilik ishtiroki bo'lmasa, boshqa barqaror rivojlanish maqsadlariga erishish ham qiyinlashadi.",
            ],
        },
        {
            "title": "Kelgusi ustuvor yo'nalishlar",
            "paragraphs": [
                "Kelgusida korrupsiyani kamaytirish, odil sudlovga teng kirishni kengaytirish, bolalar va zaif guruhlarni himoya qilish, shaffof boshqaruvni kuchaytirish hamda fuqarolarning qaror qabul qilishdagi ishtirokini oshirish SDG 16 ning asosiy ustuvor yo'nalishlari bo'lib qoladi.",
                "Tinchlik, adolat va samarali boshqaruvni ta'minlash uchun davlat, fuqarolik jamiyati, sud tizimi va xalqaro hamkorlar o'rtasida uzviy hamkorlik zarur.",
            ],
        },
    ],
}

SDG_17_DETAIL_UZ_CLEAN = {
    "hero_title": "Barqaror rivojlanish yo'lida hamkorlik",
    "idea_title": "Asosiy g'oya",
    "idea_text": "Barqaror rivojlanish manfaatlari yo'lida global hamkorlikni faollashtirish.",
    "sections": [
        {
            "title": "Umumiy ma'lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 17-maqsadi barqaror rivojlanish manfaatlari yo'lida global hamkorlikni faollashtirishga qaratilgan. Keyingi o'rinlarda bu maqsad SDG 17 deb yuritiladi.",
                "Birlashgan Millatlar Tashkiloti tomonidan 2015-yilda belgilangan 17 ta barqaror rivojlanish maqsadlaridan biri sifatida SDG 17 2030-yilgacha erishilishi kerak bo'lgan 17 ta maqsad va 25 ta ko'rsatkichdan iborat bo'lib, ular moliya, texnologiya, salohiyatni oshirish, savdo va tizimli masalalarni qamrab oladi.",
            ],
        },
        {
            "title": "Hamkorlikning mazmuni",
            "paragraphs": [
                "SDG 17 barcha maqsadlarga erishish uchun tenglikka asoslangan, adolatli va bir tomonlama bo'lmagan sektoral hamkorlik zarurligini anglatadi.",
                "Bu mamlakatlar siyosatini uyg'unlashtirish, adolatli savdoni rivojlantirish, transchegaraviy barqaror rivojlanishni rag'batlantirish va muvofiqlashtirilgan investitsiya tashabbuslarini kuchaytirishga qaratilgan.",
                "Maqsad rivojlangan va rivojlanayotgan davlatlar o'rtasidagi hamkorlikni mustahkamlash, SDGlardan umumiy asos sifatida foydalanish va hamkorlik yo'lini belgilash uchun umumiy qarashlarni shakllantirishni ham o'z ichiga oladi.",
            ],
        },
        {
            "title": "Savdo va moliyalashtirish",
            "paragraphs": [
                "SDG 17 savdoni rivojlantirishga intiladi va rivojlanayotgan mamlakatlar uchun adolatli, ochiq va hamma uchun foydali bo'lgan universal qoidalarga asoslangan savdo tizimini ta'minlashga yordam beradi.",
                "SDGlarga erishish uchun har yili 5 trillion dollardan 7 trillion dollargacha sarmoya talab etiladi. 2017-yilda jami rasmiy rivojlanish yordami 147,2 milliard AQSh dollarini tashkil etgan bo'lsa-da, bu belgilangan ehtiyojdan past hisoblanadi.",
                "2017-yilda rivojlanayotgan mamlakatlarga xalqaro pul o'tkazmalari 613 milliard AQSh dollariga yetgan va bu hamkorlikni moliyaviy jihatdan qo'llab-quvvatlashda muhim manba bo'lib qolgan.",
            ],
        },
        {
            "title": "Global muammolar va ehtiyojlar",
            "paragraphs": [
                "Mojarolar yoki tabiiy ofatlar natijasida yuzaga kelgan gumanitar inqirozlar qo'shimcha moliyaviy resurslar va yordam talab qilishda davom etmoqda.",
                "Shunga qaramay, ko'plab mamlakatlar iqtisodiy o'sish va savdoni rag'batlantirish uchun rasmiy rivojlanish yordamiga muhtoj bo'lib qolmoqda. Global taraqqiyot xaritasi shuni ko'rsatadiki, dunyoning aksariyat qismida asosiy muammolar hali ham saqlanib qolmoqda.",
            ],
        },
        {
            "title": "Ko'p tomonlama hamkorlikning ahamiyati",
            "paragraphs": [
                "Muvaffaqiyatli barqaror rivojlanish dasturi hukumatlar, xususiy sektor va fuqarolik jamiyati o'rtasidagi hamkorlikni talab qiladi.",
                "Prinsiplar va qadriyatlar, umumiy qarashlar hamda odamlar va sayyorani markazga qo'yadigan umumiy maqsadlarga asoslangan ushbu inklyuziv hamkorlik global, mintaqaviy, milliy va mahalliy darajada zarur.",
            ],
        },
        {
            "title": "Ustuvor yo'nalishlar",
            "paragraphs": [
                "SDG 17 uzoq muddatli investitsiyalarga muhtoj bo'lgan, rivojlanayotgan mamlakatlarda ko'proq moslasha oladigan sektorlar va kompaniyalarni kuchaytirishga qaratilgan.",
                "Uning asosiy yo'nalishlari mamlakatlarning energiya, infratuzilma, transport tizimlari va axborot-kommunikatsiya texnologiyalari sohasidagi imkoniyatlarini takomillashtirish bilan bog'liq.",
            ],
        },
    ],
}


def build_sdg_goal(item, language_code):
    use_uz = language_code == "uz"
    return {
        "number": item["number"],
        "image": item["image_uz"] if use_uz else item["image_en"],
        "gif": item["gif"],
        "title": item["title_uz"] if use_uz else item["title_en"],
        "description": item["description_uz"] if use_uz else item["description_en"],
    }


def get_sdg_goal(number, language_code):
    raw_item = next((item for item in SDG_CONTENT if item["number"] == number), None)
    if not raw_item:
        raise Http404("SDG not found")
    return build_sdg_goal(raw_item, language_code)


def set_portal_language(request, language_code):
    language_code = language_code if language_code in {"uz", "en"} else "en"
    request.session["portal_language"] = language_code
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    response = redirect(next_url)
    response.set_cookie("portal_language", language_code)
    return response


def normalize_search_text(value):
    normalized = (value or "").lower()
    for source, target in {
        "РІР‚в„ў": "'",
        "`": "'",
        "РљВ»": "'",
        "РІР‚Сљ": '"',
        "РІР‚Сњ": '"',
        "РІР‚вЂњ": "-",
        "РІР‚вЂќ": "-",
    }.items():
        normalized = normalized.replace(source, target)
    return " ".join(normalized.split())


def score_search_entry(query, *values):
    normalized_query = normalize_search_text(query)
    if not normalized_query:
        return 1

    searchable_text = normalize_search_text(" ".join(str(value or "") for value in values))
    if not searchable_text:
        return 0

    tokens = [token for token in normalized_query.split() if token]
    if normalized_query in searchable_text:
        return 120 + len(tokens)
    if tokens and all(token in searchable_text for token in tokens):
        return 80 + len(tokens)

    token_hits = sum(1 for token in tokens if token in searchable_text)
    if token_hits:
        return 30 + token_hits
    return 0


def build_search_sections(language_code, query):
    query = (query or "").strip()
    use_uz = language_code == "uz"

    def section(label_uz, label_en, items):
        return {"label": label_uz if use_uz else label_en, "items": items}

    def sort_and_trim(items, limit=8):
        ranked = [item for item in items if item.get("_score", 0) > 0]
        ranked.sort(key=lambda item: (-item["_score"], item["title"]))
        return [{key: value for key, value in item.items() if key != "_score"} for item in ranked[:limit]]

    sections = []

    site_settings = localize_object(SiteSettings.objects.first(), language_code)
    leadership_items = []
    if site_settings:
        leadership_score = score_search_entry(
            query,
            site_settings.institution_name,
            site_settings.leader_name,
            site_settings.leader_title,
            site_settings.leader_message,
            site_settings.email,
            site_settings.phone,
        )
        if leadership_score:
            leadership_items.append(
                {
                    "title": site_settings.leader_name,
                    "summary": site_settings.leader_title,
                    "url": "/",
                    "meta": use_uz and "Rahbariyat" or "Leadership",
                    "_score": leadership_score,
                }
            )

    for department in localize_collection(DepartmentContact.objects.all(), language_code):
        score = score_search_entry(
            query,
            department.department_name,
            department.contact_person,
            department.email,
            department.phone,
            department.office_location,
            department.office_hours,
        )
        if score:
            leadership_items.append(
                {
                    "title": department.contact_person,
                    "summary": department.department_name,
                    "url": "/contact/",
                    "meta": department.email,
                    "_score": score,
                }
            )

    special_contacts = [
        (ANTI_CORRUPTION_CONTACT_CONTENT["uz" if use_uz else "en"], "/about/anti-corruption/contact/"),
        (FINANCIAL_CONTACT_CONTENT["uz" if use_uz else "en"], "/about/sdg-investment/contact/"),
        (WOMEN_SUPPORT_CONTACT_CONTENT["uz" if use_uz else "en"], "/about/xotin-qizlar/contact/"),
    ]
    for content, url in special_contacts:
        joined_sections = " ".join(
            " ".join(section.get("paragraphs", []) + section.get("bullets", []))
            for section in content.get("sections", [])
        )
        score = score_search_entry(
            query,
            content.get("title"),
            content.get("leader_name"),
            content.get("leader_role"),
            " ".join(content.get("leader_details", [])),
            joined_sections,
        )
        if score:
            leadership_items.append(
                {
                    "title": content.get("leader_name") or content.get("title"),
                    "summary": content.get("leader_role") or content.get("title"),
                    "url": url,
                    "meta": content.get("title"),
                    "_score": score,
                }
            )

    governance_items = []
    for slug, content in GOVERNANCE_PAGE_CONTENT.items():
        title = content["title_uz"] if use_uz else content["title_en"]
        intro = content["intro_uz"] if use_uz else content["intro_en"]
        rich_text = strip_tags(content.get("single_card_raw_uz" if use_uz else "single_card_raw_en", ""))
        section_text = " ".join(
            " ".join(section.get("paragraphs", []) + section.get("bullets", []))
            for section in content.get("sections_uz" if use_uz else "sections_en", [])
        )
        score = score_search_entry(query, title, intro, slug, rich_text, section_text)
        if score:
            governance_items.append({"title": title, "summary": intro, "url": f"/about/{slug}/", "_score": score})

    campus_items = []
    campus_sections = [
        {
            "title_uz": "Joylashuv & Infratuzilma",
            "title_en": "Location & Infrastructure",
            "summary_uz": "Kampus hududi, bino va inshootlar, yashil maydonlar hamda infratuzilma quvvatlari bo'yicha asosiy ma'lumotlar.",
            "summary_en": "Core information on the campus site, buildings, green areas, and infrastructure capacity.",
        },
        {
            "title_uz": "Energiya & iqlim o'zgarishi",
            "title_en": "Energy & Climate Change",
            "summary_uz": "Energiya samaradorligi, elektr va issiqlik iste'moli, quyosh energiyasi va emissiyalarni kamaytirish choralarini qamrab oladi.",
            "summary_en": "Covers energy efficiency, electricity and heat use, solar energy, and measures to reduce emissions.",
        },
        {
            "title_uz": "Chiqindilar",
            "title_en": "Waste",
            "summary_uz": "Maishiy va operatsion chiqindilarni boshqarish, saralash, qayta ishlash va ekologik nazorat bo'yicha yo'nalish.",
            "summary_en": "Focuses on operational and household waste management, sorting, recycling, and environmental control.",
        },
        {
            "title_uz": "Suv",
            "title_en": "Water",
            "summary_uz": "Suv resurslarini tejash, tarmoqlarni monitoring qilish va samarali foydalanish bo'yicha tashabbuslar.",
            "summary_en": "Highlights initiatives for water conservation, network monitoring, and efficient use.",
        },
        {
            "title_uz": "Transport",
            "title_en": "Transport",
            "summary_uz": "Talaba va xodimlar qatnovi, kampus ichki harakati va barqaror transport yechimlari bo'yicha ma'lumotlar.",
            "summary_en": "Presents information on student and staff mobility, internal campus movement, and sustainable transport solutions.",
        },
    ]
    for item in campus_sections:
        title = item["title_uz"] if use_uz else item["title_en"]
        summary = item["summary_uz"] if use_uz else item["summary_en"]
        score = score_search_entry(query, title, summary, "campus", "sustainability")
        if score:
            campus_items.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": "/sustainability-strategy/",
                    "_score": score,
                }
            )

    page_items = []
    page_map = {
        "home": "/",
        "about": "/about/",
        "programs": "/programs/",
        "research": "/research-projects/",
        "education": "/education-initiatives/",
        "sustainability": "/sustainability-strategy/",
        "reports": "/reports-insights/",
        "news": "/news-events/",
        "contact": "/contact/",
    }
    for page in localize_collection(PageContent.objects.all(), language_code):
        url = page_map.get(page.page_key)
        if url:
            score = score_search_entry(query, page.title, page.intro, page.supporting_title, page.supporting_text)
            if score:
                page_items.append({"title": page.title, "summary": page.intro, "url": url, "_score": score})

    program_items = []
    for item in localize_collection(Program.objects.all(), language_code):
        score = score_search_entry(query, item.title, item.summary, item.body, item.slug)
        if score:
            program_items.append(
                {
                    "title": item.title,
                    "summary": item.summary,
                    "url": f"/programs/{item.slug}/" if item.slug.startswith("sdg-") else "/programs/",
                    "_score": score,
                }
            )

    research_items = []
    for item in localize_collection(ResearchProject.objects.all(), language_code):
        score = score_search_entry(query, item.title, item.summary, item.body, item.lead_unit, item.timeframe)
        if score:
            research_items.append({"title": item.title, "summary": item.summary, "url": "/research-projects/", "_score": score})

    education_items = []
    for item in localize_collection(EducationInitiative.objects.all(), language_code):
        score = score_search_entry(query, item.title, item.summary, item.body, item.audience, item.delivery_model)
        if score:
            education_items.append({"title": item.title, "summary": item.summary, "url": "/education-initiatives/", "_score": score})

    report_items = []
    for item in localize_collection(Report.objects.all(), language_code):
        score = score_search_entry(query, item.title, item.summary, item.body, item.highlight_metric)
        if score:
            report_items.append(
                {
                    "title": item.title,
                    "summary": item.summary,
                    "url": "/reports-insights/",
                    "meta": item.publish_date.strftime("%d.%m.%Y") if getattr(item, "publish_date", None) else "",
                    "_score": score,
                }
            )

    report_cards = [
        {
            "title_uz": "Issiqxona gazlari emissiyalari hisoboti",
            "title_en": "Greenhouse gas emissions report",
            "summary_uz": "Universitet faoliyatidagi issiqxona gazlari, emissiya ko'rsatkichlari va ekologik monitoring bo'yicha ma'lumotlar.",
            "summary_en": "Information on greenhouse gas emissions, climate indicators, and environmental monitoring across the university.",
            "url": "/reports-insights/greenhouse-gases/",
        },
        {
            "title_uz": "Moliyaviy hisobot",
            "title_en": "Financial report",
            "summary_uz": "Moliyaviy faoliyat, mablag'lar taqsimoti va institutsional xarajatlar bo'yicha asosiy hisobotlar.",
            "summary_en": "Key reports on financial activity, fund allocation, and institutional expenditure.",
            "url": "/reports-insights/financial-report/",
        },
        {
            "title_uz": "Barqarorlik hisoboti",
            "title_en": "Sustainability report",
            "summary_uz": "Barqaror rivojlanish maqsadlari, tashabbuslar va universitetning umumiy barqarorlik natijalari bo'yicha hisobot.",
            "summary_en": "A report covering sustainability goals, initiatives, and the university's overall sustainability performance.",
            "url": "/reports-insights/sustainability-report/",
        },
    ]
    for card in report_cards:
        title = card["title_uz"] if use_uz else card["title_en"]
        summary = card["summary_uz"] if use_uz else card["summary_en"]
        score = score_search_entry(query, title, summary, "report", "insights")
        if score:
            report_items.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": card["url"],
                    "_score": score,
                }
            )

    news_items = []
    for item in localize_collection(NewsArticle.objects.all(), language_code):
        score = score_search_entry(
            query,
            item.title,
            item.summary,
            item.body,
            getattr(item, "title_uz", ""),
            getattr(item, "title_en", ""),
            getattr(item, "summary_uz", ""),
            getattr(item, "summary_en", ""),
        )
        if score:
            news_items.append(
                {
                    "title": item.title,
                    "summary": item.summary,
                    "url": item.get_absolute_url(),
                    "meta": item.published_on.strftime("%d.%m.%Y") if getattr(item, "published_on", None) else "",
                    "_score": score,
                }
            )

    event_items = []
    for item in localize_collection(Event.objects.all(), language_code):
        score = score_search_entry(query, item.title, item.summary, item.details, item.venue, item.audience)
        if score:
            event_items.append(
                {
                    "title": item.title,
                    "summary": item.summary,
                    "url": item.get_absolute_url(),
                    "meta": item.start_date.strftime("%d.%m.%Y") if getattr(item, "start_date", None) else "",
                    "_score": score,
                }
            )

    for group in [
        section("Rahbariyat va aloqalar", "Leadership and contacts", sort_and_trim(leadership_items)),
        section("Asosiy sahifalar", "Main pages", sort_and_trim(page_items)),
        section("Barqarorlik boshqaruvi", "Sustainability governance", sort_and_trim(governance_items)),
        section("Kampus", "Campus", sort_and_trim(campus_items)),
        section("Dasturlar va BRMlar", "Programs and SDGs", sort_and_trim(program_items)),
        section("Tadqiqot", "Research", sort_and_trim(research_items)),
        section("Ta'lim va tashabbuslar", "Education and initiatives", sort_and_trim(education_items)),
        section("Hisobotlar", "Reports", sort_and_trim(report_items)),
        section("Yangiliklar", "News", sort_and_trim(news_items)),
        section("Tadbirlar", "Events", sort_and_trim(event_items)),
    ]:
        if group["items"]:
            sections.append(group)

    return sections


class BasePortalContextMixin:
    page_key = "home"

    def get_language_code(self):
        language_code = (
            self.request.session.get("portal_language")
            or self.request.COOKIES.get("portal_language")
            or getattr(self.request, "LANGUAGE_CODE", "en")
            or "en"
        )
        return language_code if language_code in {"uz", "en"} else "en"

    def get_site_settings(self):
        return localize_object(SiteSettings.objects.first(), self.get_language_code())

    def get_page_content(self):
        return localize_object(PageContent.objects.filter(page_key=self.page_key).first(), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = self.get_site_settings()
        context["page_content"] = self.get_page_content()
        context["footer_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], self.get_language_code())
        context["footer_departments"] = localize_collection(DepartmentContact.objects.all()[:3], self.get_language_code())
        context["active_page"] = self.page_key
        context["current_language"] = self.get_language_code()
        context["header_search_query"] = self.request.GET.get("q", "").strip()
        return context


class HomeView(BasePortalContextMixin, TemplateView):
    template_name = "portal/home.html"
    page_key = "home"

    @staticmethod
    def _fragment_signature(items):
        if not items:
            return "empty"
        return "-".join(
            f"{item.pk}:{item.updated_at.strftime('%Y%m%d%H%M%S')}"
            for item in items
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        selected_sdg = self.request.GET.get("sdg")
        available_sdg_numbers = list(
            NewsArticle.objects.filter(sdg_goal__isnull=False)
            .order_by("sdg_goal")
            .values_list("sdg_goal", flat=True)
            .distinct()
        )
        try:
            selected_sdg = int(selected_sdg) if selected_sdg else None
        except (TypeError, ValueError):
            selected_sdg = None
        if selected_sdg not in range(1, 18):
            selected_sdg = available_sdg_numbers[0] if available_sdg_numbers else 1
        sustainability_news = NewsArticle.objects.filter(sdg_goal=selected_sdg)[:3]
        latest_news_items = list(NewsArticle.objects.all()[:3])
        context["hero_stats"] = localize_collection(HeroStat.objects.all()[:4], language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all()[:4], language_code)
        context["featured_programs"] = localize_collection(Program.objects.filter(featured=True)[:3], language_code)
        context["featured_research"] = localize_collection(ResearchProject.objects.filter(featured=True)[:2], language_code)
        context["impact_metrics"] = localize_collection(ImpactMetric.objects.filter(scope__in=["home", "both"])[:4], language_code)
        context["latest_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], language_code)
        context["latest_news"] = localize_collection(latest_news_items, language_code)
        context["sustainability_news"] = localize_collection(sustainability_news, language_code)
        context["partners"] = localize_collection(Partner.objects.all()[:6], language_code)
        context["sdg_goals"] = [build_sdg_goal(item, language_code) for item in SDG_CONTENT]
        context["selected_sdg"] = selected_sdg
        context["selected_sdg_goal"] = get_sdg_goal(selected_sdg, language_code)
        context["home_hero_cache_key"] = (
            f"{language_code}:{context['site_settings'].updated_at.strftime('%Y%m%d%H%M%S')}"
        )
        context["home_sdg_grid_cache_key"] = language_code
        context["home_latest_news_cache_key"] = (
            f"{language_code}:{self._fragment_signature(latest_news_items)}"
        )
        return context


class ResultsShowcaseView(BasePortalContextMixin, TemplateView):
    template_name = "portal/results_showcase.html"
    page_key = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()

        ranking_cards = [
            {
                "region": "QS Asia",
                "value": "925th",
                "title_uz": "QS Asia University Rankings",
                "title_en": "QS Asia University Rankings",
                "subtitle_uz": "Osiyo universitetlari reytingi",
                "subtitle_en": "Asia university ranking",
            },
            {
                "region": "QS Uzbekistan",
                "value": "15th",
                "title_uz": "Uzbekistan University Ranking",
                "title_en": "Uzbekistan University Ranking",
                "subtitle_uz": "O'zbekiston bo'yicha universitetlar reytingi",
                "subtitle_en": "National university standing in Uzbekistan",
            },
            {
                "region": "QS Central Asia",
                "value": "52nd",
                "title_uz": "Asian University Rankings - Central Asia",
                "title_en": "Asian University Rankings - Central Asia",
                "subtitle_uz": "Markaziy Osiyo mintaqaviy reytingi",
                "subtitle_en": "Regional standing across Central Asia",
            },
        ]

        sdg_rankings = [
            (1, "1001+"),
            (2, "601-800"),
            (3, "1001-1500"),
            (4, "1500+"),
            (5, "1001-1500"),
            (6, "801-1000"),
            (7, "601-800"),
            (8, "1001+"),
            (9, "801-1000"),
            (10, "1001+"),
            (11, "801-1000"),
            (12, "801+"),
            (13, "801-1000"),
            (14, "601+"),
            (15, "601-800"),
            (16, "1001+"),
        ]

        context["results_page"] = {
            "eyebrow": "Natijalar" if language_code == "uz" else "Results",
            "title": (
                "Qarshi davlat universitetining global va SDG natijalari"
                if language_code == "uz"
                else "Karshi State University global and SDG results"
            ),
            "intro": (
                "Universitetning xalqaro reytinglardagi o'rni, ta'sir ko'rsatkichlari va Barqaror rivojlanish maqsadlari bo'yicha natijalari."
                if language_code == "uz"
                else "A showcase of the university's international rankings, impact indicators, and Sustainable Development Goal results."
            ),
            "rankings_label": "Xalqaro reytinglar" if language_code == "uz" else "International rankings",
            "impact_label": "Ta'sir va kampus ko'rsatkichlari" if language_code == "uz" else "Impact and campus indicators",
            "sdg_label": "SDG natijalari" if language_code == "uz" else "SDG results",
            "sdg_intro": (
                "Quyidagi ko'rsatkichlar universitetning THE Impact Rankings doirasidagi SDG yo'nalishlari bo'yicha qayd etilgan natijalarini aks ettiradi."
                if language_code == "uz"
                else "The tiles below highlight the university's recorded standings across SDG areas in the THE Impact Rankings framework."
            ),
            "impact_cards": [
                {
                    "logo": "images/impact.png",
                    "value": "TOP 1500+",
                    "title": "THE Impact Rankings",
                    "summary": (
                        "Barqaror rivojlanish maqsadlari bo'yicha global universitetlar reytingi."
                        if language_code == "uz"
                        else "Global university ranking linked to the Sustainable Development Goals."
                    ),
                },
                {
                    "logo": "images/uigreenmetric.png",
                    "value": "#403",
                    "title": "UI GreenMetric",
                    "summary": (
                        "World University Rankings bo'yicha ekologik va yashil kampus natijasi."
                        if language_code == "uz"
                        else "Environmental and green-campus standing in the World University Rankings."
                    ),
                },
            ],
        }
        context["results_ranking_cards"] = [
            {
                "region": item["region"],
                "value": item["value"],
                "title": item[f"title_{language_code}"],
                "subtitle": item[f"subtitle_{language_code}"],
            }
            for item in ranking_cards
        ]
        context["results_sdg_cards"] = [
            {
                "number": number,
                "rank": rank,
                "title": get_sdg_goal(number, language_code)["title"],
                "image": f"images/goals/E_WEB_{number:02d}.png",
            }
            for number, rank in sdg_rankings
        ]
        return context


class AboutView(BasePortalContextMixin, TemplateView):
    template_name = "portal/about.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["values"] = localize_collection(InstitutionalValue.objects.all(), language_code)
        context["governance_roles"] = localize_collection(GovernanceRole.objects.all(), language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all(), language_code)
        return context


class GovernanceDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/governance_detail.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs["slug"]
        section = GOVERNANCE_PAGE_CONTENT.get(slug)
        if not section:
            raise Http404("Governance page not found")

        language_code = self.get_language_code()
        language_suffix = "uz" if language_code == "uz" else "en"
        context["governance_section"] = {
            "slug": slug,
            "eyebrow": section[f"eyebrow_{language_suffix}"],
            "title": section[f"title_{language_suffix}"],
            "intro": section[f"intro_{language_suffix}"],
            "sections": section[f"sections_{language_suffix}"],
            "raw_html": section.get(f"single_card_raw_{language_suffix}"),
            "single_card": slug in {"sdg-policy", "sdg-purchase", "sdg-investment", "sdg-committee", "anti-corruption", "jamoatchilik", "xotin-qizlar", "ethics-code", "talabalar-kengashi", "uglerod-emissiyalari", "disability-support-policy"},
        }
        contact_language = "uz" if language_code == "uz" else "en"
        governance_contact_panels = {
            "anti-corruption": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": ANTI_CORRUPTION_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": ANTI_CORRUPTION_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Mutaxassis ma'lumotlari" if language_code == "uz" else "View specialist details",
                "url": reverse("anti-corruption-contact"),
            },
            "disability-support-policy": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": DISABILITY_SUPPORT_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": DISABILITY_SUPPORT_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Markaz ma'lumotlari" if language_code == "uz" else "View center details",
                "url": reverse("governance-finance-contact", args=[slug]),
            },
            "sdg-investment": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": FINANCIAL_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": FINANCIAL_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Mutaxassis ma'lumotlari" if language_code == "uz" else "View specialist details",
                "url": reverse("governance-finance-contact", args=[slug]),
            },
            "sdg-purchase": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": FINANCIAL_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": FINANCIAL_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Mutaxassis ma'lumotlari" if language_code == "uz" else "View specialist details",
                "url": reverse("governance-finance-contact", args=[slug]),
            },
            "xotin-qizlar": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": WOMEN_SUPPORT_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": WOMEN_SUPPORT_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Mutaxassis ma'lumotlari" if language_code == "uz" else "View specialist details",
                "url": reverse("governance-finance-contact", args=[slug]),
            },
            "talabalar-kengashi": {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": STUDENT_UNION_CONTACT_CONTENT[contact_language]["leader_name"],
                "department": STUDENT_UNION_CONTACT_CONTENT[contact_language]["title"],
                "button_label": "Mutaxassis bilan bog'lanish" if language_code == "uz" else "Contact specialist",
                "url": reverse("governance-finance-contact", args=[slug]),
            },
        }
        if slug in governance_contact_panels:
            context["governance_contact_panel"] = governance_contact_panels[slug]
        elif context.get("footer_departments") and slug != "uglerod-emissiyalari":
            responsible_contact = context["footer_departments"][0]
            context["governance_contact_panel"] = {
                "title": "Mas'ul mutaxassis" if language_code == "uz" else "Responsible specialist",
                "name": responsible_contact.contact_person,
                "department": responsible_contact.department_name,
                "button_label": "Mutaxassis bilan bog'lanish" if language_code == "uz" else "Contact specialist",
                "url": f"mailto:{responsible_contact.email}",
            }
        if slug == "ethics-code":
            if language_code == "uz":
                context["ethics_pdf_panel"] = {
                    "title": "Mas'ul mutaxassis",
                    "description": "Yoshlar bilan ishlash bo'limi bo'yicha mas'ul mutaxassis ma'lumotlari va aloqa tafsilotlarini ushbu bo'lim orqali ko'rishingiz mumkin.",
                    "button_label": "Mutaxassis bilan bog'lanish",
                    "button_url": "/about/ethics-code/contact/",
                    "download_label": "PDF hujjatni yuklab olish",
                    "section_title": "PDF hujjat asosidagi batafsil ma'lumotlar",
                    "section_intro": "Quyida odob-axloq kodeksining PDF hujjatidan olingan asosiy bo'limlar qisqacha bayon qilingan.",
                    "items": [
                        {
                            "title": "1. Umumiy qoidalar",
                            "points": [
                                "Kodeks O'zbekiston Respublikasi qonunchiligiga asoslanib ishlab chiqilgan bo'lib, universitetning barcha xodim, talaba va doktorantlari uchun majburiydir.",
                                "Maqsadlari: milliy va umuminsoniy qadriyatlar asosida madaniyat shakllantirish, huquqbuzarliklarning oldini olish, sog'lom ijtimoiy-psixologik muhit yaratish.",
                            ],
                        },
                        {
                            "title": "2. Asosiy prinsiplar",
                            "points": [
                                "Qonuniylik РІР‚вЂќ qonunchilikka so'zsiz rioya qilish",
                                "Vatanparvarlik РІР‚вЂќ Vatanga sadoqat va xizmat burchiga sodiqlik",
                                "Adolat va halollik РІР‚вЂќ barcha munosabatlarda xolis bo'lish",
                                "Samaradorlik РІР‚вЂќ innovatsiyalar orqali faoliyatni doimiy yaxshilash",
                            ],
                        },
                        {
                            "title": "3. Korrupsiyaga qarshi kurash",
                            "points": [
                                "Korrupsiyaning har qanday shakli qat'iyan rad etiladi.",
                                "Barcha xodim va talabalar korrupsiyaga qarshi faol kurashishi shart.",
                            ],
                        },
                        {
                            "title": "4. Kiyinish va tashqi ko'rinish qoidalari",
                            "points": [
                                "Qizlar: tizzani yopuvchi yubka/shim, och bo'lmagan bluzka, to'q poyabzal",
                                "Erkaklar: klassik shim/kostyum, oq/havorang ko'ylak, soqol/soch tartibli",
                                "Taqiqlanadi: shaffof kiyim, ochiq yelka/qorin, pirsing, tatuirovka, diniy ramzlar (xoch, hijob, kipa va h.k.)",
                                "Dam olish kunlari erkin kiyim ruxsat etiladi (qoidalar doirasida)",
                            ],
                        },
                        {
                            "title": "5. Qat'iyan taqiqlangan xatti-harakatlar",
                            "points": [
                                "Giyohvand, alkogol, tamaki, vayp iste'mol qilish",
                                "Janjal, qimor, zo'ravonlik",
                                "Soxta hujjat taqdim etish yoki hujjatlarni o'zgartirish",
                                "Dars vaqtida telefon ishlatish",
                                "Ekstremistik, pornografik materiallar tarqatish",
                                "Universitetni obro'sizlantiruvchi ma'lumot ijtimoiy tarmoqlarda joylashtirish",
                            ],
                        },
                        {
                            "title": "6. O'qituvchi-talaba munosabatlari",
                            "points": [
                                "Talabalar darsga kirmay qolish va kechikishga yo'l qo'ymaydi",
                                "O'qituvchi kirganida talabalar o'rindan turadi",
                                "Akademik ta'qib (harassment) РІР‚вЂќ qat'iyan taqiqlanadi",
                                "Talabalar asosli shikoyat bilan dekanat yoki rekturat orqali murojaat qila oladi",
                            ],
                        },
                        {
                            "title": "7. Rahbariyat majburiyatlari",
                            "points": [
                                "Qarindoshlik/mahalliychilik asosida kadr tanlash taqiqlanadi",
                                "Xodimlarga psixologik yoki jismoniy ta'sir ko'rsatish taqiqlanadi",
                                "Qulay ish sharoitlari (kompyuter, internet, kutubxona) ta'minlanishi shart",
                            ],
                        },
                        {
                            "title": "8. Rag'batlantirish va javobgarlik",
                            "points": [
                                "Kodeksga rioya qilganlar moddiy yoki ma'naviy rag'batlantiriladi",
                                "Buzganlar intizomiy javobgarlikka tortiladi",
                                "Odob-axloq komissiyasi (kamida 5 kishi) har qanday shikoyatni ko'rib chiqadi",
                            ],
                        },
                    ],
                }
            else:
                context["ethics_pdf_panel"] = {
                    "title": "Responsible specialist",
                    "description": "Use this section to view the contact details and profile of the specialist responsible for youth affairs.",
                    "button_label": "Contact specialist",
                    "button_url": "/about/ethics-code/contact/",
                    "download_label": "Download PDF document",
                    "section_title": "Detailed information based on the PDF document",
                    "section_intro": "Below is a concise summary of the main sections extracted from the code of ethics PDF.",
                    "items": [
                        {
                            "title": "1. General provisions",
                            "points": [
                                "The code is developed in accordance with the legislation of the Republic of Uzbekistan and is mandatory for all university employees, students, and doctoral candidates.",
                                "Its goals include building culture on the basis of national and universal values, preventing misconduct, and creating a healthy socio-psychological environment.",
                            ],
                        },
                        {
                            "title": "2. Core principles",
                            "points": [
                                "Legality РІР‚вЂќ unconditional compliance with legislation",
                                "Patriotism РІР‚вЂќ loyalty to the country and dedication to service",
                                "Justice and integrity РІР‚вЂќ impartiality in all relations",
                                "Efficiency РІР‚вЂќ continuous improvement through innovation",
                            ],
                        },
                        {
                            "title": "3. Anti-corruption approach",
                            "points": [
                                "Any form of corruption is strictly rejected.",
                                "All employees and students are required to actively combat corruption.",
                            ],
                        },
                        {
                            "title": "4. Dress code and appearance rules",
                            "points": [
                                "For women: knee-covering skirts/trousers, modest blouse, dark shoes",
                                "For men: classic trousers/suit, white or light-blue shirt, neat beard/hair",
                                "Prohibited: transparent clothing, exposed shoulders or abdomen, piercing, tattoos, and religious symbols (cross, hijab, kippah, etc.)",
                                "Casual clothing is allowed on days off within established rules",
                            ],
                        },
                        {
                            "title": "5. Strictly prohibited actions",
                            "points": [
                                "Consumption of drugs, alcohol, tobacco, or vape products",
                                "Fighting, gambling, and violence",
                                "Submitting forged documents or altering official records",
                                "Using phones during class",
                                "Distributing extremist or pornographic materials",
                                "Posting information on social media that damages the university's reputation",
                            ],
                        },
                        {
                            "title": "6. Teacher-student relations",
                            "points": [
                                "Students must not skip classes or arrive late",
                                "Students stand when a teacher enters the classroom",
                                "Academic harassment is strictly prohibited",
                                "Students may submit justified complaints through the dean's office or rectorate",
                            ],
                        },
                        {
                            "title": "7. Responsibilities of leadership",
                            "points": [
                                "Recruitment based on kinship or local favoritism is prohibited",
                                "Psychological or physical pressure on employees is prohibited",
                                "Proper working conditions must be ensured, including computers, internet, and library access",
                            ],
                        },
                        {
                            "title": "8. Incentives and accountability",
                            "points": [
                                "Those who comply with the code may receive material or moral encouragement",
                                "Violators are subject to disciplinary responsibility",
                                "The ethics commission, composed of at least 5 members, reviews any complaint",
                            ],
                        },
                    ],
                }
            context["ethics_pdf_url"] = "/about/ethics-code/document/"
            context["ethics_pdf_download_url"] = "/about/ethics-code/document/?download=1"
        return context


class AntiCorruptionContactView(BasePortalContextMixin, TemplateView):
    template_name = "portal/anti_corruption_contact.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        content = ANTI_CORRUPTION_CONTACT_CONTENT["uz" if language_code == "uz" else "en"]
        content = {
            **content,
            "image_url": "/static/images/staff/korrupsiya.jpg",
            "back_url": "/about/anti-corruption/",
            "back_label": "Korrupsiyaga qarshi siyosat sahifasiga qaytish" if language_code == "uz" else "Back to anti-corruption policy",
            "cache_key": "anti-corruption-contact-v2",
        }
        context["department_contact_page"] = content
        return context


class GovernanceFinanceContactView(BasePortalContextMixin, TemplateView):
    template_name = "portal/anti_corruption_contact.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        slug = kwargs["slug"]
        governance_contact_content = {
            "sdg-investment": FINANCIAL_CONTACT_CONTENT,
            "sdg-purchase": FINANCIAL_CONTACT_CONTENT,
            "xotin-qizlar": WOMEN_SUPPORT_CONTACT_CONTENT,
            "ethics-code": YOUTH_AFFAIRS_CONTACT_CONTENT,
            "jamoatchilik": TRADE_UNION_CONTACT_CONTENT,
            "disability-support-policy": DISABILITY_SUPPORT_CONTACT_CONTENT,
            "talabalar-kengashi": STUDENT_UNION_CONTACT_CONTENT,
        }
        if slug not in governance_contact_content:
            raise Http404("Governance contact page not found")

        content = governance_contact_content[slug]["uz" if language_code == "uz" else "en"]
        content = {
            **content,
            "back_url": f"/about/{slug}/",
            "back_label": "Boshqaruv sahifasiga qaytish" if language_code == "uz" else "Back to governance",
            "cache_key": f"{slug}-contact-v3",
        }
        context["department_contact_page"] = content
        return context


class GovernanceRoadmapView(BasePortalContextMixin, TemplateView):
    template_name = "portal/governance_roadmap.html"
    page_key = "about"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs["slug"]
        if slug != "disability-support-policy":
            raise Http404("Governance roadmap page not found")

        language_code = self.get_language_code()
        roadmap_content = DISABILITY_SUPPORT_ROADMAP_CONTENT["uz" if language_code == "uz" else "en"]
        context["roadmap_page"] = {
            **roadmap_content,
            "back_url": reverse("governance-detail", args=[slug]),
            "back_label": "Siyosat sahifasiga qaytish" if language_code == "uz" else "Back to policy",
            "contact_url": reverse("governance-finance-contact", args=[slug]),
            "contact_label": "Markaz ma'lumotlari" if language_code == "uz" else "View center details",
            "cache_key": "disability-support-roadmap-v1",
        }
        return context


class SearchView(BasePortalContextMixin, TemplateView):
    template_name = "portal/search_results.html"
    page_key = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        query = self.request.GET.get("q", "").strip()
        search_sections = build_search_sections(language_code, query)
        suggested_sections = build_search_sections(language_code, "")[:4] if query and not search_sections else []

        context.update(
            {
                "active_page": "",
                "search_query": query,
                "search_sections": search_sections,
                "search_total_results": sum(len(section["items"]) for section in search_sections),
                "suggested_search_sections": suggested_sections,
            }
        )
        return context


def ethics_code_document(request):
    if not ETHICS_CODE_PDF_PATH.exists():
        raise Http404("Ethics code PDF not found")

    response = FileResponse(ETHICS_CODE_PDF_PATH.open("rb"), content_type="application/pdf")
    filename = ETHICS_CODE_PDF_PATH.name
    if request.GET.get("download") == "1":
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
    else:
        response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response


class ProgramsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/programs.html"
    page_key = "programs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["sdg_goals"] = [build_sdg_goal(item, language_code) for item in SDG_CONTENT]
        return context


class SDGDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sdg_detail.html"
    page_key = "programs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        number = kwargs["number"]
        goal = get_sdg_goal(number, language_code)
        context["goal"] = goal
        context["previous_goal"] = number - 1 if number > 1 else None
        context["next_goal"] = number + 1 if number < 17 else None
        context["goal_work_items"] = SDGWorkItem.objects.filter(goal_number=number)

        if number == 1 and language_code == "uz":
            context["detail_content"] = SDG_1_DETAIL_UZ_CLEAN
        elif number == 2 and language_code == "uz":
            context["detail_content"] = SDG_2_DETAIL_UZ_CLEAN
        elif number == 3 and language_code == "uz":
            context["detail_content"] = SDG_3_DETAIL_UZ_CLEAN
        elif number == 4 and language_code == "uz":
            context["detail_content"] = SDG_4_DETAIL_UZ_CLEAN
        elif number == 5 and language_code == "uz":
            context["detail_content"] = SDG_5_DETAIL_UZ_CLEAN
        elif number == 6 and language_code == "uz":
            context["detail_content"] = SDG_6_DETAIL_UZ_CLEAN
        elif number == 7 and language_code == "uz":
            context["detail_content"] = SDG_7_DETAIL_UZ_CLEAN
        elif number == 8 and language_code == "uz":
            context["detail_content"] = SDG_8_DETAIL_UZ_CLEAN
        elif number == 9 and language_code == "uz":
            context["detail_content"] = SDG_9_DETAIL_UZ_CLEAN
        elif number == 10 and language_code == "uz":
            context["detail_content"] = SDG_10_DETAIL_UZ_CLEAN
        elif number == 11 and language_code == "uz":
            context["detail_content"] = SDG_11_DETAIL_UZ_CLEAN
        elif number == 12 and language_code == "uz":
            context["detail_content"] = SDG_12_DETAIL_UZ_CLEAN
        elif number == 13 and language_code == "uz":
            context["detail_content"] = SDG_13_DETAIL_UZ_CLEAN
        elif number == 14 and language_code == "uz":
            context["detail_content"] = SDG_14_DETAIL_UZ_CLEAN
        elif number == 15 and language_code == "uz":
            context["detail_content"] = SDG_15_DETAIL_UZ_CLEAN
        elif number == 16 and language_code == "uz":
            context["detail_content"] = SDG_16_DETAIL_UZ_CLEAN
        elif number == 17 and language_code == "uz":
            context["detail_content"] = SDG_17_DETAIL_UZ_CLEAN
        else:
            context["detail_content"] = {
                "hero_title": goal["title"],
                "idea_title": "Asosiy gРІР‚Вoya" if language_code == "uz" else "Core idea",
                "idea_text": goal["description"],
                "sections": [
                    {
                        "title": "Umumiy maРІР‚в„ўlumot" if language_code == "uz" else "Overview",
                        "paragraphs": [
                            goal["description"],
                            "Mazkur maqsad universitetning ilmiy izlanishlari, taРІР‚в„ўlim dasturlari va jamoatchilik bilan ishlash tashabbuslari orqali qoРІР‚Вllab-quvvatlanadi."
                            if language_code == "uz"
                            else "This goal is supported through the university's research agenda, educational programs, and community engagement initiatives.",
                        ],
                    },
                    {
                        "title": "Asosiy yoРІР‚Вnalishlar" if language_code == "uz" else "Priority directions",
                        "bullets": [
                            "taРІР‚в„ўlim, tadqiqot va kampus boshqaruvida integratsiya"
                            if language_code == "uz"
                            else "integration across teaching, research, and campus management",
                            "maРІР‚в„ўlumotlarga asoslangan institutsional qarorlar"
                            if language_code == "uz"
                            else "data-informed institutional decision-making",
                            "mahalliy va xalqaro hamkorlik"
                            if language_code == "uz"
                            else "local and international partnerships",
                        ],
                    },
                ],
            }
        return context


class SDGUpdatesView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sdg_updates.html"
    page_key = "programs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        number = kwargs["number"]
        goal = get_sdg_goal(number, language_code)
        context["goal"] = goal
        context["previous_goal"] = number - 1 if number > 1 else None
        context["next_goal"] = number + 1 if number < 17 else None
        context["goal_news_items"] = localize_collection(NewsArticle.objects.filter(sdg_goal=number), language_code)
        context["goal_work_items"] = SDGWorkItem.objects.filter(goal_number=number)
        return context


RESEARCH_CARD_CONTENT = {
    "sdg-publications": {
        "eyebrow_uz": "Tadqiqot va ta'lim",
        "eyebrow_en": "Research & Education",
        "title_uz": "SDG nashrlari",
        "title_en": "SDG publications",
        "intro_uz": "Barqaror rivojlanish maqsadlari bilan bog'liq maqolalar, hisobotlar va ilmiy nashrlar.",
        "intro_en": "Published articles, reports, and academic outputs connected to the Sustainable Development Goals.",
        "body_uz": [
            "Ushbu bo'lim universitetda Barqaror rivojlanish maqsadlari bilan bog'liq tayyorlangan ilmiy maqolalar, nashrlar, tahliliy sharhlar va institutsional hisobotlarni jamlaydi.",
            "Sahifa ilmiy natijalarni bir joyda ko'rsatish, tadqiqot faoliyatini tizimlashtirish va manfaatdor tomonlar uchun ochiq akademik ma'lumotlar maydonini yaratishga xizmat qiladi.",
        ],
        "body_en": [
            "This section brings together scientific articles, publications, analytical reviews, and institutional reports prepared at the university in connection with the Sustainable Development Goals.",
            "The page is designed to present academic outputs in one place, structure research activity, and provide an open knowledge space for stakeholders.",
        ],
    },
    "research-centers": {
        "eyebrow_uz": "Tadqiqot va ta'lim",
        "eyebrow_en": "Research & Education",
        "title_uz": "Tadqiqot markazlari",
        "title_en": "Research centers",
        "intro_uz": "Barqarorlikka yo'naltirilgan tadqiqot va innovatsiyalarni qo'llab-quvvatlovchi universitet markazlari va laboratoriyalari.",
        "intro_en": "University research centers and laboratories supporting sustainability-focused inquiry and innovation.",
        "body_uz": [
            "Ushbu bo'lim universitet tarkibidagi tadqiqot markazlari, ilmiy laboratoriyalar va barqarorlik yo'nalishidagi ilmiy platformalarni yoritadi.",
            "Markazlar ilmiy salohiyatni oshirish, fanlararo hamkorlikni kuchaytirish hamda amaliy va nazariy tadqiqotlarni rivojlantirish uchun xizmat qiladi.",
        ],
        "body_en": [
            "This section highlights the university's research centers, scientific laboratories, and research platforms working in sustainability-related areas.",
            "These centers support academic capacity, strengthen interdisciplinary cooperation, and advance both applied and theoretical research activity.",
        ],
        "cards_uz": RESEARCH_CENTER_CARDS,
        "cards_en": RESEARCH_CENTER_CARDS_EN,
    },
    "sustainability-subjects": {
        "eyebrow_uz": "Tadqiqot va ta'lim",
        "eyebrow_en": "Research & Education",
        "title_uz": "Barqarorlik oid fanlar",
        "title_en": "Subjects related to sustainability",
        "intro_uz": "Barqarorlik tamoyillarini turli fakultetlar kesimida qamrab oluvchi fanlar ro'yxati va yo'nalishlari.",
        "intro_en": "An overview of courses that integrate sustainability principles across multiple faculties and disciplines.",
        "body_uz": [
            "Qarshi davlat universitetida jami 169 ta fan barqarorlik, atrof-muhitni muhofaza qilish, qayta tiklanuvchi energiya, biotexnologiya va ijtimoiy mas'uliyat bilan bog'liq mavzularni o'z ichiga oladi.",
            "Mazkur fanlar muhandislik va texnologiya, kimyo va biologiya, geografiya va Yer fanlari, fizika, iqtisodiyot, tibbiyot hamda pedagogika yo'nalishlari bo'yicha barqarorlik yondashuvlarini ta'limga integratsiya qiladi.",
        ],
        "body_en": [
            "Karshi State University offers a total of 169 courses that incorporate sustainability, environmental protection, renewable energy, biotechnology, and social responsibility topics.",
            "These courses embed sustainability concepts across engineering and technology, chemistry and biology, geography and earth sciences, physics, economics, medicine, and pedagogy.",
        ],
        "raw_html_uz": SUSTAINABILITY_SUBJECTS_RAW_HTML_UZ,
        "raw_html_en": SUSTAINABILITY_SUBJECTS_RAW_HTML_EN,
    },
    "sustainability-study-programs": {
        "eyebrow_uz": "Tadqiqot va ta'lim",
        "eyebrow_en": "Research & Education",
        "title_uz": "Barqarorlikka oid ta'lim dasturlari",
        "title_en": "Study programs related to sustainability",
        "intro_uz": "Barqaror rivojlanish bilan bevosita bog'liq fakultetlar va ta'lim dasturlari haqida umumiy ma'lumot.",
        "intro_en": "An overview of faculties and study programs directly connected to sustainability-oriented education.",
        "body_uz": [
            "Universitetdagi 7 ta fakultet barqarorlik bilan bevosita bog'liq ta'lim dasturlarini taklif etadi.",
            "Ushbu dasturlar atrof-muhitni muhofaza qilish, qayta tiklanuvchi energiya, barqaror qishloq xo'jaligi, ta'lim va ijtimoiy farovonlikni qamrab oladi.",
        ],
        "body_en": [
            "A total of seven faculties at the university offer study programs directly related to sustainability.",
            "These programs cover environmental protection, renewable energy, sustainable agriculture, education, and social well-being.",
        ],
        "raw_html_uz": SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_UZ,
        "raw_html_en": SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_EN,
    },
    "startups-and-grants": {
        "eyebrow_uz": "Tadqiqot va ta'lim",
        "eyebrow_en": "Research & Education",
        "title_uz": "Startaplar va grantlar",
        "title_en": "Start-ups and grants",
        "intro_uz": "Tadqiqot va rivojlanish bilan bog'liq innovatsion loyihalar, startap tashabbuslari va grant imkoniyatlari.",
        "intro_en": "Innovation projects, start-up initiatives, and grant opportunities linked to research and development.",
        "body_uz": [],
        "body_en": [],
        "projects_uz": [
            {
                "label": "1) Innovatsion loyiha",
                "title_label": "Nomi",
                "title": "РІР‚СљEnergiya tejovchi texnologiyalarda foydalaniladigan silidsid metall va yarimoРІР‚Вtkazgich birikmalar asosidagi nanooРІР‚Вlchamli plyonkalarning optik va elektrofizik xossalarini tadqiq etishРІР‚Сњ",
                "details": [
                    {"label": "Sana", "value": "10-avgust 2024"},
                    {"label": "Loyiha rahbari", "value": "Normuradov Muradulla, fizika-matematika fanlari doktori, professor"},
                    {"label": "Fan yoРІР‚Вnalishi", "value": "Matematika va fizika, mexanika fanlari"},
                    {"label": "Qisqacha mazmuni", "value": "loyiha kremniy monokristallari yuzasida hosil boРІР‚Вladigan oРІР‚Вtish metallari, ularning silisidlari va nanooРІР‚Вlchamli yupqa plyonkalar xossalarini oРІР‚Вrganishga qaratilgan. Asosiy urgРІР‚Вu РІР‚вЂќ qattiq jismli elektronika uchun noyob xossalarga ega materiallar yaratish, ion-plazma usulida olingan yupqa plyonkalar asosida yangi qurilmalar ishlab chiqish."},
                    {"label": "Ijrochi tashkilot", "value": "Qarshi davlat universiteti"},
                    {"label": "Loyiha qiymati", "value": "1 936 350 000 soРІР‚Вm."},
                ],
            },
            {
                "label": "2) Amaliy loyiha",
                "title_label": "Nomi",
                "title": "РІР‚СљQashqadaryo viloyati hududida tarqalgan isteРІР‚в„ўmolbop, dorivor qoРІР‚Вziqorinlar va ularni sunРІР‚в„ўiy ozuqa muhitlarida yetishtirish texnologiyasini ishlab chiqishРІР‚Сњ",
                "details": [
                    {"label": "Sana", "value": "10-avgust 2024"},
                    {"label": "Loyiha rahbari", "value": "dots. Sherqulova Jamila Payanovna"},
                    {"label": "Fan yoРІР‚Вnalishi", "value": "Biotexnologiya va mikologiya"},
                    {"label": "Qisqacha mazmuni", "value": "loyiha isteРІР‚в„ўmolbop va dorivor zamburugРІР‚Вlarni mahalliy sharoitda ilmiy asosda yetishtirish texnologiyasini ishlab chiqishga qaratilgan. Unda sifatli oziq-ovqat va tabiiy dori vositalariga ehtiyoj ortayotgani, Qashqadaryoda bu yoРІР‚Вnalishda rejali mikologik tadqiqotlar yetarli emasligi, sof kultura kolleksiyasini yaratish va arzon substratlar asosida yuqori hosil olish zarurligi taРІР‚в„ўkidlangan."},
                    {"label": "Ijrochi tashkilot", "value": "Qarshi davlat universiteti"},
                    {"label": "Loyiha qiymati", "value": "981 920 000 soРІР‚Вm."},
                ],
            },
            {
                "label": "3) Startup loyiha",
                "title_label": "Nomi",
                "title": "РІР‚СљClean WaterРІР‚Сњ",
                "details": [
                    {"label": "Sana", "value": "10-avgust 2024"},
                    {"label": "Loyiha rahbari", "value": "Shamsiddinova Shahrizoda Baxtiyor qizi"},
                    {"label": "Qisqacha mazmuni", "value": "loyiha suv oРІР‚Вtlari yordamida suvni biologik usulda tozalashga qaratilgan. Unda chiqindi suvlarni organo-minerallar, ogРІР‚Вir metallar, sianidlar, neft mahsulotlari va patogen mikroorganizmlardan tozalash, shuningdek, qishloq xoРІР‚Вjaligi, baliqchilik, parrandachilik va chorvachilik uchun foydali resurs olish koРІР‚Вzda tutilgan."},
                    {"label": "Hamkor tashkilot", "value": "Qarshi davlat universiteti"},
                    {"label": "Loyiha qiymati", "value": "177 410 000 soРІР‚Вm."},
                ],
            },
            {
                "label": "4) Xalqaro loyiha",
                "title_label": "Nomi",
                "title": "РІР‚СљAccess Microscholarship ProgramРІР‚Сњ",
                "details": [
                    {"label": "Sana", "value": "10-avgust 2024"},
                    {"label": "Loyiha rahbari", "value": "Musayeva DilsoРІР‚Вz Tuychiyevna, PhD"},
                    {"label": "Qisqacha mazmuni", "value": "loyiha AQShning OРІР‚Вzbekistondagi Elchixonasi moliyaviy koРІР‚Вmagida, Amerika kengashlari rahbarligida amalga oshiriladi. Qarshi shahridagi umumiy oРІР‚Вrta taРІР‚в„ўlim maktablarida oРІР‚Вqiyotgan, kam taРІР‚в„ўminlangan va ijtimoiy himoyaga muhtoj oilalar farzandlarining ingliz tili malakasini oshirishga qaratilgan. Darslik va oРІР‚Вquv jihozlari xarajatlari loyiha mablagРІР‚Вlari hisobidan qoplanadi."},
                    {"label": "Hamkor tashkilot", "value": "Qarshi davlat universiteti"},
                    {"label": "Loyiha qiymati", "value": "64 000 AQSH dollari."},
                ],
            },
        ],
        "projects_en": [
            {
                "label": "1) Innovation project",
                "title_label": "Title",
                "title": "РІР‚СљResearch on the optical and electrophysical properties of nanoscale films based on silicide metals and semiconductor compounds used in energy-saving technologiesРІР‚Сњ",
                "details": [
                    {"label": "Date", "value": "August 10, 2024"},
                    {"label": "Project leader", "value": "Normuradov Muradulla, Doctor of Physical and Mathematical Sciences, Professor"},
                    {"label": "Scientific field", "value": "Mathematics, physics, and mechanics"},
                    {"label": "Summary", "value": "The project is aimed at studying transition metals formed on the surface of silicon single crystals, their silicides, and nanoscale thin films. The main focus is on creating materials with unique properties for solid-state electronics and developing new devices based on thin films obtained through ion-plasma methods."},
                    {"label": "Implementing institution", "value": "Karshi State University"},
                    {"label": "Project value", "value": "1,936,350,000 UZS."},
                ],
            },
            {
                "label": "2) Applied project",
                "title_label": "Title",
                "title": "РІР‚СљDevelopment of technology for cultivating edible and medicinal mushrooms widespread in Kashkadarya region in artificial nutrient mediaРІР‚Сњ",
                "details": [
                    {"label": "Date", "value": "August 10, 2024"},
                    {"label": "Project leader", "value": "Assoc. Prof. Sherqulova Jamila Payanovna"},
                    {"label": "Scientific field", "value": "Biotechnology and mycology"},
                    {"label": "Summary", "value": "The project focuses on developing a scientifically grounded local technology for cultivating edible and medicinal fungi. It emphasizes the growing need for quality food and natural remedies, the limited planned mycological research in Kashkadarya, and the need to create a pure culture collection and achieve high yields using low-cost substrates."},
                    {"label": "Implementing institution", "value": "Karshi State University"},
                    {"label": "Project value", "value": "981,920,000 UZS."},
                ],
            },
            {
                "label": "3) Startup project",
                "title_label": "Title",
                "title": "РІР‚СљClean WaterРІР‚Сњ",
                "details": [
                    {"label": "Date", "value": "August 10, 2024"},
                    {"label": "Project leader", "value": "Shamsiddinova Shahrizoda Baxtiyor qizi"},
                    {"label": "Summary", "value": "The project is aimed at biologically purifying water with the help of algae. It is designed to clean wastewater from organo-minerals, heavy metals, cyanides, petroleum products, and pathogenic microorganisms, while also generating useful resources for agriculture, fisheries, poultry farming, and livestock production."},
                    {"label": "Partner institution", "value": "Karshi State University"},
                    {"label": "Project value", "value": "177,410,000 UZS."},
                ],
            },
            {
                "label": "4) International project",
                "title_label": "Title",
                "title": "РІР‚СљAccess Microscholarship ProgramРІР‚Сњ",
                "details": [
                    {"label": "Date", "value": "August 10, 2024"},
                    {"label": "Project leader", "value": "Musayeva DilsoРІР‚Вz Tuychiyevna, PhD"},
                    {"label": "Summary", "value": "The project is implemented under the leadership of American Councils with financial support from the U.S. Embassy in Uzbekistan. It is aimed at improving English language proficiency among schoolchildren in Karshi city from low-income and socially vulnerable families. The costs of textbooks and educational materials are covered through project funds."},
                    {"label": "Partner institution", "value": "Karshi State University"},
                    {"label": "Project value", "value": "64,000 USD."},
                ],
            },
        ],
    },
}


class ResearchView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["page_content"] = build_page_content_fallback(
            eyebrow="Tadqiqot" if language_code == "uz" else "Research",
            title="Tadqiqot va ta'lim" if language_code == "uz" else "Research & Education",
            intro=(
                "Universitetning BRM nashrlari, tadqiqot markazlari, barqarorlikka oid fanlari, ta'lim dasturlari va grant/startap tashabbuslari."
                if language_code == "uz"
                else "A consolidated view of the university's SDG publications, research centers, sustainability-related subjects, academic programs, and start-up or grant activity."
            ),
            supporting_title="Tadqiqot izohi" if language_code == "uz" else "Research note",
            supporting_text=(
                "Bu bo'lim universitetning ilmiy salohiyati, ta'lim integratsiyasi va BRM yo'nalishlari bo'yicha amaliy natijalarini bir joyda ko'rsatadi."
                if language_code == "uz"
                else "This section brings together the university's research capacity, education integration, and practical results related to the SDGs."
            ),
        )
        context["research_cards"] = [
            {
                "slug": "sdg-publications",
                "title": "SDG publications" if language_code == "en" else "SDG nashrlari",
                "summary": (
                    "Published articles, reports, and academic outputs connected to the Sustainable Development Goals."
                    if language_code == "en"
                    else "Barqaror rivojlanish maqsadlari bilan bog'liq maqolalar, hisobotlar va ilmiy nashrlar."
                ),
            },
            {
                "slug": "research-centers",
                "title": "Research centers" if language_code == "en" else "Tadqiqot markazlari",
                "summary": (
                    "University research centers and laboratories supporting sustainability-focused inquiry and innovation."
                    if language_code == "en"
                    else "Barqarorlikka yo'naltirilgan tadqiqot va innovatsiyalarni qo'llab-quvvatlovchi universitet markazlari va laboratoriyalari."
                ),
            },
            {
                "slug": "sustainability-subjects",
                "title": "Subjects related to sustainability" if language_code == "en" else "Barqarorlik oid fanlar",
                "summary": (
                    "Courses across multiple faculties that integrate sustainability, environmental protection, renewable energy, and social responsibility."
                    if language_code == "en"
                    else "Turli fakultetlarda barqarorlik, ekologiya, qayta tiklanuvchi energiya va ijtimoiy mas'uliyatni qamrab oluvchi fanlar."
                ),
            },
            {
                "slug": "sustainability-study-programs",
                "title": "Study programs related to sustainability" if language_code == "en" else "Barqarorlikka oid ta'lim dasturlari",
                "summary": (
                    "Multidisciplinary study programs that connect education with sustainable development, green economy, and environmental responsibility."
                    if language_code == "en"
                    else "Barqaror rivojlanish, yashil iqtisodiyot va ekologik mas'uliyat bilan bog'liq ko'p tarmoqli ta'lim dasturlari."
                ),
            },
            {
                "slug": "startups-and-grants",
                "title": "Start-ups and grants" if language_code == "en" else "Startaplar va grantlar",
                "summary": (
                    "Innovation projects, start-up initiatives, and grant opportunities linked to research and development."
                    if language_code == "en"
                    else "Tadqiqot va rivojlanish bilan bog'liq innovatsion loyihalar, startap tashabbuslari va grant imkoniyatlari."
                ),
            },
        ]
        return context


class ResearchCardDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research_card_detail.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        slug = kwargs["slug"]
        content = RESEARCH_CARD_CONTENT.get(slug)
        if not content:
            raise Http404("Research detail page not found")

        suffix = "uz" if language_code == "uz" else "en"
        cards = content.get(f"cards_{suffix}", [])
        if slug == "sdg-publications":
            sdg_data = get_sdg_publication_data()
            cards = [
                {
                    "slug": f"sdg-{goal_number}",
                    "title": goal_data[f"title_{suffix}"],
                    "summary": (
                        f"{len(goal_data['articles'])} publication(s) available."
                        if suffix == "en"
                        else f"{len(goal_data['articles'])} ta maqola nomi mavjud."
                    ),
                    "url": reverse("sdg-publication-detail", kwargs={"goal_number": goal_number}),
                }
                for goal_number, goal_data in sdg_data.items()
            ]
        context["research_detail"] = {
            "slug": slug,
            "eyebrow": content[f"eyebrow_{suffix}"],
            "title": content[f"title_{suffix}"],
            "intro": content[f"intro_{suffix}"],
            "body": content[f"body_{suffix}"],
            "raw_html": content.get(f"raw_html_{suffix}"),
            "projects": content.get(f"projects_{suffix}", []),
            "cards": [
                {
                    **item,
                    "url": item.get("url", reverse("research-center-detail", kwargs={"center_slug": item["slug"]})),
                }
                for item in cards
            ],
            "article_titles": [],
        }
        return context


class ResearchCenterDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research_card_detail.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        center_slug = kwargs["center_slug"]
        center = RESEARCH_CENTER_DETAILS.get(center_slug)
        if not center:
            raise Http404("Research center page not found")

        if language_code == "en":
            center_content = RESEARCH_CENTER_TRANSLATIONS_EN.get(center_slug, {})
        else:
            center_content = center

        context["research_detail"] = {
            "slug": center_slug,
            "eyebrow": "Research & Education" if language_code == "en" else "Tadqiqot va ta'lim",
            "title": center_content.get("title", center["title"]),
            "intro": center_content.get("summary", center["summary"]),
            "body": center_content.get("body", center["body"]),
            "raw_html": None,
            "projects": [],
            "cards": [],
            "article_titles": [],
        }
        return context


class SDGPublicationDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research_card_detail.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        suffix = "uz" if language_code == "uz" else "en"
        goal_number = kwargs["goal_number"]
        goal_data = get_sdg_publication_data().get(goal_number)
        if not goal_data:
            raise Http404("SDG publication page not found")

        context["research_detail"] = {
            "slug": f"sdg-{goal_number}",
            "eyebrow": "Research & Education" if language_code == "en" else "Tadqiqot va ta'lim",
            "title": goal_data[f"title_{suffix}"],
            "intro": goal_data[f"intro_{suffix}"],
            "body": (
                []
                if goal_data["articles"]
                else (
                    ["No publication titles were found for this SDG yet."]
                    if language_code == "en"
                    else ["Bu SDG uchun hozircha maqola nomlari topilmadi."]
                )
            ),
            "raw_html": None,
            "projects": [],
            "cards": [],
            "article_titles": goal_data["articles"],
        }
        return context


class EducationView(BasePortalContextMixin, TemplateView):
    template_name = "portal/education.html"
    page_key = "education"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_initiatives"] = localize_collection(EducationInitiative.objects.filter(featured=True), language_code)
        context["initiatives"] = localize_collection(EducationInitiative.objects.all(), language_code)
        return context


class SustainabilityView(BasePortalContextMixin, TemplateView):
    template_name = "portal/sustainability.html"
    page_key = "sustainability"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["page_content"] = build_page_content_fallback(
            eyebrow="Kampus" if language_code == "uz" else "Campus",
            title="Kampus barqarorligi" if language_code == "uz" else "Campus sustainability",
            intro=(
                "Universitet kampusida infratuzilma, energiya, chiqindilar, suv va transport yo'nalishlari bo'yicha barqaror boshqaruv choralarini ko'rsatadigan asosiy bo'limlar."
                if language_code == "uz"
                else "Core sections that present how the university manages infrastructure, energy, waste, water, and transport across the campus."
            ),
            supporting_title="Kampus izohi" if language_code == "uz" else "Campus note",
            supporting_text=(
                "Bu sahifa kampus faoliyatining asosiy ekologik va operatsion yo'nalishlarini soddalashtirilgan ko'rinishda jamlaydi."
                if language_code == "uz"
                else "This page brings together the main environmental and operational areas of campus activity in a clear, simplified structure."
            ),
        )
        context["campus_sections"] = [
            {
                "title": "Joylashuv & Infratuzilma" if language_code == "uz" else "Location & Infrastructure",
                "summary": (
                    "Kampus hududi, bino va inshootlar, yashil maydonlar hamda infratuzilma quvvatlari bo'yicha asosiy ma'lumotlar."
                    if language_code == "uz"
                    else "Core information on the campus site, buildings, green areas, and infrastructure capacity."
                ),
            },
            {
                "title": "Energiya & iqlim o'zgarishi" if language_code == "uz" else "Energy & Climate Change",
                "summary": (
                    "Energiya samaradorligi, elektr va issiqlik iste'moli, quyosh energiyasi va emissiyalarni kamaytirish choralarini qamrab oladi."
                    if language_code == "uz"
                    else "Covers energy efficiency, electricity and heat use, solar energy, and measures to reduce emissions."
                ),
            },
            {
                "title": "Chiqindilar" if language_code == "uz" else "Waste",
                "summary": (
                    "Maishiy va operatsion chiqindilarni boshqarish, saralash, qayta ishlash va ekologik nazorat bo'yicha yo'nalish."
                    if language_code == "uz"
                    else "Focuses on operational and household waste management, sorting, recycling, and environmental control."
                ),
            },
            {
                "title": "Suv" if language_code == "uz" else "Water",
                "summary": (
                    "Suv resurslarini tejash, tarmoqlarni monitoring qilish va samarali foydalanish bo'yicha tashabbuslar."
                    if language_code == "uz"
                    else "Highlights initiatives for water conservation, network monitoring, and efficient use."
                ),
            },
            {
                "title": "Transport" if language_code == "uz" else "Transport",
                "summary": (
                    "Talaba va xodimlar qatnovi, kampus ichki harakati va barqaror transport yechimlari bo'yicha ma'lumotlar."
                    if language_code == "uz"
                    else "Presents information on student and staff mobility, internal campus movement, and sustainable transport solutions."
                ),
            },
        ]
        return context


class ReportsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/reports.html"
    page_key = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["page_content"] = build_page_content_fallback(
            eyebrow="Hisobotlar" if language_code == "uz" else "Reports",
            title="Tahlillar va hisobotlar" if language_code == "uz" else "Insights & Reports",
            intro=(
                "Universitetning emissiya, moliya va umumiy barqarorlik natijalari bo'yicha asosiy hujjatlari va yuklab olinadigan hisobotlari."
                if language_code == "uz"
                else "Core documents and downloadable reports covering the university's emissions, finance, and overall sustainability performance."
            ),
            supporting_title="Hisobot izohi" if language_code == "uz" else "Reporting note",
            supporting_text=(
                "Bu sahifa tez ko'zdan kechirish, rasmiy ma'lumot olish va kerakli hisobotlarni yuklab olish uchun tartiblangan."
                if language_code == "uz"
                else "This page is structured for quick review, official reference, and direct access to key downloadable reports."
            ),
        )
        context["report_cards"] = [
            {
                "slug": "governance-meeting-minutes",
                "title": "Boshqaruv yig'ilishlari bayonnomalari" if language_code == "uz" else "Governance meeting minutes",
                "summary": (
                    "Boshqaruv yig'ilishlari, muhokama qilingan masalalar va qabul qilingan qarorlar bo'yicha rasmiy bayonnomalar."
                    if language_code == "uz"
                    else "Official minutes of governance meetings, including agenda items discussed and decisions adopted."
                ),
            },
            {
                "slug": "greenhouse-gases",
                "title": "Issiqxona gazlari emissiyalari hisoboti" if language_code == "uz" else "Greenhouse gas emissions report",
                "summary": (
                    "Universitet faoliyatidagi issiqxona gazlari, emissiya ko'rsatkichlari va ekologik monitoring bo'yicha ma'lumotlar."
                    if language_code == "uz"
                    else "Information on greenhouse gas emissions, climate indicators, and environmental monitoring across the university."
                ),
            },
            {
                "slug": "financial-report",
                "title": "Moliyaviy hisobot" if language_code == "uz" else "Financial report",
                "summary": (
                    "Moliyaviy faoliyat, mablag'lar taqsimoti va institutsional xarajatlar bo'yicha asosiy hisobotlar."
                    if language_code == "uz"
                    else "Key reports on financial activity, fund allocation, and institutional expenditure."
                ),
            },
            {
                "slug": "sustainability-report",
                "title": "Barqarorlik hisoboti" if language_code == "uz" else "Sustainability report",
                "summary": (
                    "Barqaror rivojlanish maqsadlari, tashabbuslar va universitetning umumiy barqarorlik natijalari bo'yicha hisobot."
                    if language_code == "uz"
                    else "A report covering sustainability goals, initiatives, and the university's overall sustainability performance."
                ),
            },
        ]
        return context


REPORT_INSIGHT_CARD_CONTENT = {
    "governance-meeting-minutes": {
        "eyebrow_uz": "Hisobotlar",
        "eyebrow_en": "Reports",
        "title_uz": "Boshqaruv yig'ilishlari bayonnomalari",
        "title_en": "Governance meeting minutes",
        "intro_uz": "Universitet boshqaruvi yig'ilishlari bo'yicha qisqa bayonnomalar va qabul qilingan qarorlar jamlanmasi.",
        "intro_en": "A concise collection of governance meeting minutes and adopted decisions.",
        "show_download_cta": False,
        "sections_uz": [
            {
                "title": "2024-2025-yillar bo'yicha yig'ilishlar",
                "table_headers": ["в„–", "Sana", "Muhokama mavzusi", "Qabul qilingan qaror", "Mas'ul bo'linma"],
                "table_rows": [
                    ["1", "2025-yil fevral", "Inklyuziv ta'lim va accessibilty", "Plandagi infratuzilma moslashtirish ishlari boshlandi", "O'quv ishlari bo'yicha prorektor"],
                    ["2", "2025-yil aprel", "Energiya tejamkorligi va monitoring", "LED yoritish va energiya monitoringi jadvali tasdiqlandi", "Moliya-iqtisod ishlari bo'yicha prorektor"],
                    ["3", "2025-yil iyun", "Talabalar ishtiroki va qo'llab-quvvatlash", "Yoshlar bilan ishlash bo'yicha qo'shimcha chora-tadbirlar belgilandi", "Yoshlar masalalari bo'yicha prorektor"],
                    ["4", "2025-yil sentyabr", "Barqarorlik hisobotini tayyorlash", "Yillik hisobot tuzilmasi va muddatlari tasdiqlandi", "Barqarorlik kengashi"],
                ],
            },
            {
                "title": "Qisqa izoh",
                "paragraphs": [
                    "Bayonnomalar universitetning barqarorlik, boshqaruv va hisobot berish jarayonlarini tizimli ravishda hujjatlashtirish uchun xizmat qiladi.",
                    "Har bir yig'ilishda masalalar muhokama qilinib, bajarilish muddati, mas'ul bo'linmalar va monitoring tartibi belgilanadi.",
                ],
            },
        ],
        "sections_en": [
            {
                "title": "Meetings for 2024-2025",
                "table_headers": ["No", "Date", "Discussion topic", "Decision adopted", "Responsible unit"],
                "table_rows": [
                    ["1", "February 2025", "Inclusive education and accessibility", "Infrastructure adaptation work was launched according to the plan", "Vice-Rector for Academic Affairs"],
                    ["2", "April 2025", "Energy efficiency and monitoring", "The LED lighting and energy monitoring schedule was approved", "Vice-Rector for Finance and Economic Affairs"],
                    ["3", "June 2025", "Student engagement and support", "Additional measures for youth engagement were defined", "Vice-Rector for Youth Affairs"],
                    ["4", "September 2025", "Preparation of the sustainability report", "The annual report structure and deadlines were approved", "Sustainability Council"],
                ],
            },
            {
                "title": "Short note",
                "paragraphs": [
                    "The minutes serve to document the university's sustainability, governance, and reporting processes in a structured way.",
                    "At each meeting, agenda items are discussed and deadlines, responsible units, and monitoring procedures are defined.",
                ],
            },
        ],
    },
    "greenhouse-gases": {
        "eyebrow_uz": "Hisobotlar",
        "eyebrow_en": "Reports",
        "title_uz": "Issiqxona gazlari",
        "title_en": "Greenhouse gases",
        "intro_uz": "Qarshi davlat universitetining 2024-2025 yillar bo'yicha GHG emissiyalari hisoboti.",
        "intro_en": "Karshi State University's greenhouse gas emissions report for 2024-2025.",
        "show_download_cta": False,
        "sections_uz": [
            {
                "title": "Scope 1 - To'g'ridan-to'g'ri emissiyalar",
                "table_headers": ["No", "Emissiya manbai", "Qollash doirasi (1)", "Faoliyat malumotlari", "Birlik", "Emissiya omili", "EF birligi", "Jami emissiya (tCO2e)"],
                "table_rows": [
                    ["1", "Tabiiy gaz iste'moli", "Scope 1", "601 000", "m3", "1,9", "kgCO2e/m3", "1 141,9"],
                    ["2", "Yoqilg'i ko'mir iste'moli", "Scope 1", "7 205", "kg", "2,4", "kgCO2e/kg", "17"],
                    ["", "Jami", "", "", "", "", "TOTAL (tCO2e)", "1 159"],
                ],
            },
            {
                "title": "Scope 2 - Bilvosita energiya emissiyalari",
                "table_headers": ["No", "Emissiya manbai", "Scope (2)", "Faoliyat malumotlari", "Birlik", "Emissiya omili", "EF birligi", "Jami emissiya (tCO2e)"],
                "table_rows": [
                    ["1", "Elektr energiya iste'moli", "Scope 2", "1 543 287", "kWh", "0,4", "kgCO2e/kWh", "617,31"],
                    ["2", "Operatsional (use-phase)", "Scope 2", "1 832 706", "kWh", "0", "kgt CO2/kWh", "0"],
                    ["", "Jami", "", "", "", "", "TOTAL (tCO2e)", "617,31"],
                ],
            },
            {
                "title": "Scope 3 - Boshqa bilvosita emissiyalar",
                "table_headers": ["No", "Emission Source", "Scope (3)", "Activity Data", "Unit", "Emission Factor", "EF Unit", "Total Emissions (tCO2e)"],
                "table_rows": [
                    ["1", "Benzin", "Scope 3", "8610", "liter", "2,31", "kgCO2e/litr", "19,89"],
                    ["2", "Dizel", "Scope 3", "1766", "liter", "2,68", "kgCO2e/litr", "4,73"],
                    ["3", "Gibrid transport", "Scope 3", "11200", "km", "0.09", "kgCO2e/km", "1"],
                    ["4", "Elektr poyezdi", "Scope 3", "67000", "km", "0.035", "kgCO2e/km", "2,3"],
                    ["5", "Mahalliy avtobus", "Scope 3", "15 000", "km", "0.11", "kgCO2e/km", "1,65"],
                    ["6", "AviA qisqa masofa (<1500 km)", "Scope 3", "18 450", "km", "0.18", "kgCO2e/km", "3,3"],
                    ["7", "AviA O'rta masofa (1500-3700 km)", "Scope 3", "27 300", "km", "0.13", "kgCO2e/km", "3,55"],
                    ["8", "AviA uzoq masofa (>3700 km)", "Scope 3", "37 000", "km", "0.11", "kgCO2e/km", "4,07"],
                    ["9", "Mototsikl", "Scope 3", "5000", "km", "0,1", "kg CO2 per km", "0,5"],
                    ["10", "Aralash chiqindilarni poligonga joylashtirish", "Scope 3", "120 800,0", "kg", "500", "kg CO2e per ton", "60,4"],
                    ["11", "Qog'oz", "Scope 3", "5 900,0", "kg", "100", "kg CO2e per ton", "0,6"],
                    ["12", "Ofis jihozlari", "Scope 3", "188 153", "USD", "0,0005", "tCO2 per 1,000 currency units", "94,1"],
                    ["13", "Plastik chiqindilar", "Scope 3", "2 700,0", "kg", "400", "kg CO2e per ton", "1,1"],
                    ["14", "Oziq-ovqat", "Scope 3", "3 200,0", "kg", "700", "kg CO2e per ton", "2,2"],
                    ["15", "(IT) uskunalari", "Scope 3", "359 800", "USD", "0,0008", "tCO2 per 1,000 currency units", "287,8"],
                    ["16", "Tibbiy/laboratoriya uskunalari", "Scope 3", "61 500", "USD", "0,0012", "tCO2 per 1,000 currency units", "73,8"],
                    ["17", "Qurilish", "Scope 3", "933 641", "USD", "0,0009", "tCO2 per 1,000 currency units", "840,3"],
                    ["18", "Suv ta'minoti", "Scope 3", "45 003,0", "m3", "0,34", "kg CO2 per m3", "15,3"],
                    ["19", "Oqava suvlarni tozalash", "Scope 3", "3 540,0", "m3", "0,7", "kg CO2 per m3", "2,5"],
                    ["20", "Xodimlar qatnovi", "Scope 3", "10x2x1200x220 = 5 280 000", "km", "0,18", "kg CO2e/pax-km", "950,4"],
                    ["21", "Talabalar qatnovi", "Scope 3", "10x2x9023x180 = 32 482 800", "km", "0,05", "kg CO2e/pax-km", "1 621,4"],
                    ["", "Jami", "", "", "", "", "TOTAL (tCO2e)", "3 990,85"],
                ],
            },
        ],
        "sections_en": [
            {
                "title": "Scope 1 - Direct Emissions",
                "table_headers": ["No", "Emission Source", "Scope (1)", "Activity Data", "Unit", "Emission Factor", "EF Unit", "Total Emissions (tCO2e)"],
                "table_rows": [
                    ["1", "Natural gas consumption", "Scope 1", "601 000", "m3", "1.9", "kgCO2e/m3", "1 141.9"],
                    ["2", "Coal consumption", "Scope 1", "7 205", "kg", "2.4", "kgCO2e/kg", "17"],
                    ["", "Total", "", "", "", "", "TOTAL (tCO2e)", "1 159"],
                ],
            },
            {
                "title": "Scope 2 - Indirect Energy Emissions",
                "table_headers": ["No", "Emission Source", "Scope (2)", "Activity Data", "Unit", "Emission Factor", "EF Unit", "Total Emissions (tCO2e)"],
                "table_rows": [
                    ["1", "Electricity consumption", "Scope 2", "1 543 287", "kWh", "0.4", "kgCO2e/kWh", "617.31"],
                    ["2", "Operational (use-phase)", "Scope 2", "1 832 706", "kWh", "0", "kgt CO2/kWh", "0"],
                    ["", "Total", "", "", "", "", "TOTAL (tCO2e)", "617.31"],
                ],
            },
            {
                "title": "Scope 3 - Other Indirect Emissions",
                "table_headers": ["No", "Emission Source", "Scope (3)", "Activity Data", "Unit", "Emission Factor", "EF Unit", "Total Emissions (tCO2e)"],
                "table_rows": [
                    ["1", "Petrol (Gasoline)", "Scope 3", "8610", "liter", "2.31", "kgCO2e/litr", "19.89"],
                    ["2", "Diesel", "Scope 3", "1766", "liter", "2.68", "kgCO2e/litr", "4.73"],
                    ["3", "Hybrid transport", "Scope 3", "11200", "km", "0.09", "kgCO2e/km", "1"],
                    ["4", "Electric train", "Scope 3", "67000", "km", "0.035", "kgCO2e/km", "2.3"],
                    ["5", "Local bus", "Scope 3", "15 000", "km", "0.11", "kgCO2e/km", "1.65"],
                    ["6", "Aviation (short-distance <1500 km)", "Scope 3", "18 450", "km", "0.18", "kgCO2e/km", "3.3"],
                    ["7", "Aviation (medium-distance 1500-3700 km)", "Scope 3", "27 300", "km", "0.13", "kgCO2e/km", "3.55"],
                    ["8", "Aviation (long-distance >3700 km)", "Scope 3", "37 000", "km", "0.11", "kgCO2e/km", "4.07"],
                    ["9", "Motorcycle", "Scope 3", "5000", "km", "0.1", "kg CO2 per km", "0.5"],
                    ["10", "Waste (landfill)", "Scope 3", "120 800", "kg", "500", "kg CO2e per ton", "60.4"],
                    ["11", "Paper", "Scope 3", "5 900", "kg", "100", "kg CO2e per ton", "0.6"],
                    ["12", "Office equipment", "Scope 3", "188 153", "USD", "0.0005", "tCO2 per 1,000 currency units", "94.1"],
                    ["13", "Plastic waste", "Scope 3", "2 700", "kg", "400", "kg CO2e per ton", "1.1"],
                    ["14", "Food", "Scope 3", "3 200", "kg", "700", "kg CO2e per ton", "2.2"],
                    ["15", "(IT) equipment", "Scope 3", "359 800", "USD", "0.0008", "tCO2 per 1,000 currency units", "287.8"],
                    ["16", "Medical/laboratory equipment", "Scope 3", "61 500", "USD", "0.0012", "tCO2 per 1,000 currency units", "73.8"],
                    ["17", "Construction activities", "Scope 3", "933 641", "USD", "0.0009", "tCO2 per 1,000 currency units", "840.3"],
                    ["18", "Water supply", "Scope 3", "45 003", "m3", "0.34", "kg CO2 per m3", "15.3"],
                    ["19", "Wastewater treatment", "Scope 3", "3 540", "m3", "0.7", "kg CO2 per m3", "2.5"],
                    ["20", "Staff commuting", "Scope 3", "10x2x1200x220 = 5 280 000", "km", "0.18", "kg CO2e/pax-km", "950.4"],
                    ["21", "Student commuting", "Scope 3", "10x2x9023x180 = 32 482 800", "km", "0.05", "kg CO2e/pax-km", "1 621.4"],
                    ["", "Total", "", "", "", "", "TOTAL (tCO2e)", "3 990.85"],
                ],
            },
        ],
    },
    "financial-report": {
        "eyebrow_uz": "Hisobotlar",
        "eyebrow_en": "Reports",
        "title_uz": "Moliyaviy hisobot",
        "title_en": "Financial report",
        "intro_uz": "Qarshi davlat universitetining 2024-yil uchun yillik moliyaviy hisobotining asosiy ko'rsatkichlari.",
        "intro_en": "Key figures from Karshi State University's annual financial report for 2024.",
        "download_url": "/static/documents/annual-financial-report-2024.docx",
        "download_name": "Annual Financial Report-2024.docx",
        "show_download_cta": False,
        "sections_uz": [
            {
                "title": "Umumiy hisobot",
                "table_headers": ["РІвЂћвЂ“", "Umumiy hisobot", "So'm"],
                "table_rows": [
                    ["1", "Jami daromadlar qiymati", "267 923 179 787"],
                    ["2", "Jami xarajatlar qiymati", "228 895 792 507"],
                    ["3", "Ortiqcha mablag'", "39 027 387 280"],
                    ["4", "Qarz mablag'", "0"],
                ],
            },
            {
                "title": "Daromad hisoboti",
                "table_headers": ["РІвЂћвЂ“", "Daromad hisoboti", "So'm"],
                "table_rows": [
                    ["1", "Davlat tomonidan moliyalashtirish", "66 579 927 300"],
                    ["2", "O'qish to'lovlari-kontrakt", "182 496 604 487"],
                    ["3", "Grantlar va ilmiy tadqiqotlarni moliyalashtirish", "6 848 615 800"],
                    ["4", "Boshqa daromadlar", "11 998 032 200"],
                ],
            },
            {
                "title": "Xarajatlar",
                "table_headers": ["РІвЂћвЂ“", "Xarajatlar", "So'm"],
                "table_rows": [
                    ["1", "Maosh va ish haqi", "124 947 192 257"],
                    ["2", "Infratuzilma va texnik xizmat ko'rsatish", "44 739 359 771"],
                    ["3", "Kommunal xizmatlar", "1 972 623 932"],
                    ["4", "Ta'lim resurslari", "19 716 656 428"],
                    ["5", "Boshqa xarajatlar", "37 519 960 119"],
                ],
            },
        ],
        "sections_en": [
            {
                "title": "Summary Financial Report",
                "table_headers": ["РІвЂћвЂ“", "Summary Financial Report", "Amount (UZS)"],
                "table_rows": [
                    ["1", "Total Revenue", "267 923 179 787"],
                    ["2", "Total Expenditure", "228 895 792 507"],
                    ["3", "Surplus", "39 027 387 280"],
                    ["4", "Debt", "0"],
                ],
            },
            {
                "title": "Revenue breakdown",
                "table_headers": ["РІвЂћвЂ“", "Revenue Breakdown", "Amount (UZS)"],
                "table_rows": [
                    ["1", "Government Funding", "66 579 927 300"],
                    ["2", "Tuition Fees (Contract-based)", "182 496 604 487"],
                    ["3", "Grants and Research Funding", "6 848 615 800"],
                    ["4", "Other Income", "11 998 032 200"],
                ],
            },
            {
                "title": "Expenditure Breakdown",
                "table_headers": ["РІвЂћвЂ“", "Expenditure Breakdown", "Amount (UZS)"],
                "table_rows": [
                    ["1", "Salaries and Wages", "124 947 192 257"],
                    ["2", "Infrastructure and Maintenance", "44 739 359 771"],
                    ["3", "Utilities", "1 972 623 932"],
                    ["4", "Educational Resources", "19 716 656 428"],
                    ["5", "Other Expenses", "37 519 960 119"],
                ],
            },
        ],
    },
    "sustainability-report": {
        "eyebrow_uz": "Hisobotlar",
        "eyebrow_en": "Reports",
        "title_uz": "Qarshi davlat universiteti 2024-2025 yildagi Barqarorlik hisoboti",
        "title_en": "Karshi State University Sustainability Report 2024-2025",
        "intro_uz": "Qarshi davlat universitetining 2024-2025 yillardagi barqarorlik yo'nalishlari, boshqaruv tizimi va rivojlanish natijalarini yorituvchi hisobot sahifasi.",
        "intro_en": "A report page highlighting Karshi State University's 2024-2025 sustainability priorities, governance model, and progress.",
        "show_download_cta": False,
        "sections_uz": [
            {
                "title": "Hisobot mazmuni",
                "paragraphs": [
                    "Qarshi davlat universitetining 2024-2025 yillardagi Barqarorlik hisoboti universitetning atrof-muhitga mas'uliyatli yondashuvi, barqaror rivojlanish va global hamkorlik yo'lidagi strategik majburiyatlarini har tomonlama yoritib beradi. O'zbekistonning yetakchi oliy ta'lim muassasalaridan biri sifatida QDU barqarorlik tamoyillarini ta'lim dasturlari, kampus faoliyati va jamoatchilik bilan hamkorlik jarayonlariga faol integratsiya qilib, uzoq muddatli ekologik, ijtimoiy va iqtisodiy farovonlikka hissa qo'shmoqda.",
                    "Hisobot oltita asosiy yo'nalishni qamrab oladi: infratuzilma, energiya va iqlim o'zgarishi, chiqindilarni boshqarish, suv resurslarini tejash, transport va ta'lim hamda ilmiy tadqiqotlar. Ushbu tizimli yondashuv orqali universitet barqarorlik faoliyatida o'lchab bo'ladigan natijalar, ochiqlik va doimiy takomillashuvni ta'minlaydi.",
                    "QDU barqarorlik modelining muhim jihatlaridan biri kuchli institutsional boshqaruv tizimidir. Barqarorlik tashabbuslari ilmiy ishlar va innovatsiyalar bo'yicha prorektor rahbarligidagi maxsus bo'linma tomonidan muvofiqlashtiriladi hamda professor-o'qituvchilar, talabalar va ma'muriy xodimlardan iborat Barqarorlik kengashi tomonidan qo'llab-quvvatlanadi. Ushbu inklyuziv boshqaruv modeli barqarorlikni universitet faoliyatining barcha darajalariga chuqur singdirishni ta'minlaydi.",
                    "Universitet barqarorlikni moliyalashtirishga ham katta e'tibor qaratadi, umumiy byudjetining taxminan 30 foizi yashil tashabbuslar, infratuzilmani modernizatsiya qilish va ekologik dasturlarga yo'naltirilgan. Ushbu investitsiyalar energiya samaradorligini oshirish, qayta tiklanuvchi energiya manbalarini joriy etish, suvni tejash texnologiyalari, chiqindilarni kamaytirish va barqaror kampusni rivojlantirishga xizmat qiladi hamda past uglerodli va resurslardan samarali foydalanadigan universitet modelini shakllantirishga qaratilgan.",
                    "QDU yashil va inklyuziv kampus muhitini yaratishda sezilarli yutuqlarga erishgan. Kampus hududining yarmidan ortig'i yashil hududlar bilan qoplangan bo'lib, bu bioxilma-xillikni saqlash, ilmiy tadqiqotlar va jamoatchilik bilan ishlashni qo'llab-quvvatlaydi. Shu bilan birga, universitet nogironligi bo'lgan shaxslar uchun maxsus infratuzilmalarni yaratish orqali inklyuzivlikni ta'minlaydi hamda talabalar va xodimlar uchun keng qamrovli sog'liqni saqlash, xavfsizlik va farovonlik xizmatlarini taklif etadi.",
                    "Energiya va iqlim yo'nalishida universitet zamonaviy energiya tejovchi texnologiyalarni joriy qilgan, jumladan, barcha binolarda LED yoritish tizimlari, issiqlik izolyatsiyasi va quyosh panellari o'rnatilgan. Ushbu choralar energiya iste'molini va karbon chiqindilarini sezilarli darajada kamaytirish bilan birga, qayta tiklanuvchi energiya manbalariga o'tishni jadallashtirmoqda.",
                    "Bundan tashqari, Qarshi davlat universiteti barqarorlikni ta'lim va ilmiy tadqiqotlar jarayoniga faol integratsiya qiladi. Talabalar tashabbuslari, fanlararo ilmiy loyihalar va targ'ibot tadbirlari qo'llab-quvvatlanadi. Mahalliy va xalqaro hamkorliklar orqali universitet global barqaror rivojlanish jarayonlariga hissa qo'shadi hamda o'z faoliyatini BMTning Barqaror rivojlanish maqsadlari (SDGs) bilan uyg'unlashtiradi.",
                    "Umuman olganda, ushbu hisobot Qarshi davlat universitetining zamonaviy, yashil va ijtimoiy mas'uliyatli universitetga aylanish jarayonini yoritib beradi. Universitet innovatsiya, ekologik barqarorlik va barqaror rivojlanish tamoyillariga sodiq holda milliy va global miqyosda faoliyat olib bormoqda.",
                ],
            },
        ],
        "sections_en": [
            {
                "title": "Report overview",
                "paragraphs": [
                    "Karshi State University's Sustainability Report 2024-2025 presents a comprehensive overview of the university's strategic commitment to environmental responsibility, sustainable development, and global engagement. As one of Uzbekistan's leading higher education institutions, KSU actively integrates sustainability principles into its academic programs, campus operations, and community partnerships, contributing to long-term environmental, social, and economic well-being.",
                    "The report is covering six key areas: infrastructure, energy and climate change, waste management, water conservation, transportation, and education and research. Through this structured approach, the university ensures measurable progress, transparency, and continuous improvement in sustainability performance.",
                    "A distinctive feature of KSU's sustainability model is its strong institutional governance. Sustainability initiatives are coordinated by a dedicated unit under the Vice-Rector for Scientific Affairs and Innovations, supported by a cross-functional Sustainability Council that includes faculty members, students, and administrative staff. This inclusive governance structure ensures that sustainability is embedded across all levels of university operations.",
                    "The university demonstrates a significant financial commitment to sustainability, allocating approximately 30% of its total budget toward green initiatives, infrastructure modernization, and environmental programs. Investments focus on energy efficiency, renewable energy adoption, water-saving technologies, waste reduction, and sustainable campus development, reflecting a long-term vision for a low-carbon and resource-efficient university.",
                    "KSU has made notable progress in developing a green and inclusive campus environment. Over half of the campus area is covered by vegetation, supporting biodiversity, research, and community engagement. The university also ensures accessibility and inclusivity through facilities designed for individuals with disabilities, alongside comprehensive health, safety, and well-being services for students and staff.",
                    "In the area of energy and climate action, the university has implemented advanced energy-saving technologies, including full LED lighting coverage, thermal insulation, and the installation of solar panels. These measures have significantly reduced energy consumption and carbon emissions, while supporting the transition toward renewable energy sources.",
                    "Furthermore, Karshi State University actively integrates sustainability into education and research by supporting student-led initiatives, interdisciplinary research projects, and awareness programs. Through partnerships with local and international stakeholders, the university contributes to global sustainability efforts and aligns its activities with the United Nations Sustainable Development Goals (SDGs).",
                    "Overall, the Sustainability Report highlights KSU's transformation into a smart, green, and socially responsible university, committed to innovation, environmental stewardship, and sustainable development at both national and global levels.",
                ],
            },
        ],
    },
}


class ReportCardDetailView(BasePortalContextMixin, TemplateView):
    template_name = "portal/report_detail.html"
    page_key = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        suffix = "uz" if language_code == "uz" else "en"
        slug = kwargs["slug"]
        report = REPORT_INSIGHT_CARD_CONTENT.get(slug)
        if not report:
            raise Http404("Report detail page not found")

        report_context = {
            "slug": slug,
            "eyebrow": report[f"eyebrow_{suffix}"],
            "title": report[f"title_{suffix}"],
            "intro": report[f"intro_{suffix}"],
            "download_url": report.get("download_url", ""),
            "download_name": report.get("download_name", ""),
            "show_download_cta": report.get("show_download_cta", True),
            "sections": report[f"sections_{suffix}"],
        }

        if slug == "financial-report":
            page = self.request.GET.get("page", "1")
            context["is_paginated"] = True
            context["page_number"] = page

            if page == "2":
                report_context["intro"] = "Qarshi davlat universitetining 2023-yil uchun yillik moliyaviy hisobotining asosiy ko'rsatkichlari." if suffix == "uz" else "Key figures from Karshi State University's annual financial report for 2023."
                report_context["download_url"] = "/static/documents/annual-financial-report-2023.docx"
                report_context["download_name"] = "Annual Financial Report-2023.docx"
                
                if suffix == "uz":
                    report_context["sections"] = [
                        {
                            "title": "Umumiy hisobot",
                            "table_headers": ["РІвЂћвЂ“", "Umumiy hisobot", "So'm"],
                            "table_rows": [
                                ["1", "Jami daromadlar qiymati", "269 259 861 100"],
                                ["2", "Jami xarajatlar qiymati", "198 402 697 300"],
                                ["4", "Ortiqcha mablag'", "70 857 163 800"],
                                ["5", "Qarz mablag'", "0"],
                            ],
                        },
                        {
                            "title": "Daromad hisoboti",
                            "table_headers": ["РІвЂћвЂ“", "Daromad hisoboti", "So'm"],
                            "table_rows": [
                                ["1", "Davlat tomonidan moliyalashtirish", "56 707 206 700"],
                                ["2", "O'qish to'lovlari-kontrakt", "205 655 311 200"],
                                ["3", "Grantlar va ilmiy tadqiqotlarni moliyalashtirish", "2 240 310 100"],
                                ["4", "Boshqa daromadlar", "4 657 038 100"],
                            ],
                        },
                        {
                            "title": "Xarajatlar",
                            "table_headers": ["РІвЂћвЂ“", "Xarajatlar", "So'm"],
                            "table_rows": [
                                ["1", "Maosh va ish haqi", "110 575 449 800"],
                                ["2", "Infratuzilma va texnik xizmat ko'rsatish", "27 908 827 800"],
                                ["3", "Kommunal xizmatlar", "4 287 978 000"],
                                ["4", "Ta'lim resurslari", "32 677 676 600"],
                                ["5", "Boshqa xarajatlar", "26 811 945 300"],
                            ],
                        },
                    ]
                else:
                    report_context["sections"] = [
                        {
                            "title": "Summary Financial Report",
                            "table_headers": ["РІвЂћвЂ“", "Summary Financial Report", "Amount (UZS)"],
                            "table_rows": [
                                ["1", "Total Revenue", "269 259 861 100"],
                                ["2", "Total Expenditure", "198 402 697 300"],
                                ["4", "Surplus", "70 857 163 800"],
                                ["5", "Debt", "0"],
                            ],
                        },
                        {
                            "title": "Revenue Breakdown",
                            "table_headers": ["РІвЂћвЂ“", "Revenue Breakdown", "Amount (UZS)"],
                            "table_rows": [
                                ["1", "Government Funding", "56 707 206 700"],
                                ["2", "Tuition Fees (Contract-based)", "205 655 311 200"],
                                ["3", "Grants and Research Funding", "2 240 310 100"],
                                ["4", "Other Income", "4 657 038 100"],
                            ],
                        },
                        {
                            "title": "Expenditure Breakdown",
                            "table_headers": ["РІвЂћвЂ“", "Expenditure Breakdown", "Amount (UZS)"],
                            "table_rows": [
                                ["1", "Salaries and Wages", "110 575 449 800"],
                                ["2", "Infrastructure and Maintenance", "27 908 827 800"],
                                ["3", "Utilities", "4 287 978 000"],
                                ["4", "Educational Resources", "32 677 676 600"],
                                ["5", "Other Expenses", "26 811 945 300"],
                            ],
                        },
                    ]

        context["report_detail"] = report_context
        return context


class NewsEventsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/news_events.html"
    page_key = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        selected_sdg = self.request.GET.get("sdg")
        try:
            selected_sdg = int(selected_sdg) if selected_sdg else None
        except (TypeError, ValueError):
            selected_sdg = None
        news_queryset = NewsArticle.objects.all()
        if selected_sdg in range(1, 18):
            news_queryset = news_queryset.filter(sdg_goal=selected_sdg)
        featured_article = news_queryset.filter(featured=True).first() or news_queryset.first()
        paginator = Paginator(news_queryset, 9)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        news_items = page_obj.object_list
        context["featured_article"] = localize_object(featured_article, language_code)
        context["news_items"] = localize_collection(news_items, language_code)
        context["page_obj"] = page_obj
        context["events"] = localize_collection(Event.objects.all(), language_code)
        context["selected_sdg"] = selected_sdg
        context["selected_sdg_goal"] = get_sdg_goal(selected_sdg, language_code) if selected_sdg in range(1, 18) else None
        return context


class NewsDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/news_detail.html"
    model = NewsArticle
    context_object_name = "article"
    page_key = "news"

    def get_object(self, queryset=None):
        return localize_object(super().get_object(queryset), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["related_reports"] = localize_collection(Report.objects.filter(featured=True)[:2], language_code)
        context["recent_news"] = localize_collection(NewsArticle.objects.exclude(pk=self.object.pk)[:3], language_code)
        return context


class EventDetailView(BasePortalContextMixin, DetailView):
    template_name = "portal/event_detail.html"
    model = Event
    context_object_name = "event"
    page_key = "news"

    def get_object(self, queryset=None):
        return localize_object(super().get_object(queryset), self.get_language_code())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_events"] = localize_collection(Event.objects.exclude(pk=self.object.pk)[:3], self.get_language_code())
        return context


class ContactView(BasePortalContextMixin, TemplateView):
    template_name = "portal/contact.html"
    page_key = "contact"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", ContactSubmissionForm(language_code=self.get_language_code()))
        context["departments"] = localize_collection(DepartmentContact.objects.all(), self.get_language_code())
        return context

    def post(self, request, *args, **kwargs):
        form = ContactSubmissionForm(request.POST, language_code=self.get_language_code())
        if form.is_valid():
            form.save()
            messages.success(
                request,
                translate_text("Your message has been submitted to the institutional coordination office.", self.get_language_code()),
            )
            return redirect("contact")
        return self.render_to_response(self.get_context_data(form=form))


def robots_txt(_request):
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Sitemap: /sitemap.xml",
        ]
    )
    return HttpResponse(content, content_type="text/plain")


def health_check(_request):
    return JsonResponse({"status": "ok"})

