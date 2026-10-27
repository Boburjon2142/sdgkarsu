# Serverni yangilash

Ushbu reliz: responsive sahifalar, SDG admin paneli, matn/jadval bloklari.
Repo: https://github.com/Boburjon2142/sdgkarsu — `main` branch.
Yangi model migratsiyasi yo'q. Eski oddiy matnli yangiliklar ham ishlaydi.

## 1. Muhit va zaxira

Quyidagi buyruqlar serverdagi **Bash** terminali uchun. Loyiha katalogiga
kiring va serverning mavjud virtual muhitini faollashtiring:

```bash
cd /path/to/sdgkarsu
source /path/to/venv/bin/activate
git status --short
```

Kuzatiladigan kod fayllarida lokal o'zgarishlar bo'lsa, ularni avval ko'rib
chiqing va saqlang; `reset --hard` ishlatmang. Serverdagi `.env` ni saqlang.
`.env.example` ni production `.env` ustiga nusxalamang.

Yangilash vaqtida kontent tahririni vaqtincha to'xtating. Standart
`db.sqlite3` ishlatilsa, izchil zaxira nusxasini oling:

```bash
mkdir -p "$HOME/sdg-backups"
python - <<'PY'
import sqlite3
from datetime import datetime
from pathlib import Path

source = Path('db.sqlite3')
if not source.is_file():
    raise SystemExit('db.sqlite3 topilmadi. DATABASE_URL bazasini alohida zaxiralang.')
target = Path.home() / 'sdg-backups' / ('db-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.sqlite3')
with sqlite3.connect(source) as original, sqlite3.connect(target) as backup:
    original.backup(backup)
print(target)
PY
```

`DATABASE_URL` boshqa SQLite fayliga ishora qilsa, yuqoridagi `source` ni
moslang. PostgreSQL/MySQL uchun o'z bazangizning backup vositasini ishlating.
`media/` va `.env` ni ham maxfiy, xavfsiz joyga zaxiralang. Mavjud media
fayllarini deploy paytida o'chirmang yoki demo kontent bilan almashtirmang.

## 2. Kod, paketlar va statik fayllar

```bash
git rev-parse HEAD
git fetch origin
git switch main
git pull --ff-only origin main
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Birinchi buyruq chiqargan eski commitni rollback uchun yozib oling.
Biror buyruq xato bersa, keyingi qadamga o'tmasdan sababini tuzating.
`check --deploy` ogohlantirishlarini production sozlamalari bilan solishtiring.

Production muhitida:

```dotenv
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=sdg.qarshidu.uz,www.sdg.qarshidu.uz
DJANGO_CSRF_TRUSTED_ORIGINS=https://sdg.qarshidu.uz,https://www.sdg.qarshidu.uz
DJANGO_SECURE_SSL_REDIRECT=1
```

`DJANGO_SECRET_KEY` serverdagi mavjud maxfiy qiymat bo'lib qoladi.
HTTPS proxy `X-Forwarded-Proto` ni to'g'ri uzatishi kerak.
Redis faqat mavjud xizmat bo'lsa `CACHE_URL` orqali yoqilsin; aks holda
`CACHE_URL` bo'sh bo'lishi mumkin. Mavjud `DATABASE_URL` ni saqlang.

## 3. Web ilovani qayta yuklash

**PythonAnywhere:** Web sahifasida kerakli domenni ochib **Reload** bosing.
`/static/` mapping loyiha `staticfiles/` katalogiga, `/media/` esa `media/`
katalogiga qarasin. Virtualenv yo'li paketlar o'rnatilgan muhitga mos bo'lsin.

**VPS / systemd:** xizmatning haqiqiy nomi bilan quyidagini bajaring:

```bash
sudo systemctl restart YOUR_DJANGO_SERVICE
sudo systemctl status YOUR_DJANGO_SERVICE --no-pager
```

Template va Python o'zgarishlari kuchga kirishi uchun barcha Django workerlar
qayta ishga tushishi kerak. Production uchun `runserver` ishlatmang.

## 4. Tekshirish

```bash
curl --fail https://sdg.qarshidu.uz/health/
curl --fail -I https://sdg.qarshidu.uz/static/css/admin-layout.css
curl --fail -I https://sdg.qarshidu.uz/static/css/admin-news-editor.css
curl --fail -I https://sdg.qarshidu.uz/static/js/admin-news-blocks.js
```

Brauzerda `Ctrl + F5` bosing. `/admin/` da SDG tanlab, yangilikka matn,
jadval va rasm qo'shib saqlang; saytda matn-jadval tartibi, mobil ko'rinish
va eski yangiliklarni tekshiring. CDN bo'lsa, uning statik fayl keshini yangilang.
`health/` faqat ilova javob berishini tekshiradi, bazani tekshirmaydi.

## Rollback

Zarurat bo'lsa, saqlangan eski commitga `git switch --detach OLD_COMMIT`
orqali qayting, o'sha commit paketlarini o'rnating, `collectstatic` ni qayta
bajaring va web ilovani reload qiling. Ushbu reliz schema migratsiyasini
qo'shmaydi, ammo eski kod yangi jadval bloklarini tushunmaydi. Jadval bilan
yaratilgan yangiliklarni rollbackdan oldin hisobga oling. Bazani zaxiradan
tiklash keyinroq qo'shilgan yangiliklarni yo'qotishi mumkin.

## Lokal tekshiruv natijasi

Admin uchun 9 ta test o'tgan. Butun `portal` to'plamida 38 testdan 36 tasi
o'tgan; oldindan mavjud ikki test kontentdagi sanalarni topmaydi:
`test_disability_support_roadmap_loads` (`June 2026`) va
`test_governance_meeting_minutes_detail_loads` (`February 2025`).
