def _build_table(title, heading_course, heading_field, rows):
    body = "".join(
        f"<tr><td>{course}</td><td>{field}</td></tr>"
        for course, field in rows
    )
    return (
        f'<h2>{title}</h2>'
        '<div class="governance-table-wrap">'
        '<table class="governance-table">'
        f'<thead><tr><th>{heading_course}</th><th>{heading_field}</th></tr></thead>'
        f'<tbody>{body}</tbody>'
        '</table>'
        '</div>'
    )


SUSTAINABILITY_SUBJECTS_TABLES_EN = []
SUSTAINABILITY_SUBJECTS_TABLES_UZ = []

MATH_EN = [
    ("Actuarial mathematics", "Mathematics"),
    ("Analysis and management of skills", "Mathematics"),
    ("Analysis of financial and economic data", "Mathematics"),
    ("Applied mathematics", "Mathematics"),
    ("Modeling transportation processes in automobiles", "Mathematics"),
    ("Fundamentals of artistic analysis", "Mathematics"),
    ("Corporate Governance (Economic Analysis and Audit)", "Mathematics"),
    ("Data base", "Mathematics"),
    ("Data structure and algorithms", "Mathematics"),
    ("Designing and modeling clothes", "Mathematics"),
    ("Economic analysis", "Mathematics"),
    ("Foundations of higher mathematics", "Mathematics"),
    ("Functional analysis and integral equations", "Mathematics"),
    ("Documentation, information analysis", "Mathematics"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Mathematics", "Course Name", "Field", MATH_EN)
)

MATH_UZ = [
    ("Aktuar matematika", "Matematika"),
    ("Ko'nikmalarni tahlil qilish va boshqarish", "Matematika"),
    ("Moliyaviy va iqtisodiy ma'lumotlarni tahlil qilish", "Matematika"),
    ("Amaliy matematika", "Matematika"),
    ("Avtomobillarda transport jarayonlarini modellashtirish", "Matematika"),
    ("Badiiy tahlil asoslari", "Matematika"),
    ("Korporativ boshqaruv (iqtisodiy tahlil va audit)", "Matematika"),
    ("Ma'lumotlar bazasi", "Matematika"),
    ("Ma'lumotlar tuzilmalari va algoritmlar", "Matematika"),
    ("Kiyimlarni loyihalash va modellashtirish", "Matematika"),
    ("Iqtisodiy tahlil", "Matematika"),
    ("Oliy matematika asoslari", "Matematika"),
    ("Funksional tahlil va integral tenglamalar", "Matematika"),
    ("Hujjatlar va axborotni tahlil qilish", "Matematika"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Matematika", "Fan nomi", "Yo'nalish", MATH_UZ)
)

ENGINEERING_EN = [
    ("Agrobiotechnology", "Engineering & Technology"),
    ("Alternative energy and nature protection", "Engineering & Technology"),
    ("Architectural construction", "Engineering & Technology"),
    ("Architectural materials science", "Engineering & Technology"),
    ("Automation of technological processes", "Engineering & Technology"),
    ("Information technology", "Engineering & Technology"),
    ("Basics of electrical safety", "Engineering & Technology"),
    ("BIM technologies in construction", "Engineering & Technology"),
    ("Bioengineering", "Engineering & Technology"),
    ("Biomass energy and energy devices based on them", "Engineering & Technology"),
    ("Biomass, geothermal energy and energy devices based on them", "Engineering & Technology"),
    ("Biotechnology of medicinal plants", "Engineering & Technology"),
    ("Biotechnology", "Engineering & Technology"),
    ("Fundamentals of Biotechnology", "Engineering & Technology"),
    ("Carpentry furniture finishing technology", "Engineering & Technology"),
    ("Cereal crop biotechnology", "Engineering & Technology"),
    ("Descriptive geometry and graphics engineering", "Engineering & Technology"),
    ("Computer Science and Information Technology", "Engineering & Technology"),
    ("Construction and operation of vehicles", "Engineering & Technology"),
    ("Constructions of buildings and facilities", "Engineering & Technology"),
    ("Digital information technology", "Engineering & Technology"),
    ("Finishing technology of carpentry furniture", "Engineering & Technology"),
    ("Ecobiotechnology", "Engineering & Technology"),
    ("Electrical engineering, electronics and electrical wiring", "Engineering & Technology"),
    ("Electrical safety", "Engineering & Technology"),
    ("Electrical engineering", "Engineering & Technology"),
    ("Energy efficient technologies", "Engineering & Technology"),
    ("Energy management", "Engineering & Technology"),
    ("Engineering geodesy", "Engineering & Technology"),
    ("Engineering graphics", "Engineering & Technology"),
    ("Engineering physics", "Engineering & Technology"),
    ("Engineering psychology", "Engineering & Technology"),
    ("Enzymological engineering", "Engineering & Technology"),
    ("History of Science and Technology", "Engineering & Technology"),
    ("Fine art technology and copying", "Engineering & Technology"),
    ("Food microbiology and biotechnology", "Engineering & Technology"),
    ("Fundamentals of bioenergy", "Engineering & Technology"),
    ("Fundamentals of electrical engineering and electrical engineering", "Engineering & Technology"),
    ("Fundamentals of mechanization, automation and robotics", "Engineering & Technology"),
    ("Game technology in preschool education", "Engineering & Technology"),
    ("Genetic engineering", "Engineering & Technology"),
    ("Genetic and cellular engineering", "Engineering & Technology"),
    ("Grape growing technology", "Engineering & Technology"),
    ("Heat engineering and hydropower", "Engineering & Technology"),
    ("Cell Biotechnology", "Engineering & Technology"),
    ("Industrial and radiation safety", "Engineering & Technology"),
    ("Industrial biotechnology", "Engineering & Technology"),
    ("Industrial ecology and safety of life activities", "Engineering & Technology"),
    ("Industrial Internet of Things", "Engineering & Technology"),
    ("Industrial programming", "Engineering & Technology"),
    ("Industrial sanitation and hygiene", "Engineering & Technology"),
    ("Informatics and Information technology", "Engineering & Technology"),
    ("Information technologies in construction", "Engineering & Technology"),
    ("Information technology and computer graphics", "Engineering & Technology"),
    ("Information technology and education", "Engineering & Technology"),
    ("Information technology in chemistry", "Engineering & Technology"),
    ("Information technology in the field of design", "Engineering & Technology"),
    ("Information technology in tourism", "Engineering & Technology"),
    ("Introduction to Biotechnology", "Engineering & Technology"),
    ("Introduction to sewing technology", "Engineering & Technology"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Engineering & Technology", "Course Name", "Field", ENGINEERING_EN)
)

ENGINEERING_UZ = [
    ("Agrobiotexnologiya", "Muhandislik va texnologiya"),
    ("Muqobil energiya va tabiatni muhofaza qilish", "Muhandislik va texnologiya"),
    ("Arxitektura qurilishi", "Muhandislik va texnologiya"),
    ("Qurilish materiallari fanlari", "Muhandislik va texnologiya"),
    ("Texnologik jarayonlarni avtomatlashtirish", "Muhandislik va texnologiya"),
    ("Axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Elektr xavfsizligi asoslari", "Muhandislik va texnologiya"),
    ("Qurilishda BIM texnologiyalari", "Muhandislik va texnologiya"),
    ("Bioinjeneriya", "Muhandislik va texnologiya"),
    ("Biomassa energiyasi va unga asoslangan energiya qurilmalari", "Muhandislik va texnologiya"),
    ("Biomassa, geotermal energiya va ularga asoslangan energiya qurilmalari", "Muhandislik va texnologiya"),
    ("Dorivor o'simliklar biotexnologiyasi", "Muhandislik va texnologiya"),
    ("Biotexnologiya", "Muhandislik va texnologiya"),
    ("Biotexnologiya asoslari", "Muhandislik va texnologiya"),
    ("Duradgorlik mebellarini pardozlash texnologiyasi", "Muhandislik va texnologiya"),
    ("Donli ekinlar biotexnologiyasi", "Muhandislik va texnologiya"),
    ("Tasviriy geometriya va muhandislik grafikasi", "Muhandislik va texnologiya"),
    ("Kompyuter fanlari va axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Transport vositalarini qurish va ulardan foydalanish", "Muhandislik va texnologiya"),
    ("Bino va inshootlar konstruksiyalari", "Muhandislik va texnologiya"),
    ("Raqamli axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Duradgorlik mebellarini yakuniy ishlov berish texnologiyasi", "Muhandislik va texnologiya"),
    ("Ekobiotexnologiya", "Muhandislik va texnologiya"),
    ("Elektrotexnika, elektronika va elektr simlari", "Muhandislik va texnologiya"),
    ("Elektr xavfsizligi", "Muhandislik va texnologiya"),
    ("Elektrotexnika", "Muhandislik va texnologiya"),
    ("Energiya tejamkor texnologiyalar", "Muhandislik va texnologiya"),
    ("Energiya menejmenti", "Muhandislik va texnologiya"),
    ("Muhandislik geodeziyasi", "Muhandislik va texnologiya"),
    ("Muhandislik grafikasi", "Muhandislik va texnologiya"),
    ("Muhandislik fizikasi", "Muhandislik va texnologiya"),
    ("Muhandislik psixologiyasi", "Muhandislik va texnologiya"),
    ("Enzimologik muhandislik", "Muhandislik va texnologiya"),
    ("Fan va texnika tarixi", "Muhandislik va texnologiya"),
    ("Tasviriy san'at texnologiyasi va nusxa ko'chirish", "Muhandislik va texnologiya"),
    ("Oziq-ovqat mikrobiologiyasi va biotexnologiyasi", "Muhandislik va texnologiya"),
    ("Bioenergetika asoslari", "Muhandislik va texnologiya"),
    ("Elektrotexnika asoslari", "Muhandislik va texnologiya"),
    ("Mexanizatsiya, avtomatlashtirish va robototexnika asoslari", "Muhandislik va texnologiya"),
    ("Maktabgacha ta'limda o'yin texnologiyalari", "Muhandislik va texnologiya"),
    ("Gen muhandisligi", "Muhandislik va texnologiya"),
    ("Genetik va hujayra muhandisligi", "Muhandislik va texnologiya"),
    ("Uzumchilik texnologiyasi", "Muhandislik va texnologiya"),
    ("Issiqlik texnikasi va gidroenergetika", "Muhandislik va texnologiya"),
    ("Hujayra biotexnologiyasi", "Muhandislik va texnologiya"),
    ("Sanoat va radiatsion xavfsizlik", "Muhandislik va texnologiya"),
    ("Sanoat biotexnologiyasi", "Muhandislik va texnologiya"),
    ("Sanoat ekologiyasi va hayot faoliyati xavfsizligi", "Muhandislik va texnologiya"),
    ("Sanoat Interneti (IIoT)", "Muhandislik va texnologiya"),
    ("Sanoat dasturlash", "Muhandislik va texnologiya"),
    ("Sanoat sanitariyasi va gigiyenasi", "Muhandislik va texnologiya"),
    ("Informatika va axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Qurilishda axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Axborot texnologiyalari va kompyuter grafikasi", "Muhandislik va texnologiya"),
    ("Axborot texnologiyalari va ta'lim", "Muhandislik va texnologiya"),
    ("Kimyo sohasida axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Dizayn sohasida axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Turizmda axborot texnologiyalari", "Muhandislik va texnologiya"),
    ("Biotexnologiyaga kirish", "Muhandislik va texnologiya"),
    ("Tikuvchilik texnologiyasiga kirish", "Muhandislik va texnologiya"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Muhandislik va texnologiya", "Fan nomi", "Yo'nalish", ENGINEERING_UZ)
)

CHEMISTRY_EN = [
    ("Agrochemical service in agriculture", "Chemistry"),
    ("Agrochemistry in cotton", "Chemistry"),
    ("The Methods of agrochemical testing", "Chemistry"),
    ("Analytical and organic chemistry", "Chemistry"),
    ("Analytical, physicolloid and bioorganic chemistry", "Chemistry"),
    ("Biochemistry and sports biochemistry", "Chemistry"),
    ("Biochemistry of agricultural products", "Chemistry"),
    ("Biochemistry", "Chemistry"),
    ("Chemical ecology and environmental protection", "Chemistry"),
    ("Physical chemistry", "Chemistry"),
    ("Chemistry for physicists", "Chemistry"),
    ("Food chemistry", "Chemistry"),
    ("Food chemistry and analysis", "Chemistry"),
    ("Food chemistry and biochemistry", "Chemistry"),
    ("Chemistry of heterocyclic compounds", "Chemistry"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Chemistry", "Course Name", "Field", CHEMISTRY_EN)
)

CHEMISTRY_UZ = [
    ("Qishloq xo'jaligida agrokimyoviy xizmatlar", "Kimyo"),
    ("Paxtachilikda agrokimyo", "Kimyo"),
    ("Agrokimyoviy tahlil usullari", "Kimyo"),
    ("Analitik va organik kimyo", "Kimyo"),
    ("Analitik, fizik-kolloid va bioorganik kimyo", "Kimyo"),
    ("Biokimyo va sport biokimyosi", "Kimyo"),
    ("Qishloq xo'jaligi mahsulotlari biokimyosi", "Kimyo"),
    ("Biokimyo", "Kimyo"),
    ("Kimyoviy ekologiya va atrof-muhitni muhofaza qilish", "Kimyo"),
    ("Fizik kimyo", "Kimyo"),
    ("Fiziklar uchun kimyo", "Kimyo"),
    ("Oziq-ovqat kimyosi", "Kimyo"),
    ("Oziq-ovqat kimyosi va tahlili", "Kimyo"),
    ("Oziq-ovqat kimyosi va biokimyosi", "Kimyo"),
    ("Geterotsiklik birikmalar kimyosi", "Kimyo"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Kimyo", "Fan nomi", "Yo'nalish", CHEMISTRY_UZ)
)

GEOGRAPHY_EN = [
    ("Applied ecology", "Geography & Earth Sciences"),
    ("Basic problems of geography", "Geography & Earth Sciences"),
    ("Basics of land cadastre and soil inspection", "Geography & Earth Sciences"),
    ("Biogeography", "Geography & Earth Sciences"),
    ("Differential Geometry", "Geography & Earth Sciences"),
    ("Differential geometry and topology", "Geography & Earth Sciences"),
    ("Earthquake and human struggle", "Geography & Earth Sciences"),
    ("Ecology and environmental protection", "Geography & Earth Sciences"),
    ("Economic Geography", "Geography & Earth Sciences"),
    ("Ecology and nature conservation", "Geography & Earth Sciences"),
    ("Ecology and environmental conservation", "Geography & Earth Sciences"),
    ("Environmental policy", "Geography & Earth Sciences"),
    ("Environmental law", "Geography & Earth Sciences"),
    ("Environmental impact assessment", "Geography & Earth Sciences"),
    ("Fundamentals of geometry", "Geography & Earth Sciences"),
    ("Fundamentals of geomorphology and geology", "Geography & Earth Sciences"),
    ("Fundamentals of population and economic geography", "Geography & Earth Sciences"),
    ("Geobotany / phytosenology", "Geography & Earth Sciences"),
    ("Geoecology and landscape ecology", "Geography & Earth Sciences"),
    ("The doctrine of the geographical crust", "Geography & Earth Sciences"),
    ("Innovative technologies in teaching geography", "Geography & Earth Sciences"),
    ("Methods of teaching geography", "Geography & Earth Sciences"),
    ("Geographical research methods", "Geography & Earth Sciences"),
    ("Geography of Central Asia", "Geography & Earth Sciences"),
    ("Geography of service areas", "Geography & Earth Sciences"),
    ("Geography of small areas", "Geography & Earth Sciences"),
    ("Geography of tourism", "Geography & Earth Sciences"),
    ("Geography of tourist destinations", "Geography & Earth Sciences"),
    ("Geography of Uzbekistan", "Geography & Earth Sciences"),
    ("Geoinformation technologies in ecology", "Geography & Earth Sciences"),
    ("Geology. Soil geography", "Geography & Earth Sciences"),
    ("Geometry and algebra", "Geography & Earth Sciences"),
    ("Global Geopolitics, Migration and Uneven Development", "Geography & Earth Sciences"),
    ("Fundamentals of geopolitics", "Geography & Earth Sciences"),
    ("Human behavior and the social environment", "Geography & Earth Sciences"),
    ("Human resources economics", "Geography & Earth Sciences"),
    ("Hydroecology and geoecology", "Geography & Earth Sciences"),
    ("Industry information resources", "Geography & Earth Sciences"),
    ("Human ecology", "Geography & Earth Sciences"),
    ("Introduction to Economic Geography", "Geography & Earth Sciences"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Geography & Earth Sciences", "Course Name", "Field", GEOGRAPHY_EN)
)

GEOGRAPHY_UZ = [
    ("Amaliy ekologiya", "Geografiya va Yer fanlari"),
    ("Geografiyaning asosiy muammolari", "Geografiya va Yer fanlari"),
    ("Yer kadastri va tuproqni baholash asoslari", "Geografiya va Yer fanlari"),
    ("Biogeografiya", "Geografiya va Yer fanlari"),
    ("Differensial geometriya", "Geografiya va Yer fanlari"),
    ("Differensial geometriya va topologiya", "Geografiya va Yer fanlari"),
    ("Zilzila va inson kurashi", "Geografiya va Yer fanlari"),
    ("Ekologiya va atrof-muhitni muhofaza qilish", "Geografiya va Yer fanlari"),
    ("Iqtisodiy geografiya", "Geografiya va Yer fanlari"),
    ("Ekologiya va tabiatni muhofaza qilish", "Geografiya va Yer fanlari"),
    ("Ekologik siyosat", "Geografiya va Yer fanlari"),
    ("Ekologik huquq", "Geografiya va Yer fanlari"),
    ("Atrof-muhitga ta'sirni baholash", "Geografiya va Yer fanlari"),
    ("Geometriya asoslari", "Geografiya va Yer fanlari"),
    ("Geomorfologiya va geologiya asoslari", "Geografiya va Yer fanlari"),
    ("Aholi va iqtisodiy geografiya asoslari", "Geografiya va Yer fanlari"),
    ("Geobotanika / fitotsenologiya", "Geografiya va Yer fanlari"),
    ("Geoekologiya va landshaft ekologiyasi", "Geografiya va Yer fanlari"),
    ("Geografik qobiq haqidagi ta'limot", "Geografiya va Yer fanlari"),
    ("Geografiyani o'qitishda innovatsion texnologiyalar", "Geografiya va Yer fanlari"),
    ("Geografiyani o'qitish metodikasi", "Geografiya va Yer fanlari"),
    ("Geografik tadqiqot usullari", "Geografiya va Yer fanlari"),
    ("Markaziy Osiyo geografiyasi", "Geografiya va Yer fanlari"),
    ("Xizmat ko'rsatish sohalari geografiyasi", "Geografiya va Yer fanlari"),
    ("Kichik hududlar geografiyasi", "Geografiya va Yer fanlari"),
    ("Turizm geografiyasi", "Geografiya va Yer fanlari"),
    ("Turistik manzillar geografiyasi", "Geografiya va Yer fanlari"),
    ("O'zbekiston geografiyasi", "Geografiya va Yer fanlari"),
    ("Ekologiyada geoinformatsion texnologiyalar", "Geografiya va Yer fanlari"),
    ("Geologiya. Tuproq geografiyasi", "Geografiya va Yer fanlari"),
    ("Geometriya va algebra", "Geografiya va Yer fanlari"),
    ("Global geopolitika, migratsiya va notekis rivojlanish", "Geografiya va Yer fanlari"),
    ("Geosiyosat asoslari", "Geografiya va Yer fanlari"),
    ("Inson xulqi va ijtimoiy muhit", "Geografiya va Yer fanlari"),
    ("Inson resurslari iqtisodiyoti", "Geografiya va Yer fanlari"),
    ("Gidroekologiya va geoekologiya", "Geografiya va Yer fanlari"),
    ("Tarmoq axborot resurslari", "Geografiya va Yer fanlari"),
    ("Inson ekologiyasi", "Geografiya va Yer fanlari"),
    ("Iqtisodiy geografiyaga kirish", "Geografiya va Yer fanlari"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Geografiya va Yer fanlari", "Fan nomi", "Yo'nalish", GEOGRAPHY_UZ)
)

PHYSICS_EN = [
    ("Applied optics", "Physics"),
    ("Biophysics", "Physics"),
    ("Condensed matter physics", "Physics"),
    ("Differential equations and mathematical physics", "Physics"),
    ("Methods of teaching physics", "Physics"),
    ("Methods and history of teaching physics", "Physics"),
    ("Fundamentals of Physics and Astronomy", "Physics"),
    ("Physics in ecology", "Physics"),
    ("Fundamentals of nanophysics", "Physics"),
    ("Fundamentals of thermodynamics", "Physics"),
    ("General physics", "Physics"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Physics", "Course Name", "Field", PHYSICS_EN)
)

PHYSICS_UZ = [
    ("Amaliy optika", "Fizika"),
    ("Biofizika", "Fizika"),
    ("Qattiq jismlar fizikasi", "Fizika"),
    ("Differensial tenglamalar va matematik fizika", "Fizika"),
    ("Fizikani o'qitish metodikasi", "Fizika"),
    ("Fizikani o'qitish metodlari va tarixi", "Fizika"),
    ("Fizika va astronomiya asoslari", "Fizika"),
    ("Ekologiyada fizika", "Fizika"),
    ("Nanofizika asoslari", "Fizika"),
    ("Termodinamika asoslari", "Fizika"),
    ("Umumiy fizika", "Fizika"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Fizika", "Fan nomi", "Yo'nalish", PHYSICS_UZ)
)

MEDICINE_EN = [
    ("Basics of healthy eating", "Medicine & Health"),
    ("Career development", "Medicine & Health"),
    ("Ecological physiology", "Medicine & Health"),
    ("Fundamentals of health preservation", "Medicine & Health"),
    ("Health and Life safety", "Medicine & Health"),
    ("Hygienical basic formation of healthy children", "Medicine & Health"),
    ("Digestion and nutritional physiology", "Medicine & Health"),
    ("Plant nutrition and fertilizers", "Medicine & Health"),
    ("Protection of greenhouse crops from diseases", "Medicine & Health"),
    ("The Public health and health care organization", "Medicine & Health"),
    ("Health and Life Safety", "Medicine & Health"),
    ("Basics of health knowledge and healthy lifestyles", "Medicine & Health"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Medicine & Health", "Course Name", "Field", MEDICINE_EN)
)

MEDICINE_UZ = [
    ("Sog'lom ovqatlanish asoslari", "Tibbiyot va sog'liqni saqlash"),
    ("Karyera rivojlanishi", "Tibbiyot va sog'liqni saqlash"),
    ("Ekologik fiziologiya", "Tibbiyot va sog'liqni saqlash"),
    ("Salomatlikni saqlash asoslari", "Tibbiyot va sog'liqni saqlash"),
    ("Hayot faoliyati xavfsizligi", "Tibbiyot va sog'liqni saqlash"),
    ("Bolalarda sog'lom turmush gigiyenasi asoslari", "Tibbiyot va sog'liqni saqlash"),
    ("Hazm qilish va oziqlanish fiziologiyasi", "Tibbiyot va sog'liqni saqlash"),
    ("O'simliklar oziqlanishi va o'g'itlar", "Tibbiyot va sog'liqni saqlash"),
    ("Issiqxona ekinlarini kasalliklardan himoya qilish", "Tibbiyot va sog'liqni saqlash"),
    ("Jamoat salomatligi va sog'liqni saqlashni tashkil etish", "Tibbiyot va sog'liqni saqlash"),
    ("Sog'lom turmush tarzi va salomatlik bilimlari asoslari", "Tibbiyot va sog'liqni saqlash"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Tibbiyot va sog'liqni saqlash", "Fan nomi", "Yo'nalish", MEDICINE_UZ)
)

PEDAGOGY_EN = [
    ("Developmental psychology", "Pedagogy & Education"),
    ("Methods of teaching ecological sciences", "Pedagogy & Education"),
    ("General and developmental psychology", "Pedagogy & Education"),
    ("Developmental psychology. Pedagogical psychology", "Pedagogy & Education"),
    ("Developmental psychology. Differential psychology", "Pedagogy & Education"),
    ("Teaching biology", "Pedagogy & Education"),
    ("Theory and methodology of speech development", "Pedagogy & Education"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Pedagogy & Education", "Course Name", "Field", PEDAGOGY_EN)
)

PEDAGOGY_UZ = [
    ("Rivojlanish psixologiyasi", "Pedagogika"),
    ("Ekologiya fanlarini o'qitish metodikasi", "Pedagogika"),
    ("Umumiy va rivojlanish psixologiyasi", "Pedagogika"),
    ("Rivojlanish psixologiyasi. Pedagogik psixologiya", "Pedagogika"),
    ("Rivojlanish psixologiyasi. Differensial psixologiya", "Pedagogika"),
    ("Biologiyani o'qitish metodikasi", "Pedagogika"),
    ("Nutq rivojlantirish nazariyasi va metodikasi", "Pedagogika"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Pedagogika", "Fan nomi", "Yo'nalish", PEDAGOGY_UZ)
)

ECONOMICS_EN = [
    ("Energy management", "Economics"),
    ("Green Economy", "Economics"),
    ("Human resources economics", "Economics"),
    ("Management of vital factors of vegetable crops in the greenhouse", "Economics"),
    ("New strategy and competitiveness (firms, clusters and economic development)", "Economics"),
    ("Organization and management of greenhouse economy", "Economics"),
    ("The Energy management", "Economics"),
    ("The Human resource management", "Economics"),
    ("Fundamentals of Business Analysis in Software Development", "Economics"),
]
SUSTAINABILITY_SUBJECTS_TABLES_EN.append(
    _build_table("Economics", "Course Name", "Field", ECONOMICS_EN)
)

ECONOMICS_UZ = [
    ("Energiya menejmenti", "Iqtisodiyot"),
    ("Yashil iqtisodiyot", "Iqtisodiyot"),
    ("Inson resurslari iqtisodiyoti", "Iqtisodiyot"),
    ("Issiqxonada sabzavot ekinlarining muhim omillarini boshqarish", "Iqtisodiyot"),
    ("Yangi strategiya va raqobatbardoshlik (firmalar, klasterlar va iqtisodiy rivojlanish)", "Iqtisodiyot"),
    ("Issiqxona xo'jaligini tashkil etish va boshqarish", "Iqtisodiyot"),
    ("Inson resurslarini boshqarish", "Iqtisodiyot"),
    ("Dasturiy ta'minotni ishlab chiqishda biznes tahlili asoslari", "Iqtisodiyot"),
]
SUSTAINABILITY_SUBJECTS_TABLES_UZ.append(
    _build_table("Iqtisodiyot", "Fan nomi", "Yo'nalish", ECONOMICS_UZ)
)

SUSTAINABILITY_SUBJECTS_RAW_HTML_EN = """
<div class="governance-richtext">
  <p><strong>SUBJECTS RELATED TO SUSTAINABILITY</strong></p>
  <p>Karshi State University demonstrates a strong institutional commitment to integrating environmental awareness and sustainability principles across its academic programs. The university offers a total of <strong>169 courses</strong> that incorporate topics related to sustainability, environmental protection, renewable energy, biotechnology, and social responsibility.</p>
  <p>These courses span multiple faculties, including Engineering &amp; Technology, Chemistry, Geography &amp; Earth Sciences, Physics, Economics, Medicine &amp; Health, and Pedagogy &amp; Education, ensuring that sustainability concepts are embedded in both scientific and socio-economic disciplines.</p>
  <p>Through these sustainability-related courses, the university aligns its academic offerings with the UN Sustainable Development Goals, especially SDG 4, SDG 7, SDG 13, and SDG 15, and equips students with knowledge and skills for local, national, and global sustainable development.</p>
  {tables}
</div>
""".strip().format(tables="".join(SUSTAINABILITY_SUBJECTS_TABLES_EN))

SUSTAINABILITY_SUBJECTS_RAW_HTML_UZ = """
<div class="governance-richtext">
  <p><strong>BARQARORLIK OID FANLAR</strong></p>
  <p>Qarshi davlat universiteti o'zining ta'lim dasturlariga ekologik ong va barqaror rivojlanish tamoyillarini integratsiya qilish bo'yicha kuchli institutsional majburiyatni namoyon etadi. Universitetda barqarorlik, atrof-muhitni muhofaza qilish, qayta tiklanuvchi energiya, biotexnologiya va ijtimoiy mas'uliyatga oid mavzularni qamrab olgan jami <strong>169 ta fan</strong> mavjud.</p>
  <p>Mazkur fanlar turli fakultetlar, jumladan, muhandislik va texnologiya, kimyo, geografiya va Yer fanlari, fizika, iqtisodiyot, tibbiyot va sog'liqni saqlash hamda pedagogika yo'nalishlarini qamrab olib, barqarorlik tushunchalarining nafaqat ilmiy, balki ijtimoiy-iqtisodiy fanlarga ham singdirilganini ta'minlaydi.</p>
  <p>Mazkur barqarorlikka oid fanlar orqali Qarshi davlat universiteti o'z ta'lim dasturlarini BMTning Barqaror rivojlanish maqsadlari, xususan, 4-maqsad, 7-maqsad, 13-maqsad va 15-maqsad bilan uyg'unlashtiradi hamda talabalarni barqaror rivojlanishga hissa qo'sha oladigan bilim va ko'nikmalar bilan ta'minlaydi.</p>
  {tables}
</div>
""".strip().format(tables="".join(SUSTAINABILITY_SUBJECTS_TABLES_UZ))
