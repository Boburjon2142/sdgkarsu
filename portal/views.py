from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
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
from .translation_utils import localize_collection, localize_object, translate_text


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
    "hero_title": "O‘ta qashshoqlikka barham berish",
    "idea_title": "Asosiy g‘oya",
    "idea_text": "Butun dunyoda barcha turdagi qashshoqlikni butkul yo‘q qilish",
    "sections": [
        {
            "title": "Umumiy ma’lumot",
            "paragraphs": [
                "2015-yilda Birlashgan Millatlar Tashkiloti tomonidan belgilangan Barqaror rivojlanish maqsadlarining birinchi yo‘nalishi — qashshoqlikning barcha shakllariga barham berishdir (SDG 1).",
                "Davlatlar quyidagi prinsipni qabul qilgan: “Hech kimni ortda qoldirmaslik”.",
                "Bu maqsad oziq-ovqat yetishmovchiligi, toza ichimlik suvi muammosi va sanitariya yetishmasligi kabi muammolarni ham qamrab oladi.",
                "Shuningdek, iqlim o‘zgarishi va mojarolar keltirib chiqaradigan xavflarni ham hal qilishni talab qiladi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 1 doirasida 7 ta maqsad va 13 ta ko‘rsatkich mavjud.",
                "Natijada quyidagilar amalga oshiriladi:",
            ],
            "bullets": [
                "O‘ta qashshoqlikni yo‘q qilish",
                "Qashshoqlikni kamida 50% ga qisqartirish",
                "Ijtimoiy himoya tizimini yaratish",
                "Resurs va xizmatlarga teng kirishni ta’minlash",
                "Ofatlarga chidamlilikni oshirish",
            ],
        },
        {
            "title": "Global holat",
            "paragraphs": ["Hozirgi kunda quyidagi ko‘rsatkichlar dolzarb hisoblanadi:"],
            "bullets": [
                "Dunyo aholisining taxminan 10% qashshoqlikda yashaydi",
                "2015-yilda 736 million odam o‘ta qashshoqlikda yashagan",
                "Eng katta ulush Afrika hududiga to‘g‘ri keladi",
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
                "iqlim o‘zgarishi",
                "urush va mojarolar",
            ],
        },
        {
            "title": "Bolalar va qashshoqlik",
            "bullets": [
                "385 millionga yaqin bola kuniga $1.90 dan kam daromad bilan yashaydi",
                "Ko‘plab mamlakatlarda bolalar qashshoqligi bo‘yicha aniq statistika yo‘q",
                "97% mamlakatda yetarli data mavjud emas",
            ],
        },
        {
            "title": "Ijobiy o‘zgarishlar",
            "paragraphs": [
                "1990–2015 oralig‘ida qashshoqlikda yashovchilar soni 1.8 milliarddan 776 milliongacha kamaydi.",
                "Ammo muammo hali to‘liq hal bo‘lmagan va erishilgan natijalarni saqlab qolish uchun izchil siyosat zarur.",
            ],
        },
        {
            "title": "Hukumatlar roli",
            "paragraphs": ["Mahalliy va global hukumatlar quyidagi yo‘nalishlarda faol ishlaydi:"],
            "bullets": [
                "kam ta’minlanganlarni qo‘llab-quvvatlash",
                "shaffof boshqaruvni ta’minlash",
                "bandlikni oshirish",
                "ta’lim va iqtisodiy imkoniyatlarni kengaytirish",
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
    "idea_title": "Asosiy g‘oya",
    "idea_text": "Ochlikni tugatish, oziq-ovqat xavfsizligini ta’minlash va oziqlanishni yaxshilash hamda qishloq xo‘jaligining barqaror rivojlanishiga ko‘maklashish.",
    "sections": [
        {
            "title": "Umumiy ma’lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 2-maqsadi ochlikni tugatish, oziq-ovqat xavfsizligini ta’minlash, oziqlanishni yaxshilash hamda qishloq xo‘jaligining barqaror rivojlanishiga ko‘maklashishni nazarda tutadi.",
                "SDG 2 oziq-ovqat xavfsizligi, ovqatlanish sifatini yaxshilash va qishloq xo‘jaligi bilan barqaror iqtisodiy rivojlanish o‘rtasidagi uzviy bog‘liqlikni ko‘rsatadi.",
                "Birlashgan Millatlar Tashkiloti ma’lumotlariga ko‘ra, dunyoda yuz millionlab odamlar ochlik va to‘yib ovqatlanmaslik xavfi ostida yashamoqda.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va natijalar",
            "paragraphs": [
                "SDG 2 doirasida 8 ta maqsad va 14 ta ko‘rsatkich mavjud.",
                "Mazkur vazifalarni amalga oshirish natijasida quyidagilarga erishish ko‘zda tutiladi:",
            ],
            "bullets": [
                "ochlikni yo‘q qilish va oziq-ovqat bilan ta’minlashni yaxshilash",
                "to‘yib ovqatlanmaslikning barcha shakllarini yo‘q qilish",
                "qishloq xo‘jaligi hosildorligini oshirish",
                "barqaror oziq-ovqat ishlab chiqarish tizimlari va qishloq xo‘jaligi amaliyotini kengaytirish",
                "urug‘lar, ekinlar va uy hayvonlarining genetik xilma-xilligini ko‘paytirish",
                "investitsiyalar, tadqiqot va texnologiyalarni keng joriy etish",
            ],
        },
        {
            "title": "Bugungi global holat",
            "paragraphs": [
                "To‘yib ovqatlanmaslik darajasi ayrim davrlarda kamaygan bo‘lsa-da, 2015-yildan keyin och qolish ko‘rsatkichlari yana o‘sishni boshladi.",
                "Bunga oziq-ovqat tizimlaridagi uzilishlar, iqlim o‘zgarishi, mojarolar va iqtisodiy beqarorlik sabab bo‘lmoqda.",
                "COVID-19 pandemiyasi esa xarid qobiliyati va mahsulot tarqatish zanjirlariga salbiy ta’sir ko‘rsatib, vaziyatni keskinlashtirdi.",
            ],
        },
        {
            "title": "Xavflar va muammolar",
            "paragraphs": [
                "Dunyo 2030-yilgacha ocharchilikni to‘liq yo‘qotish yo‘lida jiddiy sinovlarga duch kelmoqda.",
            ],
            "bullets": [
                "iqlim o‘zgarishi va qurg‘oqchilik",
                "urush va mojarolar",
                "oziq-ovqat narxlarining oshishi",
                "qishloq xo‘jaligida texnologik orqada qolish",
                "taqsimot tizimidagi zaifliklar",
            ],
        },
        {
            "title": "Bolalar va ovqatlanish",
            "paragraphs": [
                "Bolalar orasidagi to‘yib ovqatlanmaslik jismoniy va aqliy rivojlanishga bevosita salbiy ta’sir ko‘rsatadi.",
                "Dunyoda millionlab bolalar yetarli ovqatlanmaslik tufayli sog‘liq, ta’lim va kelajakdagi iqtisodiy imkoniyatlardan mahrum bo‘lish xavfi ostida qolmoqda.",
            ],
        },
        {
            "title": "Qishloq xo‘jaligi va rivojlanish",
            "paragraphs": [
                "Rivojlanayotgan mamlakatlarda qishloq xo‘jaligi millionlab oilalar uchun asosiy daromad manbai hisoblanadi.",
                "Zamonaviy texnologiyalar, adolatli taqsimlash tizimlari va samarali investitsiyalar orqali oziq-ovqat ishlab chiqarishni ko‘paytirish va chiqindilarni kamaytirish mumkin.",
                "Ayollar va kichik ishlab chiqaruvchilarni qo‘llab-quvvatlash bu yo‘nalishda alohida ahamiyatga ega.",
            ],
        },
        {
            "title": "Hukumatlar va institutlar roli",
            "paragraphs": [
                "Davlatlar va xalqaro institutlar SDG 2 ga erishish uchun quyidagi yo‘nalishlarda ishlaydi:",
            ],
            "bullets": [
                "oziq-ovqat xavfsizligi siyosatini kuchaytirish",
                "mahalliy ishlab chiqaruvchilarni qo‘llab-quvvatlash",
                "innovatsion agrotexnologiyalarni joriy etish",
                "barqaror suv va yer resurslarini boshqarish",
                "zaif qatlamlar uchun oziq-ovqat va ijtimoiy yordam dasturlarini kengaytirish",
            ],
        },
    ],
}


SDG_3_DETAIL_UZ = {
    "hero_title": "Sog‘lik va farovonlik",
    "idea_title": "Asosiy g‘oya",
    "idea_text": "Sog‘lom turmush tarzini ta’minlash va barcha yoshdagi kishilarning farovonligiga ko‘maklashish.",
    "sections": [
        {
            "title": "Umumiy ma’lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 3-maqsadi sog‘lom turmush tarzini ta’minlash va barcha yoshdagi kishilarning farovonligiga ko‘maklashishni nazarda tutadi.",
                "SDG 3 sog‘lom turmush tarzining turli jihatlarini qamrab oladi va unga doimiy e’tibor qaratadi.",
            ],
        },
        {
            "title": "Asosiy maqsadlar va ko‘rsatkichlar",
            "paragraphs": [
                "SDG 3ni amalga oshirish uchun 13 maqsad va taraqqiyot yo‘lini belgilash uchun 28 ko‘rsatkich mavjud.",
                "Birinchi 9 maqsad “maqsadli natijalar” bo‘lib, ularga quyidagilar kiradi:",
            ],
            "bullets": [
                "onalar o‘limini kamaytirish",
                "yangi tug‘ilgan chaqaloqlar va besh yoshgacha bo‘lgan bolalar o‘limini kamaytirish",
                "yuqumli kasalliklarga qarshi kurashish",
                "yuqumli bo‘lmagan kasalliklardan o‘limni kamaytirish va ruhiy salomatlikni yaxshilash",
                "giyohvandlikning oldini olish va davolash",
                "yo‘l-transport hodisalarida jarohatlar va o‘limlarni kamaytirish",
                "jinsiy va reproduktiv salomatlik xizmatlaridan foydalanishni kengaytirish",
                "umumiy sog‘liqni saqlash qamroviga erishish",
                "xavfli kimyoviy moddalardan kasallanish va o‘limni kamaytirish",
            ],
        },
        {
            "title": "Erishish vositalari",
            "paragraphs": [
                "SDG 3 maqsadlarining qolgan to‘rttasi erishish vositalari bo‘lib, ular quyidagi yo‘nalishlarni qamrab oladi:",
            ],
            "bullets": [
                "tamaki nazorati bo‘yicha xalqaro konvensiyalarni amalga oshirish",
                "tadqiqot, dori vositalari va vaksinalardan universal foydalanishni qo‘llab-quvvatlash",
                "rivojlanayotgan mamlakatlarda sog‘liqni saqlashni moliyalashtirish va tizimni mustahkamlash",
                "global sog‘liq xavflari bo‘yicha erta ogohlantirish tizimlarini takomillashtirish",
            ],
        },
        {
            "title": "Global sog‘liq kun tartibi",
            "paragraphs": [
                "SDG 3 barcha erkaklar va ayollar uchun tibbiy xizmatlardan teng foydalanishni ta’minlaydigan universal tibbiy qamrovga erishishga qaratilgan.",
                "U yangi tug‘ilgan chaqaloqlar, besh yoshgacha bo‘lgan bolalar o‘limining oldini olish va epidemiyalarni tugatish bilan birga iqtisodiy hamda ijtimoiy tengsizlik, urbanizatsiya, iqlim inqirozi va boshqa yuqumli kasalliklar xavfiga ham e’tibor qaratadi.",
                "2030-yil kun tartibidagi asosiy masala salomatlikka e’tiborni oshirish bo‘lib, COVID-19 pandemiyasi hisobga olinganda global miqyosda salomatlik va farovonlikni ta’minlashga jiddiy e’tibor qaratish zarur.",
            ],
        },
        {
            "title": "Bolalar salomatligi",
            "paragraphs": [
                "Har bir bolaning omon qolishi va rivojlanishini ta’minlash yuqori ta’sirli chora-tadbirlarni ko‘rishni talab qiladi.",
                "Bunga yangi tug‘ilgan chaqaloqlarni sifatli prenatal, tug‘ruq va tug‘ruqdan keyingi parvarish bilan qamrab olish, yuqumli kasalliklardan himoya qilish hamda yetarli va to‘yimli oziq-ovqatdan foydalanish imkoniyatini kengaytirish kiradi.",
            ],
        },
        {
            "title": "Asosiy statistika va xavflar",
            "paragraphs": [
                "UNDP ma’lumotlariga ko‘ra, har 2 soniyada 30 yoshdan 70 yoshgacha bo‘lgan bir kishi yurak-qon tomir kasalliklari, surunkali nafas yo‘llari kasalliklari, diabet yoki saraton kabi yuqumli bo‘lmagan kasalliklardan bevaqt vafot etadi.",
                "Dunyo bo‘ylab 2019-yilda 2.4 million chaqaloq bevaqt vafot etgan, kuniga taxminan 6,700 neonatal o‘lim qayd etilgan.",
                "O‘rtacha umr ko‘rish davomiyligini oshirish va ona-bola salomatligini yaxshilash borasida sezilarli yutuqlar bo‘lsa-da, ko‘plab mamlakatlarda bu maqsadlarga erishish uchun hali jiddiy ishlar talab etiladi.",
            ],
        },
        {
            "title": "Kelajak uchun ustuvor yo‘nalishlar",
            "paragraphs": [
                "Onalar o‘limini kamaytirish, toza suv va sanitariya xizmatlaridan foydalanishni kengaytirish, bezgak, sil, poliomiyelit va OIV/OITS tarqalishini qisqartirish SDG 3ning muhim yo‘nalishlari bo‘lib qolmoqda.",
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
                "«Hech kimni ortda qoldirmaslik» tamoyili asosida davlatlar eng uzoqda qolayotgan hududlar va ijtimoiy qatlamlar uchun taraqqiyotni tezlashtirish majburiyatini oldilar. Bu gender tengligiga erishish va barcha ayol-qizlarning imkoniyatlarini kengaytirish uchun alohida ahamiyatga ega.",
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
    "hero_title": "Munosib ish o‘rinlari va iqtisodiy o‘sish",
    "idea_title": "Asosiy g‘oya",
    "idea_text": "Keng qamrovli va barqaror iqtisodiy o‘sish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini ta’minlashga ko‘maklashish.",
    "sections": [
        {
            "title": "Umumiy ma’lumot",
            "paragraphs": [
                "Barqaror rivojlanishning 8-maqsadi keng qamrovli va barqaror iqtisodiy o‘sish hamda barcha uchun bandlik va munosib mehnat qilish imkoniyatlarini ta’minlashga ko‘maklashishga qaratilgan. Keyingi o‘rinlarda bu maqsad SDG 8 deb yuritiladi.",
                "SDG 8 ni amalga oshirish uchun 12 maqsad va taraqqiyot yo‘lini belgilash uchun 17 ta ko‘rsatkich mavjud.",
            ],
        },
        {
            "title": "Asosiy maqsadlar",
            "paragraphs": [
                "Birinchi o‘ntalik maqsadlar maqsadli natijalar deb yuritiladi va ular quyidagilarni qamrab oladi:",
            ],
            "bullets": [
                "barqaror iqtisodiy o‘sish",
                "iqtisodiy samaradorlikni oshirish uchun diversifikatsiya, innovatsiyalar va modernizatsiya",
                "ish o‘rinlari yaratish va korxonalar o‘sishini qo‘llab-quvvatlash siyosatini rag‘batlantirish",
                "iste’mol va ishlab chiqarishda resurslardan foydalanish samaradorligini oshirish",
                "to‘liq bandlik va teng haq to‘lanadigan munosib mehnat",
                "bandlikka ko‘maklashish",
                "yoshlarni ta’lim va tarbiyalash",
                "zamonaviy qullik, odam savdosi va bolalar mehnatiga barham berish",
                "mehnat huquqlarini himoya qilish va xavfsiz mehnat muhitini yaratish",
                "sog‘lom va barqaror turizmni rivojlantirish, bank, sug‘urta va moliyaviy xizmatlardan hamma teng foydalanishi",
            ],
        },
        {
            "title": "Yutuq vositalari",
            "paragraphs": [
                "Bundan tashqari, qolgan ikki maqsad yutuq vositalari hisoblanadi va ular quyidagilarni o‘z ichiga oladi:",
            ],
            "bullets": [
                "savdoni rivojlantirish uchun yordam berish hajmini oshirish",
                "yoshlar bandligining global strategiyasini ishlab chiqish",
            ],
        },
        {
            "title": "Global holat va iqtisodiy xatarlar",
            "paragraphs": [
                "Mazkur maqsad har bir mamlakatning iqtisodiy sektoridan, irqi va madaniyatidan qat’i nazar, fuqarolarning yaxshi hayot uchun zarur ehtiyojlarini ta’minlashga qaratilgan. Dunyo aholisining qariyb yarmi hali ham kuniga taxminan 2 AQSh dollari ekvivalenti bilan yashaydi.",
                "Ko‘p joylarda ish bilan band bo‘lish qashshoqlikdan xalos bo‘lishni kafolatlamaydi. Noto‘g‘ri taraqqiyot va nomutanosib iqtisodiy siyosat qashshoqlikni bartaraf etishga to‘sqinlik qilishi mumkin.",
                "COVID-19 pandemiyasi esa dunyoni Buyuk Depressiyadan keyingi eng yomon global iqtisodiy inqirozlardan biriga olib keldi va o‘sish sur’atlariga salbiy ta’sir ko‘rsatdi.",
            ],
        },
        {
            "title": "Bandlik va mehnat bozori",
            "paragraphs": [
                "2008-yilgi iqtisodiy inqiroz va global retsessiyaning uzoq davom etgan ta’siriga qaramay, o‘tgan o‘n yilliklarda ayrim hududlarda ishchilarning o‘ta qashshoqlikda yashashi kamaydi. Shunga qaramay, bandlikning o‘sish darajasi ko‘plab mamlakatlarda sekinlashib bormoqda.",
                "Barcha xodimlarning katta qismi hali ham rasmiy mehnat shartnomasiga ega emas. Bu esa ijtimoiy himoya, munosib daromad va mehnat xavfsizligi bilan bog‘liq muammolarni kuchaytiradi.",
            ],
        },
        {
            "title": "Kelajak ustuvor yo‘nalishlari",
            "paragraphs": [
                "SDG 8 kelib chiqishi, irqi va jinsidan qat’i nazar, barcha ishchilar uchun barqaror va adolatli iqtisodiy o‘sishni rag‘batlantirishga qaratilgan. Bu diversifikatsiya, texnologik yangilanish va innovatsiyalar orqali iqtisodiy samaradorlikni oshirishni anglatadi.",
                "Kelgusida yuqori qo‘shilgan qiymatga ega, mehnatni ko‘p talab qiluvchi tarmoqlarga e’tibor qaratish, yoshlar bandligini kuchaytirish va munosib mehnat standartlarini mustahkamlash asosiy vazifa bo‘lib qoladi.",
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


class BasePortalContextMixin:
    page_key = "home"

    def get_language_code(self):
        return getattr(self.request, "LANGUAGE_CODE", "en")

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
        return context


class HomeView(BasePortalContextMixin, TemplateView):
    template_name = "portal/home.html"
    page_key = "home"

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
        context["hero_stats"] = localize_collection(HeroStat.objects.all()[:4], language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all()[:4], language_code)
        context["featured_programs"] = localize_collection(Program.objects.filter(featured=True)[:3], language_code)
        context["featured_research"] = localize_collection(ResearchProject.objects.filter(featured=True)[:2], language_code)
        context["impact_metrics"] = localize_collection(ImpactMetric.objects.filter(scope__in=["home", "both"])[:4], language_code)
        context["latest_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], language_code)
        context["latest_news"] = localize_collection(NewsArticle.objects.all()[:3], language_code)
        context["sustainability_news"] = localize_collection(sustainability_news, language_code)
        context["partners"] = localize_collection(Partner.objects.all()[:6], language_code)
        context["sdg_goals"] = [build_sdg_goal(item, language_code) for item in SDG_CONTENT]
        context["selected_sdg"] = selected_sdg
        context["selected_sdg_goal"] = get_sdg_goal(selected_sdg, language_code)
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
                "idea_title": "Asosiy g‘oya" if language_code == "uz" else "Core idea",
                "idea_text": goal["description"],
                "sections": [
                    {
                        "title": "Umumiy ma’lumot" if language_code == "uz" else "Overview",
                        "paragraphs": [
                            goal["description"],
                            "Mazkur maqsad universitetning ilmiy izlanishlari, ta’lim dasturlari va jamoatchilik bilan ishlash tashabbuslari orqali qo‘llab-quvvatlanadi."
                            if language_code == "uz"
                            else "This goal is supported through the university's research agenda, educational programs, and community engagement initiatives.",
                        ],
                    },
                    {
                        "title": "Asosiy yo‘nalishlar" if language_code == "uz" else "Priority directions",
                        "bullets": [
                            "ta’lim, tadqiqot va kampus boshqaruvida integratsiya"
                            if language_code == "uz"
                            else "integration across teaching, research, and campus management",
                            "ma’lumotlarga asoslangan institutsional qarorlar"
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
        context["goal_work_items"] = SDGWorkItem.objects.filter(goal_number=number)
        return context


class ResearchView(BasePortalContextMixin, TemplateView):
    template_name = "portal/research.html"
    page_key = "research"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["featured_projects"] = localize_collection(ResearchProject.objects.filter(featured=True), language_code)
        context["projects"] = localize_collection(ResearchProject.objects.all(), language_code)
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
        context["policies"] = localize_collection(PolicyDocument.objects.all(), language_code)
        context["featured_policies"] = localize_collection(PolicyDocument.objects.filter(featured=True)[:3], language_code)
        context["strategic_priorities"] = localize_collection(StrategicPriority.objects.all(), language_code)
        return context


class ReportsView(BasePortalContextMixin, TemplateView):
    template_name = "portal/reports.html"
    page_key = "reports"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.get_language_code()
        context["metrics"] = localize_collection(ImpactMetric.objects.filter(scope__in=["reports", "both"]), language_code)
        context["reports"] = localize_collection(Report.objects.all(), language_code)
        context["featured_reports"] = localize_collection(Report.objects.filter(featured=True)[:3], language_code)
        context["achievements"] = localize_collection(Achievement.objects.all(), language_code)
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
