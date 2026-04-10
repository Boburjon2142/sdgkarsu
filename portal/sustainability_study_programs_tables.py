def _build_programs_table(title, heading_number, heading_faculty, heading_program, groups):
    rows = []
    for index, (faculty, programs) in enumerate(groups, start=1):
        first = True
        for program in programs:
            number_cell = str(index) if first else ""
            faculty_cell = faculty if first else ""
            rows.append(
                f"<tr><td>{number_cell}</td><td>{faculty_cell}</td><td>{program}</td></tr>"
            )
            first = False

    body = "".join(rows)
    return (
        f'<h2>{title}</h2>'
        '<div class="governance-table-wrap">'
        '<table class="governance-table governance-table--narrow-first">'
        f'<thead><tr><th>{heading_number}</th><th>{heading_faculty}</th><th>{heading_program}</th></tr></thead>'
        f'<tbody>{body}</tbody>'
        '</table>'
        '</div>'
    )


STUDY_PROGRAM_GROUPS_EN = [
    (
        "Pedagogy",
        [
            "Primary Education",
            "Special Pedagogy: Speech Therapy (Logopedics)",
            "Preschool Education",
            "Psychology",
        ],
    ),
    (
        "Mathematics and Computer Sciences",
        [
            "Mathematics",
            "Software Engineering",
            "Information Systems and Technologies",
            "Artificial Intelligence",
            "Mechanics and Mathematical Modeling",
        ],
    ),
    (
        "Economics",
        [
            "Economics",
            "Finance and Financial Technologies",
            "Banking",
            "Accounting",
            "Marketing",
            "Tourism and Hospitality",
        ],
    ),
    (
        "Physics",
        [
            "Physics",
            "Electronics and Instrumentation",
            "Power Engineering",
            "Light Industry Engineering",
            "Renewable Energy Sources",
        ],
    ),
    (
        "Chemistry and Biology",
        [
            "Chemistry",
            "Biology",
            "Microbiology",
            "Biotechnology",
        ],
    ),
    (
        "Medicine",
        [
            "General Medicine",
            "Pediatrics",
        ],
    ),
    (
        "Geography and Agronomy",
        [
            "Plant Protection and Quarantine",
            "Geography",
            "Agrochemistry and Soil Science",
            "Ecology and Environmental Protection",
            "Soil Science",
        ],
    ),
]

STUDY_PROGRAM_GROUPS_UZ = [
    (
        "Pedagogika",
        [
            "Boshlang'ich ta'lim",
            "Maxsus pedagogika: Logopediya",
            "Maktabgacha ta'lim",
            "Psixologiya",
        ],
    ),
    (
        "Matematika va kompyuter fanlari",
        [
            "Matematika",
            "Dasturiy injiniring",
            "Axborot tizimlari va texnologiyalari",
            "Sun'iy intellekt",
            "Mexanika va matematik modellashtirish",
        ],
    ),
    (
        "Iqtisodiyot",
        [
            "Iqtisodiyot",
            "Moliya va moliyaviy texnologiyalar",
            "Bank ishi",
            "Buxgalteriya hisobi",
            "Marketing",
            "Turizm va mehmondo'stlik",
        ],
    ),
    (
        "Fizika",
        [
            "Fizika",
            "Elektronika va asbobsozlik",
            "Energetika",
            "Yengil sanoat muhandisligi",
            "Qayta tiklanuvchi energiya manbalari",
        ],
    ),
    (
        "Kimyo va biologiya",
        [
            "Kimyo",
            "Biologiya",
            "Mikrobiologiya",
            "Biotexnologiya",
        ],
    ),
    (
        "Tibbiyot",
        [
            "Davolash ishi",
            "Pediatriya",
        ],
    ),
    (
        "Geografiya va Agronomiya",
        [
            "O'simliklarni himoya qilish va karantin",
            "Geografiya",
            "Agrokimyo va tuproqshunoslik",
            "Ekologiya va atrof-muhitni muhofaza qilish",
            "Tuproqshunoslik",
        ],
    ),
]

SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_EN = """
<div class="governance-richtext">
  <p><strong>STUDY PROGRAMS RELATED TO SUSTAINABILITY</strong></p>
  <p>Karshi State University actively integrates sustainability principles into its academic programs, ensuring that future professionals are equipped with the knowledge and skills to address global environmental, social, and economic challenges.</p>
  <p>A total of seven faculties at the university offer study programs directly related to sustainability, encompassing environmental protection, renewable energy, sustainable agriculture, education, and social well-being. These programs contribute to the achievement of the UN Sustainable Development Goals (SDGs), particularly SDG 4 (Quality Education), SDG 7 (Affordable and Clean Energy), SDG 13 (Climate Action), and SDG 15 (Life on Land).</p>
  <ul class="governance-bullet-list">
    <li><strong>Faculty of Pedagogy</strong> offers programs such as Primary Education, Preschool Education, Special Pedagogy (Speech Therapy), and Psychology, which promote sustainable education, inclusive learning, and the development of social and emotional well-being.</li>
    <li><strong>Faculty of Mathematics and Computer Sciences</strong> includes programs such as Software Engineering, Information Systems and Technologies, Artificial Intelligence, and Mathematical Modeling, providing students with digital and analytical skills essential for designing sustainable and efficient technological solutions.</li>
    <li><strong>Faculty of Economics</strong> offers programs in Economics, Finance and Financial Technologies, Banking, Accounting, Marketing, and Tourism and Hospitality. These programs support the transition to a green economy, sustainable finance, and responsible tourism management.</li>
    <li><strong>Faculty of Physics</strong> provides programs in Physics, Electronics and Instrumentation, Power Engineering, Light Industry Engineering, and Renewable Energy Sources. These programs focus on energy efficiency, clean energy production, and the development of environmentally friendly technologies.</li>
    <li><strong>Faculty of Chemistry and Biology</strong> offers programs such as Chemistry, Biology, Microbiology, and Biotechnology, which contribute to sustainable agriculture, pollution control, and the advancement of eco-friendly scientific research.</li>
    <li><strong>Faculty of Medicine</strong> includes programs in General Medicine and Pediatrics, which emphasize human health, environmental safety, and sustainable healthcare practices.</li>
    <li><strong>Faculty of Geography and Agronomy</strong> provides programs such as Plant Protection and Quarantine, Geography, Agrochemistry and Soil Science, Ecology and Environmental Protection, and Soil Science. These programs directly support sustainable land management, environmental conservation, and climate adaptation practices.</li>
  </ul>
  <p>Through these multidisciplinary programs, Karshi State University fosters sustainability-oriented education and research across its academic structure, ensuring that graduates contribute to sustainable development in their respective professional fields.</p>
  %s
</div>
""" % _build_programs_table(
    "Study programs by faculty",
    "No",
    "Faculty",
    "Study programs",
    STUDY_PROGRAM_GROUPS_EN,
)

SUSTAINABILITY_STUDY_PROGRAMS_RAW_HTML_UZ = """
<div class="governance-richtext">
  <p><strong>BARQARORLIKKA OID TA'LIM DASTURLARI</strong></p>
  <p>Qarshi davlat universiteti o'zining ta'lim dasturlariga barqaror rivojlanish tamoyillarini faol ravishda integratsiya qilib, kelajak mutaxassislarini global ekologik, ijtimoiy va iqtisodiy muammolarni hal etishga zarur bilim va ko'nikmalar bilan ta'minlamoqda.</p>
  <p>Universitetda jami yettita fakultet barqarorlik bilan bevosita bog'liq ta'lim dasturlarini taklif etadi. Ushbu dasturlar atrof-muhitni muhofaza qilish, qayta tiklanuvchi energiya, barqaror qishloq xo'jaligi, ta'lim va ijtimoiy farovonlik kabi yo'nalishlarni qamrab oladi. Mazkur dasturlar BMTning Barqaror rivojlanish maqsadlariga, xususan, 4-maqsad (Sifatli ta'lim), 7-maqsad (Arzon va toza energiya), 13-maqsad (Iqlim o'zgarishiga qarshi kurash) va 15-maqsad (Quruqlikdagi hayot)ga erishishga xizmat qiladi.</p>
  <ul class="governance-bullet-list">
    <li><strong>Pedagogika fakulteti</strong>. Boshlang'ich ta'lim, Maktabgacha ta'lim, Maxsus pedagogika (logopediya) va Psixologiya kabi dasturlarni taklif etadi. Ushbu dasturlar barqaror ta'lim, inklyuziv o'qitish hamda ijtimoiy va emotsional farovonlikni rivojlantirishga xizmat qiladi.</li>
    <li><strong>Matematika va kompyuter ilmlari fakulteti</strong>. Dasturiy injiniring, Axborot tizimlari va texnologiyalari, Sun'iy intellekt hamda Matematik modellashtirish kabi yo'nalishlarni o'z ichiga oladi. Bu dasturlar talabalarni barqaror va samarali texnologik yechimlarni ishlab chiqish uchun zarur bo'lgan raqamli va tahliliy ko'nikmalar bilan ta'minlaydi.</li>
    <li><strong>Iqtisodiyot fakulteti</strong>. Iqtisodiyot, Moliya va moliyaviy texnologiyalar, Bank ishi, Buxgalteriya hisobi, Marketing hamda Turizm va mehmondo'stlik kabi dasturlarni taklif etadi. Ushbu yo'nalishlar yashil iqtisodiyotga o'tish, barqaror moliya tizimini rivojlantirish va mas'uliyatli turizmni boshqarishni qo'llab-quvvatlaydi.</li>
    <li><strong>Fizika fakulteti</strong>. Fizika, Elektronika va asbobsozlik, Energetika, Yengil sanoat muhandisligi va Qayta tiklanuvchi energiya manbalari kabi dasturlarni o'z ichiga oladi. Bu dasturlar energiya samaradorligi, toza energiya ishlab chiqarish va ekologik toza texnologiyalarni rivojlantirishga qaratilgan.</li>
    <li><strong>Kimyo va biologiya fakulteti</strong>. Kimyo, Biologiya, Mikrobiologiya va Biotexnologiya yo'nalishlarini taklif etadi. Ushbu dasturlar barqaror qishloq xo'jaligi, atrof-muhit ifloslanishini kamaytirish va ekologik xavfsiz ilmiy tadqiqotlarni rivojlantirishga xizmat qiladi.</li>
    <li><strong>Tibbiyot fakulteti</strong>. Davolash ishi va Pediatriya yo'nalishlarini o'z ichiga oladi. Bu dasturlar inson salomatligi, ekologik xavfsizlik va barqaror sog'liqni saqlash amaliyotlariga alohida e'tibor qaratadi.</li>
    <li><strong>Geografiya va Agronomiya fakulteti</strong>. O'simliklarni himoya qilish va karantin, Geografiya, Agrokimyo va tuproqshunoslik, Ekologiya va atrof-muhitni muhofaza qilish, Tuproqshunoslik kabi yo'nalishlarni taklif etadi. Ushbu dasturlar yer resurslarini barqaror boshqarish, tabiatni muhofaza qilish va iqlim o'zgarishiga moslashish choralarini qo'llab-quvvatlaydi.</li>
  </ul>
  <p>Mazkur ko'p tarmoqli ta'lim dasturlari orqali Qarshi davlat universiteti o'zining akademik tuzilmasida barqarorlikka yo'naltirilgan ta'lim va ilmiy tadqiqotlarni rivojlantirib, bitiruvchilarning turli kasbiy sohalarda barqaror rivojlanishga hissa qo'shishini ta'minlaydi.</p>
  %s
</div>
""" % _build_programs_table(
    "Fakultetlar kesimidagi ta'lim dasturlari",
    "№",
    "Fakultet",
    "Ta'lim dasturlari",
    STUDY_PROGRAM_GROUPS_UZ,
)
