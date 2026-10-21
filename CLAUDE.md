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
WARNING: card figures (VERIFIED_HP / VERIFIED_RANGE / VERIFIED_0100 / VERIFIED_L in index.html) and specs.json "rows" are keyed by the
car's INDEX in CARS. Append new cars at the end. If you ever remove or reorder cars, remap those keys (see commit "Fix card figures
after duplicate removal").

Preview locally: `cd site && python3 -m http.server 8080` then open http://localhost:8080 (use a server, not file://, so CSS masks load).

## Data layer — Firebase

`site/fb.js` (loaded first on every page, also by both generators) provides the old claude.ai runtime calls
`window.claude.use('db' | 'user' | 'downloads')` on top of Firebase (project `chiccheckcar-8003f`, compat SDK from gstatic):
- `db` is Firestore. `user.id()` is the Firebase Auth uid; visitors are signed in anonymously on their first request.
- `user.isOwner()` / `cccFb.isOwnerUser()` = signed in with the owner email (ankermeir2005@gmail.com, set in fb.js and firestore.rules).
- Admin area (index.html#admin): owner and staff sign in with Firebase email/password (`cccFb.signIn/signUp/signOut`).
  Staff create an account -> `accounts/<uid>`; the owner approves -> `approvals/<uid>` {status:'approved'}.
- Access is enforced by `firestore.rules` (repo root). After changing it, paste it in Firebase console -> Firestore -> Rules -> Publish.
- Firebase console needs: Authentication with Email/Password + Anonymous enabled, the owner user added, Firestore created.

Data shapes:
- `leads/<customerUid>` doc: {name, phone, city, status, src, ts, history[], reqs[], loan, profile, unseen, last}.
  Each customer request is an item in `reqs[]` {rid, ts, src, car, detail, name, phone, city, status, note, unseen, loan?};
  the admin list shows every request as its own row.
- Statuses: new, work, meet, quote, uw, won, lost, noans, cold (cold = left details at the gate, no request yet).

Still open:
- Customer accounts (auth.js) are browser-local (localStorage `ccc_me`, PBKDF2 password hash). Move them to Firebase Auth
  and add real SMS verification for password reset (owner asked for SMS).
- Licence-plate lookup (loan.js step 4, `plateLookup`) calls data.gov.il resource 053cea08-09bc-40ec-8f7a-156f0677aff3
  directly from the browser and fills make/model + first-registration year. Not yet verified against the live API from the live site.

## Owner's rules (keep them)

- "המחיר, המלאי והפרטים העסקיים נלקחים רק מהאקסל שלי. מידע טכני בלבד מותר להשלים מהאינטרנט."
  Prices are shown exactly as in the Excel (no rounding).
  Update 2026-10-20 (owner request): prices for model-year 2026 cars were replaced with the verified importer list price on iCar,
  only where model, trim, engine and drive match exactly; others keep the Excel price. See docs/price-report-icar-2026.md.
- "אל תשנה, תמחק או תאחד דגמים מהאקסל בלי אישור שלי". 2026-10-20 the owner approved removing exact duplicates
  (same car and same price); 6 were removed, keeping the first copy. Near-duplicates with different prices still need the owner's choice.
- "אל תשנה עיצוב בחיים" (2026-10-20): never change the site's design, layout, card order/sorting, colours, fonts or animations.
  Data changes (prices, cars, photos) only.
- "אין להמציא ביקורות, נתוני מלאי, מחירים, הנחות או מבצעים שלא סיפקתי"
- "לא להמציא שום נתון. אם לא ניתן לאמת נתון בוודאות, אל תציג את השורה בכלל באתר. אסור להציג ללקוח 'ממתין לאימות', 'לא ידוע' או placeholder אחר."
- No images with watermarks, other agencies' logos, or of a different version of the car.

## Deal terms (owner, 2026-10-21)

- `site/terms.js` is the single source of deal terms for every page (cards, car page, calculator, personal area). Change numbers there only.
- Finance: 5.9% annual nominal, 60 payments, 50% balloon, full car price financed (Spitzer). The monthly payment is always labelled "משוער".
  Never show 3.9% anywhere.
- Down payment is paid ON TOP of the car price. Tiers: <=200k 9,900; <=300k 14,900 (EV 16,900); <=400k 16,900 (EV 19,000);
  >400k, commercial (cat 'מסחרי') and Toyota Land Cruiser 24,900. Only fuel 'חשמלי' counts as EV (hybrids/PHEV = non-EV).
- Required disclaimer: "המקדמה משולמת בנוסף למחיר הרכב. תנאי העסקה כפופים לאישור מימון ולהסכם העסקה."
- End-of-term options: never promise a swap without extra payment.

## Catalog: one card per model (2026-10-22)

- index.html groups CARS at render time: same maker + model + fuel + cat = one model card (`GKEY`, `GROUPS`). CARS itself is unchanged
  and every trim keeps its own index, car.html#car<N> link, cart key and lead text with the exact trim.
- Card: trim pills (cheapest selected by default), price/figures/monthly of the selected trim, "השווה רמות גימור" (comparison modal:
  table on desktop, swipe cards on mobile; rows with no data are hidden; differing rows highlighted) and "בחר גרסה והמשך" (-> car page).
- Comparison specs come from `site/specs.js` — GENERATED by tools/gen_car.py from specs.json, loaded only when a comparison opens.
- car.html shows a "רמת גימור" switcher linking the sibling trims.
- `RECOMMEND` (index -> reason) in index.html drives the "מומלץ" tag. Empty on purpose: no equipment/value data exists yet. Never invent one.

## Owner-supplied material

- Owner instruction (2026-10-20): "כול מה שאני שולח לך תוסיף לטבלה" — every price, car or photo the owner sends is added to the
  catalog (CARS in index.html) and logged in docs/price-report-icar-2026.md (prices) with the date and "נמסר ע"י הבעלים" as source.
  Re-run both generators after any CARS change.

## Car photos (owner approved this style)

- One photo per model (same maker + model share it), saved as `site/cars/<maker>-<model>.webp` and set in the car's `img` field in CARS.
- Style (owner, 2026-10-20): WHITE car, FRONT 3/4 view (front-left corner toward the viewer), transparent background, trimmed,
  1000px wide, WebP ~82, saved as `site/cars/<slug>-34.webp`. Must look like `site/cars/toyota-yaris-34.webp`.
  Good sources: toyota-europe image server (`day-exterior-33_040.png`), hyundai.com/contents/vr360/<code>/exterior/<colour>/001.png,
  kia.com configurator frames, byd.com/eu gallery "Front View" white, mg.co.uk configurator front/arctic-white, omodajaecoo.com.au. Re-run both generators after changing CARS.
- Same model and generation as sold in Israel is enough; the trim may differ (owner approved). The page already says "תמונה להמחשה בלבד".
- Preferred source: the Israeli importer's own configurator images (e.g. toyota.co.il -> img-optimize.toyota-europe.com
  `visual-for-model-selector` PNG, change width/height in the URL for a larger size).
- Sites that block automated access (seen: jaecoo.co.il, omoda.co.il, skoda.co.il, citroen.co.il): ask the owner to send the photos.
- The financing wizard never tells a customer they are eligible — it only collects a request for a finance rep.

## Open items

- Real car photos (owner to supply), business details for the footer (name, company no., address),
  WhatsApp number (currently 972545762802 inside wa.me links), accessibility-coordinator details in the accessibility statement.
- Design: studio theme — ink #1f1519, accent #7a2a4a, soft pink #f4e9ee, bg #efe9e8→#d9d0cf, fonts Heebo + Unbounded.
