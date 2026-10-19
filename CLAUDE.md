# ChicCheckCar — car-sales website

Hebrew (RTL) car-sales site for the owner's dealership. Built originally as a claude.ai artifact and exported here unchanged.

## Structure

```
site/
  index.html     Main page: entry gate, scroll-scrubbed intro (kframes/), catalog (CARS data inside), finance calculator,
                 contact form, side menu, cart drawer, legal modals, and the admin / leads center (CRM).
  car.html       Per-car page, routed by hash: car.html#car<N> (N = index in CARS). GENERATED — do not hand-edit.
  me.html        Customer personal area: cart / my requests / my details. GENERATED — do not hand-edit.
  auth.js        Customer account: registration, sign-in, password reset (ID number + date of birth), shared by all pages.
  loan.js        "רכישה זריזה" 5-step financing-eligibility wizard (amount, personal, income, trade-in, summary).
  kframes/       156 intro frames (k001–k156.jpg) scrubbed by scroll.
  logo.png, logo-wide.png, car-sample.png (placeholder: covered car — used when a model has no photo).
tools/
  gen_car.py     python3 tools/gen_car.py site   -> rebuilds site/car.html from CARS in index.html + tools/specs/specs.json
  gen_me.py      python3 tools/gen_me.py site    -> rebuilds site/me.html (copies cccLead / cccDone / okbox from index.html)
  specs/         Technical specs per model group (sources listed inside).
```

After editing index.html (CARS, cccLead, cccDone, okbox styles) always re-run both generators.

Preview locally: `cd site && python3 -m http.server 8080` then open http://localhost:8080 (use a server, not file://, so CSS masks load).

## Data layer — the main open task

On claude.ai the pages used the artifact runtime `window.claude.use('db' | 'user' | 'downloads')`.
Outside claude.ai `window.claude` does not exist; every call is wrapped in try/catch, so the site runs, but:
- `window.cccLead(info)` (index.html, also copied into car.html / me.html) cannot save leads -> customers see the
  "עוד צעד אחד" dialog with a WhatsApp fallback.
- The admin area (#adm in index.html; open with index.html#admin or footer "כניסת מנהלים") cannot load leads.
- Staff accounts (collections `accounts` / `approvals`) and the owner password live in that db too.

To go live, replace the `claude.use(...)` calls with a real backend (e.g. Firebase Auth + Firestore, or Supabase):
- `leads/<customerId>` doc: {name, phone, city, status, src, ts, history[], reqs[], loan, profile, unseen, last}.
  Each customer request is an item in `reqs[]` {rid, ts, src, car, detail, name, phone, city, status, note, unseen, loan?};
  the admin list shows every request as its own row.
- Statuses: new, work, meet, quote, uw, won, lost, noans, cold (cold = left details at the gate, no request yet).
- Only the owner and approved staff may read `leads`; a customer may write only their own doc.
- Customer accounts (auth.js) are currently browser-local (localStorage `ccc_me`, PBKDF2 password hash).
  With a backend: move them server-side and add real SMS verification for password reset (owner asked for SMS).
- Licence-plate lookup for trade-in can then use data.gov.il (Ministry of Transport open data) — blocked on claude.ai.

## Owner's rules (keep them)

- "המחיר, המלאי והפרטים העסקיים נלקחים רק מהאקסל שלי. מידע טכני בלבד מותר להשלים מהאינטרנט."
  Prices are shown exactly as in the Excel (no rounding).
- "אל תשנה, תמחק או תאחד דגמים מהאקסל בלי אישור שלי" — 7 duplicate model names exist; ask before merging.
- "אין להמציא ביקורות, נתוני מלאי, מחירים, הנחות או מבצעים שלא סיפקתי"
- "לא להמציא שום נתון. אם לא ניתן לאמת נתון בוודאות, אל תציג את השורה בכלל באתר. אסור להציג ללקוח 'ממתין לאימות', 'לא ידוע' או placeholder אחר."
- No images with watermarks, other agencies' logos, or of a different version of the car.
- The financing wizard never tells a customer they are eligible — it only collects a request for a finance rep.

## Open items

- Real car photos (owner to supply), business details for the footer (name, company no., address),
  WhatsApp number (currently 972545762802 inside wa.me links), accessibility-coordinator details in the accessibility statement.
- Design: studio theme — ink #1f1519, accent #7a2a4a, soft pink #f4e9ee, bg #efe9e8→#d9d0cf, fonts Heebo + Unbounded.
