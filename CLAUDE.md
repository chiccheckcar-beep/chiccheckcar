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
  gen_legal.py   python3 tools/gen_legal.py site -> rebuilds privacy.html, privacy-settings.html, terms.html, accessibility.html
                 from the legal windows in index.html (the texts live there). Re-run after editing any legal text.
  specs/         Technical specs per model group (sources listed inside).
```

```
site/audit.html  "ChicCheckCar System Audit" (2026-10-25): internal health dashboard (noindex). Lives in the managers area: the leads center
                 header button "בדיקת מערכת" opens it full-screen inside the admin (audit.html?embed=1). audit.html shows a lock screen to
                 anyone who is not the owner or an approved staff account (approvals/<uid>.status == approved).
                 Reads the deployed files (CARS from index.html, specs.js, terms.js), runs the customer flows inside hidden iframes of the
                 real pages (cccLead is stubbed there: no test lead is ever sent), and reads Firestore leads with the team sign-in.
                 Lead merge = copy reqs into the kept doc (fromDoc) + mergedInto on the other doc / req; nothing is deleted; reversible.
                 The leads center (index.html listen()) skips docs/reqs that have mergedInto. History is per browser (localStorage).
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

Customer accounts (2026-10-25): Firebase Auth email/password (auth.js + fb.js customerRegister). Registering links the visitor's
anonymous session, so the uid and leads/<uid> stay the same; signing in on another device opens the same doc. Password reset =
Firebase reset e-mail. The browser keeps only name/phone/city/email/username (ccc_me); ID number + birth date live only in
leads/<uid>.profile. Old browser-only accounts (PBKDF2 hash in ccc_me) move to Firebase on their next sign-in with the same password.
Personal area (me.html) lists requests from the server (leads/<uid>.reqs; local-only ones are flagged "not saved") with the deal
(request.deal = price, down, monthly, months, rate, balloon, saved by cccLead) and the purchase-process timeline.
Purchase process: 12 stages in terms.js (CCC_STAGES / CCC_STAGE_LABEL). The team sets the stage per request in the leads-center
drawer ("שלב בתהליך הרכישה") -> progress/<customerUid> {reqs: {<rid>: {stage, result, ts, by, log[]}}}; customers can only read it.
No stage yet = stage 2 ("waiting for review").
firestore.rules (2026-10-25) adds `progress` and stops customers from setting team-only fields (status other than new/cold,
merge marks, test flag). THE OWNER MUST PUBLISH IT in Firebase console; until then stages cannot be saved and the audit flags it.
Audit "אזור אישי" tab: metrics + checks + a full end-to-end test with a temporary test customer (separate Firebase app, doc
flagged test:true and hidden from the leads center), deleted at the end.

Still open:
- SMS verification for password reset (owner asked for SMS; needs the Firebase Blaze plan). Reset is by e-mail today.
- Licence-plate lookup (loan.js step 4, `plateLookup`) calls data.gov.il resource 053cea08-09bc-40ec-8f7a-156f0677aff3
  directly from the browser and fills make/model + first-registration year. Not yet verified against the live API from the live site.

## Owner's rules (keep them)

- "המחיר, המלאי והפרטים העסקיים נלקחים רק מהאקסל שלי. מידע טכני בלבד מותר להשלים מהאינטרנט."
  Prices: update 2026-10-25 (owner): every price is rounded UP to the next 500, so it ends in 000 or 500
  (e.g. 145,960 -> 146,000; 172,294 -> 172,500).
  New prices the owner sends get the same rounding. Logged in docs/price-report-icar-2026.md.
  Update 2026-10-20 (owner request): prices for model-year 2026 cars were replaced with the verified importer list price on iCar,
  only where model, trim, engine and drive match exactly; others keep the Excel price. See docs/price-report-icar-2026.md.
- "אל תשנה, תמחק או תאחד דגמים מהאקסל בלי אישור שלי". 2026-10-20 the owner approved removing exact duplicates
  (same car and same price); 6 were removed, keeping the first copy. Near-duplicates with different prices still need the owner's choice.
- "אל תשנה עיצוב בחיים" (2026-10-20): never change the site's design, layout, card order/sorting, colours, fonts or animations.
  Data changes (prices, cars, photos) only.
- "אין להמציא ביקורות, נתוני מלאי, מחירים, הנחות או מבצעים שלא סיפקתי"
- "לא להמציא שום נתון. אם לא ניתן לאמת נתון בוודאות, אל תציג את השורה בכלל באתר. אסור להציג ללקוח 'ממתין לאימות', 'לא ידוע' או placeholder אחר."
- No images with watermarks, other agencies' logos, or of a different version of the car.
- (2026-10-25) Public pages never show where data came from: no source links, no "מקורות", no "לפי iCar / נתוני יצרן" labels.
  tools/specs/specs.json keeps sources + notes for internal use only; gen_car.py strips them (clean(), estimate notes become a
  neutral "estimated" line). The only credit on the site is the CC BY-SA line for the MG HS / MG4 photos, at the end of the
  privacy policy (licence requirement, owner's choice).

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

## Service terms (owner, 2026-10-25)

- The owner's service agreement (company name ChicCheckCar; contact chiccheckcar@gmail.com, 054-576-2802 — owner 2026-10-25) has its own page site/terms.html (GENERATED from the `#legal-service` window by gen_legal.py; index.html#service redirects there;
  footer + side menu links). Since 2026-10-25 every legal link opens its own page instead of a pop-up window and the original is downloadable at site/service-agreement.pdf. Text kept as the owner wrote it; site/service-agreement.pdf is the owner's updated PDF (2026-10-25, with logo).

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
  WhatsApp number 972545762802 (confirmed by the owner 2026-10-25), accessibility-coordinator details in the accessibility statement.
- Design: studio theme — ink #1f1519, accent #7a2a4a, soft pink #f4e9ee, bg #efe9e8→#d9d0cf, fonts Heebo + Unbounded.
