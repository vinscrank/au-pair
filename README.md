# Au pair

Au pair matches au pairs and babysitters with host families in Dublin. Both sides complete a profile, then browse cards. A like from both people is a match, and only then is WhatsApp shown.

The brand is a warm paper-and-ink listing, not a dating app: Fraunces and Outfit, cream `#F3EEE6`, ink `#1C2B26`, clay `#C6533A`, honey `#E4B15A`. The mark is a doorway with a hearth dot.

## Run it locally

Postgres, from the repo root:

```bash
docker compose up -d
cp .env.example .env
cp .env.example backend/.env
```

`DATABASE_URL` in those files is the local database. When you have Neon, paste that single connection string over `DATABASE_URL` in both files. `postgresql://` and `postgres://` are accepted. Keep `sslmode=require`. Leave the driver prefix off; the app adds `postgresql+psycopg`. The pooler connection disables server-side prepared statements so transaction pooling still works. Replace `JWT_SECRET` before any shared deployment. The Neon password stays only in the gitignored `.env` files. `.env.example` is a placeholder. Do not commit `.env`.

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

Frontend, in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The Next app proxies `/api` and `/uploads` to the API, and the session cookie is httpOnly.

`python -m app.seed` loads eight fictional Dublin profiles and can be run again. It only replaces the `@demo.aupair.ie` accounts.

Demo password for every seed account: `dublin-demo`

| Email | Role |
| --- | --- |
| sofia.rossi@demo.aupair.ie | Candidate, live-in au pair |
| aoife.nolan@demo.aupair.ie | Candidate, northside babysitter |
| mateusz.kowal@demo.aupair.ie | Candidate, Dublin 15, drives |
| ines.moreau@demo.aupair.ie | Candidate, south coast, live-in |
| niamh.brennan@demo.aupair.ie | Family, Rathgar |
| ada.okonkwo@demo.aupair.ie | Family, Blanchardstown |
| orla.byrne@demo.aupair.ie | Family, Clontarf evenings |
| ciara.murphy@demo.aupair.ie | Family, Blackrock after school |

Seed photos are Unsplash placeholders. The names and bios are fictional.

## Profiles

Fields follow what Dublin ads actually ask, not a generic form.

- AuPairWorld's Ireland notes: childcare plus light housework, hours, pocket money, a separate room for live-in, driving and insurance when a car is involved.
- Au pair job posts (children, ages, city, start, duration, weekly hours, pocket money, languages at home, a plain-language schedule).
- mindme.ie babysitter profiles: age, area, hourly rate or negotiable, years of experience, age bands from newborn to teenagers, own transport, pets, short notice, smoker, languages, qualification, first aid, self-reported Garda vetting, driving licence, and whether care is in the family's home.

Family profiles also include Vincenzo's questions: name, WhatsApp, where care is needed, children's ages, the schedule, and start timing (as soon as possible, within a few weeks, or just exploring).

Discover stays locked until the server marks the profile complete. Cards show the short version. The full profile opens from the card.

## Contact, later

WhatsApp for the other person is added only in `backend/app/contact_gate.py` (`allow_contact`). Today it requires a mutual match and the viewer's id. A payment check belongs in that function. The app does not take payment. Discover responses do not include a number. Matches include `contact.available` and `contact.value`.

## Checks

```bash
cd backend && python -m unittest tests.test_flow
```
