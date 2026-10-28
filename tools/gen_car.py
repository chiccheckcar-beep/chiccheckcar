import re, json, sys
site = sys.argv[1]
html = open(f'{site}/index.html', encoding='utf-8').read()
cars = json.loads(re.search(r'const CARS\s*=\s*(\[.*?\]);', html, re.S).group(1))
cars = [{k: c.get(k,'') for k in ('maker','model','trim','extra','fuel','drive','price','cat','img')} for c in cars]
atto = [{"n":"448","u":"כ\"ס","l":"הספק מרבי"},{"n":"3.9","u":"שנ'","l":"תאוצה 0–100 קמ\"ש"},{"n":"470","u":"ק\"מ","l":"טווח חשמלי WLTP"},{"n":"17.8","u":"קוט\"ש/100 ק\"מ","l":"צריכת חשמל WLTP"}]
mg3 = [{"n":"194","u":"כ\"ס","l":"הספק מרבי"},{"n":"22.7","u":"ק\"מ/ל","l":"צריכת דלק משולבת"},{"n":"5","u":"","l":"מושבים"},{"n":"293","u":"ליטר","l":"נפח תא מטען"}]
stats = {}
for i,c in enumerate(cars):
    if c['model']=='ATTO 3 EVO' and c['trim']=='Excellence': stats[i] = atto
    if c['model']=='MG3' and c['trim']=='Luxury': stats[i] = mg3
page = r'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>ChicCheckCar</title>
<link rel="icon" href="logo.png">
<meta name="description" content="פרטי הרכב, מחיר, נתונים טכניים ותשלום חודשי משוער · ChicCheckCar">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&family=Unbounded:wght@600;700&display=swap">
<style>
:root{--bg:#ffffff;--line:#e8e1d8;--txt:#1d1b19;--mut:#6f675e;color-scheme:light}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--txt);font-family:system-ui,"Segoe UI",Arial,sans-serif;line-height:1.6}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.wrap{max-width:1100px;margin:0 auto;padding-inline:20px}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
header img{height:44px;width:auto;display:block}
.back{display:inline-flex;align-items:center;gap:8px;background:#1d1b19;color:#fff;text-decoration:none;font-size:17px;font-weight:700;padding:13px 26px;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.18);transition:transform .2s,box-shadow .2s}
.back:hover,.back:focus-visible{color:#fff;transform:translateY(-2px);box-shadow:0 12px 28px rgba(0,0,0,.25)}
.back:focus-visible{outline:2px solid #1d1b19;outline-offset:3px}
@media (max-width:600px){.back{font-size:15px;padding:11px 18px}}
.back{margin-top:18px;margin-inline-start:auto}
@media (max-width:600px){.back{margin-top:12px}}
/* ---- Car page: showroom layout ---- */
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);gap:40px;align-items:center;padding-block:28px 44px}
.stage{order:2;position:relative;margin:0;padding:24px 0 10px;background:radial-gradient(ellipse 60% 22% at 50% 88%,rgba(29,27,25,.12),transparent 70%)}
.stage img{width:100%;height:auto;display:block}
.stage figcaption{font-size:11px;color:var(--mut);text-align:center;margin-top:4px}
.info{order:1;display:flex;flex-direction:column;gap:10px}
.eyebrow{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut)}
h1{font-size:clamp(30px,4.6vw,52px);font-weight:800;margin:0;line-height:1.05;letter-spacing:-.01em;text-wrap:balance}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12px;border:1px solid var(--line);border-radius:999px;padding:3px 12px;color:var(--txt);background:#fff}
.chip.dark{background:var(--txt);color:#fff;border-color:var(--txt)}
.extraline{font-size:14px;color:var(--mut)}
.pricebox{margin-top:8px;padding:18px 20px;border:1px solid var(--line);border-radius:16px;background:#faf9f7}
.pricebox .from{font-size:13px;color:var(--mut)}
.pricebox .big{font-family:"Unbounded",system-ui,"Segoe UI",Arial,sans-serif;font-size:30px;font-weight:700;line-height:1.2;font-variant-numeric:tabular-nums}
.pricebox .mon{font-size:15px;color:var(--mut);margin-top:2px}
.pricebox .mon b{color:var(--txt);font-size:17px}
.plan-note{font-size:11.5px;color:var(--mut);margin:8px 0 0}
.btn{display:inline-block;background:#ffffff;color:var(--txt);border:1px solid var(--txt);border-radius:10px;padding:12px 22px;font-weight:700;text-decoration:none;cursor:pointer;font-size:15px;font-family:inherit;transition:background .15s,color .15s;text-align:center}
.btn:hover{background:var(--txt);color:#fff}
.btn.solid{background:var(--txt);color:#fff}
.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px}
.actions .btn.solid{grid-column:1 / -1}
.actions .cartbtn{grid-column:1 / -1;display:flex;align-items:center;justify-content:center;gap:8px}
.actions .cartbtn[aria-pressed="true"]{background:#7a2a4a;border-color:#7a2a4a;color:#fff}
.mycart{grid-column:1 / -1;text-align:center;font-size:14px;color:var(--mut);text-decoration:underline}
.mycart[hidden]{display:none}
/* stats band */
.band{background:#0d0d0d;color:#fff;border-radius:22px;padding:34px 18px;margin-bottom:36px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;text-align:center}
.band .n{font-family:"Unbounded",system-ui,"Segoe UI",Arial,sans-serif;font-size:clamp(24px,3.4vw,40px);font-weight:700;line-height:1.1;direction:ltr;white-space:nowrap;font-variant-numeric:tabular-nums}
.band .n small{font-size:.42em;font-weight:600;margin-inline-start:4px}
.band .l{font-size:11px;letter-spacing:.14em;color:#a8a29a;margin-top:8px}
.band > div + div{border-inline-start:1px solid #2a2826}
/* spec sheet */
.sheet-title{font-size:22px;margin:0 0 14px}
.sheet{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-bottom:28px}
.group{border:1px solid var(--line);border-radius:16px;padding:18px 18px 8px;background:#fff}
.group h3{font-size:12px;letter-spacing:.16em;color:var(--mut);margin:0 0 6px;font-weight:600}
.group dl{margin:0}
.group .r{display:flex;justify-content:space-between;gap:14px;padding:11px 0;border-top:1px solid #f0ebe4}
.group .r:first-child{border-top:0}
.group dt{color:var(--mut);font-size:14px;flex:0 0 auto}
.group dd{margin:0;font-weight:700;font-size:14.5px;text-align:left;min-width:0}
@media (max-width:900px){.hero{grid-template-columns:1fr;gap:10px}.stage{order:1}.info{order:2}.sheet{grid-template-columns:1fr}}
@media (max-width:600px){.band{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:26px;padding:26px 10px}.band > div:nth-child(3){border-inline-start:0}.actions{grid-template-columns:1fr}.pricebox .big{font-size:26px}}
.approx{max-width:560px;margin:-20px auto 28px;font-size:13px;color:#8a5a00;background:#fff7e6;border:1px solid #f0d9a8;border-radius:10px;padding:10px 14px;text-align:center}
#offer{border-top:1px solid var(--line);padding-block:36px 60px}
#finance{border-top:1px solid var(--line);padding-block:36px 40px}
#finance h2{text-align:center;font-size:24px;margin:0 0 6px}
#finance p.lead{text-align:center;color:var(--mut);margin:0 0 20px}
.fin{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:24px;align-items:start;max-width:900px;margin:0 auto}
.fin-in{display:flex;flex-direction:column;gap:6px;padding:22px;border:1px solid var(--line);border-radius:18px;background:#fff}
.fin-in label{font-size:14px;color:var(--mut);margin:0}
.fin-row{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-top:6px}
.fin-row output{font-weight:700;font-size:16px;font-variant-numeric:tabular-nums}
.mon .addon{font-size:12px;opacity:.7;font-weight:500}
.fin-row span{font-size:14px;opacity:.85}
.fin-in input[type=range]{width:100%;accent-color:#1d1b19;margin:4px 0 8px;height:28px;padding:0;border:0}
.fin-out{padding:26px 22px;border-radius:18px;background:#1d1b19;color:#fff;display:flex;flex-direction:column;gap:12px}
.fin-label{font-size:13px;opacity:.75}
.fin-big{font-size:38px;font-weight:800;line-height:1.1;direction:ltr;text-align:right;font-variant-numeric:tabular-nums}
.fin-dl{display:grid;grid-template-columns:1fr auto;gap:8px 16px;margin:6px 0 4px;padding-top:12px;border-top:1px solid rgba(255,255,255,.18);font-size:14px}
.fin-dl dt{opacity:.75}.fin-dl dd{margin:0;font-weight:700;direction:ltr;text-align:left;font-variant-numeric:tabular-nums}
.btn.solid-w{background:#fff;color:#1d1b19;border-color:#fff;text-align:center}
.btn.ghost-w{background:transparent;color:#fff;border-color:rgba(255,255,255,.5);text-align:center}
.btn.ghost-w:not([href]){display:none}
.fin-note{font-size:11.5px;opacity:.75;margin:4px 0 0;line-height:1.6}
@media (max-width:760px){.fin{grid-template-columns:1fr}.fin-big{font-size:32px}}
#offer h2{text-align:center;font-size:24px;margin:0 0 6px}
#offer p.lead{text-align:center;color:var(--mut);margin:0 0 20px}
form{max-width:420px;margin:0 auto;display:flex;flex-direction:column;gap:6px}
label{font-size:14px;color:var(--mut);margin-top:8px}
input{background:#fff;color:var(--txt);border:1px solid var(--line);border-radius:10px;padding:11px 14px;font-size:15px;font-family:inherit;width:100%}
form .btn{margin-top:16px;text-align:center;width:100%}
.note{font-size:13px;color:var(--mut);text-align:center}
.missing{text-align:center;padding-block:80px}
footer{border-top:1px solid var(--line);padding-block:24px;color:var(--mut);font-size:13px;text-align:center}
@media (max-width:600px){.wrap{padding-inline:16px}header .wrap{height:60px}header img{height:36px}.stat .n{font-size:30px}.price{font-size:15px}}

/* ===== Studio theme (matches the catalog page) ===== */
[hidden]{display:none !important}
:root{--bg:#efe9e8;--line:rgba(31,21,25,.1);--txt:#1f1519;--mut:#6a5a60;--acc:#7a2a4a;--acc2:#5e1f39;--card:#fbf9f8;--pink:#e8c7d4}
html,body{background:radial-gradient(120% 80% at 50% 0,#efe9e8 0,#d9d0cf 100%) fixed,#d9d0cf;font-family:"Heebo",system-ui,"Segoe UI",Arial,sans-serif;color:var(--txt)}
.back{background:var(--txt)}
.back:hover,.back:focus-visible{background:var(--acc)}
.hero{gap:44px;padding-block:24px 48px}
.stage{padding:34px 26px 18px;border-radius:30px;background:radial-gradient(90% 80% at 50% 30%,#ffffff 0,#ebe4e3 70%,#ddd4d3 100%);box-shadow:0 30px 60px -40px rgba(31,21,25,.45)}
.stage img{filter:drop-shadow(0 22px 18px rgba(31,21,25,.22))}
.eyebrow{color:var(--acc);font-weight:700;letter-spacing:.24em}
h1{font-family:"Heebo",system-ui,sans-serif;font-weight:800;letter-spacing:-.025em}
.chip{background:rgba(255,255,255,.7);border-color:var(--line);font-weight:600}
.chip.dark{background:var(--acc);border-color:var(--acc)}
.trimsw{margin-top:4px}
.trimsw-l{display:block;font-size:12px;color:var(--mut);margin-bottom:6px}
.trimsw-o{display:flex;flex-wrap:wrap;gap:8px}
.trimsw-o a{display:flex;flex-direction:column;gap:1px;min-width:96px;padding:8px 14px;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.7);color:inherit;text-decoration:none;transition:border-color .15s,background .15s}
.trimsw-o a:hover{border-color:var(--acc)}
.trimsw-o a b{font-size:13px;font-weight:700}
.trimsw-o a small{font-size:12px;color:var(--mut);font-variant-numeric:tabular-nums}
.trimsw-o a.on{background:var(--txt);border-color:var(--txt);color:#fff}
.trimsw-o a.on small{color:rgba(255,255,255,.75)}
@media (max-width:600px){.trimsw-o a{min-width:0;padding:6px 10px}.trimsw-o a b{font-size:12px}}
.pricebox{background:var(--card);border-color:var(--line);border-radius:22px;padding:20px 22px;box-shadow:0 14px 34px -26px rgba(31,21,25,.4)}
.pricebox .big{color:var(--txt);font-size:34px}
.pricebox .mon b{color:var(--acc)}
.btn{border-radius:14px;border-color:rgba(31,21,25,.18);background:rgba(255,255,255,.85);padding:13px 20px}
.btn:hover{background:var(--txt);border-color:var(--txt);color:#fff}
.btn.solid{background:var(--txt);border-color:var(--txt)}
.btn.solid:hover{background:var(--acc);border-color:var(--acc)}
.actions .cartbtn[aria-pressed="true"]{background:var(--acc);border-color:var(--acc)}
.mycart{color:var(--acc);font-weight:600}
.band{background:var(--txt);border-radius:26px;box-shadow:0 30px 60px -36px rgba(31,21,25,.6)}
.band .l{color:var(--pink);opacity:.85}
.band > div + div{border-inline-start-color:rgba(232,199,212,.18)}
.sheet-title,#finance h2,#offer h2{font-family:"Unbounded",system-ui,"Segoe UI",Arial,sans-serif;font-weight:700;letter-spacing:-.02em}
.sheet-title::before,#finance h2::before,#offer h2::before{content:"";display:block;width:36px;height:2px;background:var(--acc);margin:0 0 12px}
#finance h2::before,#offer h2::before{margin-inline:auto}
.group{background:var(--card);border-color:var(--line);border-radius:22px}
.group h3{color:var(--acc)}
.group .r{border-top-color:var(--line)}
.approx{border-radius:14px}
#offer,#finance{border-top-color:var(--line)}
.fin-in{background:var(--card);border-color:var(--line);border-radius:22px}
.fin-in input[type=range]{accent-color:var(--acc)}
.fin-out{background:var(--txt);border-radius:22px;box-shadow:0 30px 60px -36px rgba(31,21,25,.6)}
.fin-label{color:var(--pink);opacity:1}
.btn.solid-w{background:#fff;color:var(--txt);border-color:#fff}
.btn.solid-w:hover{background:var(--pink);border-color:var(--pink);color:var(--txt)}
.btn.ghost-w{border-color:rgba(232,199,212,.45)}
.btn.ghost-w:hover{background:rgba(255,255,255,.08);color:#fff}
#offer form{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:22px 22px 26px;box-shadow:0 20px 44px -34px rgba(31,21,25,.5)}
input{background:#fff;border-color:var(--line);border-radius:12px;padding:12px 14px}
input:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px rgba(122,42,74,.12)}
footer{background:#140d10;color:#d9d0cf;border-top:0;padding-block:28px;margin-top:20px}
footer a{color:#e8c7d4 !important}
@media (max-width:600px){.stage{padding:22px 12px 10px;border-radius:24px}.pricebox .big{font-size:28px}#offer form{padding:16px}}
.okbox{position:fixed;inset:0;z-index:400;display:grid;place-items:center;padding:16px}
.okbox[hidden]{display:none}
.okbox-bg{position:absolute;inset:0;background:rgba(20,12,16,.5);backdrop-filter:blur(4px);animation:meFade .2s ease}
.okbox-card{position:relative;width:min(400px,100%);background:#fff;color:#1f1519;border-radius:24px;padding:30px 24px 22px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px;box-shadow:0 30px 70px -20px rgba(0,0,0,.5);animation:okIn .35s cubic-bezier(.2,.9,.3,1.2);font-family:"Heebo",system-ui,"Segoe UI",Arial,sans-serif}
@keyframes okIn{from{transform:translateY(16px) scale(.96);opacity:0}}
@media (prefers-reduced-motion:reduce){.okbox-card,.okbox-bg{animation:none}}
.okbox-ic{width:72px;height:72px;border-radius:50%;display:grid;place-items:center;background:#e7f6ee;color:#18965a;margin-bottom:4px}
.okbox-ic.warn{background:#fff3df;color:#c77700}
.okbox h3{margin:0;font-size:26px;font-weight:800;font-family:inherit}
.okbox h3::before{display:none}
.okbox p{margin:0;font-size:15.5px;line-height:1.55;color:#6a5a60}
.okbox-wa{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;margin-top:8px;padding:14px;border-radius:14px;background:#25d366;color:#fff;font-weight:700;font-size:15.5px;text-decoration:none}
.okbox-wa.soft{background:#fff;color:#128c4a;border:1.5px solid #25d366;padding:11px}
.okbox-wa[hidden]{display:none}
.okbox-close{margin-top:4px;border:0;background:none;color:#6a5a60;font:inherit;font-size:14px;text-decoration:underline;cursor:pointer;padding:6px}
@keyframes meFade{from{opacity:0}}
</style>
</head>
<body>
<header><div class="wrap">
  <a class="back" href="index.html#catalog">← חזרה לקטלוג</a>
</div></header>

<main class="wrap" id="page"></main>
<div class="okbox" id="okBox" hidden role="dialog" aria-modal="true" aria-labelledby="okT">
  <div class="okbox-bg" data-ok-close></div>
  <div class="okbox-card">
    <div class="okbox-ic" id="okIc" aria-hidden="true"></div>
    <h3 id="okT"></h3>
    <p id="okP"></p>
    <a class="okbox-wa" id="okWa" target="_blank" rel="noopener" hidden></a>
    <button type="button" class="okbox-close" data-ok-close>סגירה</button>
  </div>
</div>

<footer><div class="wrap">ChicCheckCar · המחירים לפי המחירון שלנו ועשויים להשתנות. התמונות להמחשה בלבד.<br><a href="index.html#privacy" style="color:inherit">מדיניות פרטיות ועוגיות</a> · <a href="index.html#settings" style="color:inherit">הגדרות פרטיות</a> · <a href="index.html#accessibility" style="color:inherit">הצהרת נגישות</a></div></footer>

<script src="fb.js"></script>
<script src="terms.js"></script>
<script>
const CARS = __CARS__;
__LEAD__
// Confirmation after a request: "received" only when it really reached the leads center; otherwise ask to finish in WhatsApp.
window.cccDone = function({ok, phone, wa, title, text}){
  const box = document.getElementById('okBox'); if (!box) return;
  const ic = document.getElementById('okIc'), w = document.getElementById('okWa');
  const icOk = '<svg viewBox="0 0 24 24" width="38" height="38"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const icWa = '<svg viewBox="0 0 24 24" width="34" height="34"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>';
  ic.innerHTML = ok ? icOk : icWa; ic.classList.toggle('warn', !ok);
  document.getElementById('okT').textContent = title || (ok ? 'פנייתכם התקבלה' : 'עוד צעד אחד');
  document.getElementById('okP').textContent = text || (ok
    ? 'תודה! נציג של ChicCheckCar יחזור אליכם בהקדם' + (phone ? ' למספר ' + phone : '') + '.'
    : 'כדי שהפנייה תגיע אלינו, לחצו על הכפתור ושלחו את ההודעה בוואטסאפ. ההודעה כבר מוכנה עם הפרטים שלכם.');
  w.hidden = !wa; if (wa){ w.href = wa; w.textContent = ok ? 'רוצים מענה מהיר? שלחו גם בוואטסאפ' : 'שליחת הפנייה בוואטסאפ'; w.classList.toggle('soft', ok); }
  box.hidden = false; (ok ? box.querySelector('.okbox-close') : w).focus();
};
document.addEventListener('click', e => { if (e.target.closest('[data-ok-close]')) document.getElementById('okBox').hidden = true; if (e.target.closest('#okWa')) setTimeout(() => { document.getElementById('okT').textContent = 'פנייתכם נשלחה'; document.getElementById('okP').textContent = 'אם שלחתם את ההודעה בוואטסאפ, נציג יחזור אליכם בהקדם.'; }, 400); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { const b = document.getElementById('okBox'); if (b && !b.hidden) b.hidden = true; } });

const STATS = __STATS__;
const SPECS = __SPECS__;
const fmt = n => '₪' + Math.round(n).toLocaleString('he-IL');
const TERMS = window.CCC_TERMS;
const monthlyOf = price => TERMS.monthlyOf(price);
const fmtM = n => '₪' + Math.ceil(n).toLocaleString('he-IL');
const esc = s => String(s).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const GKEY = c => [c.maker, c.model, c.fuel, c.cat].join('|');
function trimSwitch(i){
  const k = GKEY(CARS[i]), ix = CARS.map((c, j) => j).filter(j => GKEY(CARS[j]) === k).sort((a, b) => CARS[a].price - CARS[b].price);
  if (ix.length < 2) return '';
  let L = ix.map(j => (CARS[j].trim || CARS[j].extra || '').trim());
  const sh = L.map(l => l.replace(/\s*\([^)]*\)\s*/g, ' ').trim()); if (new Set(sh).size === sh.length) L = sh;
  L = L.map((l, n) => L.indexOf(l) === n && L.lastIndexOf(l) === n ? (l || fmt(CARS[ix[n]].price)) : [l, CARS[ix[n]].extra && CARS[ix[n]].extra !== l ? CARS[ix[n]].extra : fmt(CARS[ix[n]].price)].filter(Boolean).join(' · '));
  return `<div class="trimsw"><span class="trimsw-l">רמת גימור</span><div class="trimsw-o">${ix.map((j, n) => `<a href="#car${j}" class="${j === i ? 'on' : ''}" ${j === i ? 'aria-current="true"' : ''}><b>${esc(L[n])}</b><small>${fmt(CARS[j].price)}</small></a>`).join('')}</div></div>`;
}
function show(){
  const m = /^#car(\d+)$/.exec(location.hash);
  const i = m ? +m[1] : -1;
  const c = CARS[i];
  const page = document.getElementById('page');
  if (!c) {
    document.title = 'ChicCheckCar';
    page.innerHTML = '<div class="missing"><h1>הרכב לא נמצא</h1><p><a class="btn" href="index.html#catalog">חזרה לקטלוג</a></p></div>';
    return;
  }
  const full = [c.maker, c.model, c.trim].filter(Boolean).join(' ');
  document.title = full + ' · ChicCheckCar';
  const st = STATS[i];
  const sp = SPECS[i] || {};
  const grp = (title, rows) => { const rr = rows.filter(r => r[1]); return rr.length ? `<div class="group"><h3>${title}</h3><dl>${rr.map(([k,v]) => `<div class="r"><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl></div>` : ''; };
  const ap = v => '';
  const band = [];
  const cons = sp.consumption || '';
  const rg = /טווח/.test(cons) ? /(כ-)?(\d+) ק"מ/.exec(cons) : null;
  const L = /(\d\.\d)/.exec(sp.engine || '') || /(\d\.\d)/.exec(c.extra || '');
  if (rg) band.push({n:rg[2], u:'ק״מ', l: c.fuel==='חשמלי' ? 'טווח נסיעה' : 'טווח חשמלי'});
  else if (L) band.push({n:ap(sp.engine)+L[1], u:'ל׳', l:'נפח מנוע'});
  if (sp.accel) band.push({n:sp.accel.split(' ')[0], u:'שנ׳', l:'0-100 קמ״ש'});
  const pw = /(\d+(?:–\d+)?)/.exec(sp.power || '');
  if (pw) band.push({n:ap(sp.power)+ap(sp.engine)+pw[1], u:'כ״ס', l: /מנוע חשמלי/.test(sp.power) ? 'הספק חשמלי' : 'הספק'});
  if (sp.seats) band.push({n:sp.seats, u:'', l:'מושבים'});
  page.innerHTML = `
  <section class="hero">
    <figure class="stage"><img src="${c.img || 'car-sample.png'}" alt="${esc(full)}"><figcaption>תמונה להמחשה בלבד</figcaption></figure>
    <div class="info">
      <div class="eyebrow">${esc(c.maker)}</div>
      <h1>${esc(c.model)}</h1>
      <div class="chips">${c.trim ? `<span class="chip dark">${esc(c.trim)}</span>` : ''}${c.fuel ? `<span class="chip">${esc(c.fuel)}</span>` : ''}${c.cat ? `<span class="chip">${esc(c.cat)}</span>` : ''}<span class="chip">0 ק"מ</span></div>
      ${c.extra ? `<div class="extraline">${esc(c.extra)}</div>` : ''}
      ${trimSwitch(i)}
      <div class="pricebox">
        <div class="from">החל מ-</div>
        <div class="big">${fmt(c.price)}</div>
        <div class="mon">החזר חודשי משוער <b>${fmtM(monthlyOf(c.price))}</b></div>
        <div class="mon">מקדמה <b>${fmt(TERMS.downOf(c))}</b> <span class="addon">בנוסף למחיר הרכב</span></div>
        <p class="plan-note">${TERMS.months} תשלומים · ריבית שנתית ${TERMS.rate}% · בלון ${TERMS.balloon}% ממחיר הרכב. ההחזר משוער עד לאישור הצעה פרטנית. המקדמה משולמת בנוסף למחיר הרכב. תנאי העסקה כפופים לאישור מימון ולהסכם העסקה.</p>
      </div>
      <div class="actions"><a class="btn solid" href="#offer" id="toOffer">לרכישה זריזה</a><button type="button" class="btn cartbtn" id="cartBtn" aria-pressed="false"></button><a class="mycart" id="myCart" href="index.html#me" hidden></a><a class="btn" id="waTop" target="_blank" rel="noopener">שליחה בוואטסאפ</a><a class="btn" href="#finance" id="toFin">מחשבון מימון</a></div>
    </div>
  </section>
  ${band.length ? `<div class="band">${band.map(b=>`<div><div class="n">${esc(b.n)}${b.u?`<small>${esc(b.u)}</small>`:''}</div><div class="l">${esc(b.l)}</div></div>`).join('')}</div>` : ''}
  <h2 class="sheet-title">מפרט טכני</h2>
  <div class="sheet">
    ${grp('זהות הרכב', [['חברה',c.maker],['דגם',c.model],['רמת גימור',c.trim],['פרטים נוספים',c.extra],['קילומטראז׳','0']])}
    ${grp('מנוע וביצועים', [['סוג מנוע', sp.engine || c.fuel],['הספק',sp.power],['תאוצה 0-100 קמ"ש',sp.accel],['תיבת הילוכים',sp.gearbox],['סוג הנעה', sp.drive || (c.drive ? c.drive.toUpperCase() : '')]])}
    ${grp('שימוש יומיומי', [[/טווח|קוט/.test(sp.consumption||'') ? 'טווח / צריכה' : 'צריכת דלק', sp.consumption],['מספר מושבים',sp.seats],['נפח תא מטען',sp.trunk]])}
  </div>
  ${sp.note ? `<p class="approx">${esc(sp.note)}</p>` : ''}
  <section id="finance">
    <h2>הרכב הבא שלך, בתשלום חודשי שמתאים לך</h2>
    <p class="lead">תנאי המימון לרכב הזה. ההחזר משוער עד לאישור הצעה פרטנית.</p>
    <div class="fin">
      <div class="fin-in">
        <div class="fin-row"><label for="finPrice">מחיר הרכב</label><output id="finPriceOut"></output></div>
        <input type="number" id="finPrice" min="10000" max="1000000" step="1" inputmode="numeric">
        <div class="fin-row"><span>מקדמה ראשונית (בנוסף למחיר)</span><output id="finDownOut"></output></div>
        <div class="fin-row"><span>ריבית שנתית</span><output id="finRateOut"></output></div>
        <div class="fin-row"><span>תקופת המימון</span><output id="finMonthsOut"></output></div>
        <div class="fin-row"><span>בלון בסוף התקופה</span><output id="finBalloonOut"></output></div>
      </div>
      <div class="fin-out" aria-live="polite">
        <div class="fin-label">החזר חודשי משוער</div>
        <div class="fin-big" id="finMonthly">—</div>
        <dl class="fin-dl">
          <dt>מחיר הרכב</dt><dd id="finLoan">—</dd>
          <dt>תשלום בלון בסוף</dt><dd id="finBal">—</dd>
          <dt>סך כל התשלומים</dt><dd id="finTotal">—</dd>
          <dt>סך הריבית</dt><dd id="finInterest">—</dd>
        </dl>
        <a class="btn solid-w" href="#offer" id="finCta">לקבלת הצעת מימון</a>
        <a class="btn ghost-w" id="finWa" target="_blank" rel="noopener">שליחת החישוב בוואטסאפ</a>
        <p class="fin-note" id="finMethod"></p>
        <p class="fin-note">ההחזר משוער בלבד עד לאישור הצעה פרטנית. המקדמה משולמת בנוסף למחיר הרכב. תנאי העסקה כפופים לאישור מימון ולהסכם העסקה.</p>
      </div>
    </div>
  </section>
  <section id="offer">
    <h2>מצאתם רכב שמעניין אתכם?</h2>
    <p class="lead">השאירו שם וטלפון, ונחזור אליכם עם כל המידע על הרכב.</p>
    <form id="leadForm">
      <label for="fName">שם מלא</label><input id="fName" required autocomplete="name">
      <label for="fPhone">טלפון</label><input id="fPhone" type="tel" required autocomplete="tel">
      <button class="btn solid" type="submit">שליחה</button>
      <a id="waLink" class="btn" target="_blank" rel="noopener" hidden>שליחת הפרטים בוואטסאפ ←</a>
    </form>
  </section>`;
  document.getElementById('toFin').addEventListener('click', e => { e.preventDefault(); document.getElementById('finance').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); });
  const openLoan = amt => { if (!window.cccLoan) return false; const im = document.querySelector('.stage img'); window.cccLoan.open({car: full, price: c.price, img: im ? im.src : ''}); window.cccLead({src:'loan', car: full, detail: 'פתח בדיקת זכאות למימון על ' + carTxt}); return true; };
  document.getElementById('toOffer').addEventListener('click', e => { e.preventDefault(); if (openLoan()) return; document.getElementById('offer').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); document.getElementById('fName').focus({preventScroll:true}); });
  const carTxt = `${full} (החל מ-${fmt(c.price)})`;
  document.getElementById('waTop').href = 'https://wa.me/972545762802?text=' + encodeURIComponent(`שלום, אני מתעניין/ת ב-${carTxt}. אשמח לקבל הצעה.`);
  { const key = [c.maker, c.model, c.trim, c.price].join('|'), b = document.getElementById('cartBtn'), my = document.getElementById('myCart');
    const rd = () => { try { return JSON.parse(localStorage.getItem('ccc_cart') || '[]'); } catch(_) { return []; } };
    const wr = v => { try { localStorage.setItem('ccc_cart', JSON.stringify(v)); } catch(_) {} };
    const ic = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="9.5" cy="19.5" r="1.5" fill="currentColor"/><circle cx="17" cy="19.5" r="1.5" fill="currentColor"/><path d="M2.5 3.5h2.2l2.4 11.1a1.5 1.5 0 0 0 1.5 1.2h8.7a1.5 1.5 0 0 0 1.5-1.1L21 7.5H5.6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    const upd = () => { const cart = rd().filter(k => CARS.some(x => [x.maker, x.model, x.trim, x.price].join('|') === k)), on = cart.includes(key);
      b.innerHTML = ic + (on ? 'בסל ✓' : 'הוספה לסל'); b.setAttribute('aria-pressed', String(on));
      my.hidden = !cart.length; my.textContent = 'לסל שלי (' + cart.length + ') ←'; };
    b.onclick = () => { const cart = rd(), at = cart.indexOf(key); if (at < 0 && window.cccAuth && !(window.cccAuth.hasAccount() && window.cccAuth.unlocked())){ window.cccAuth.require('כדי לשמור את ' + full + ' בסל, השאירו פרטים פעם אחת.', () => b.onclick()); return; } if (at >= 0) cart.splice(at, 1); else { cart.push(key); window.cccLead({src:'cart', car: full, detail: 'הוסיף לסל מעמוד הרכב: ' + carTxt}); } wr(cart); upd(); };
    upd(); }
  document.getElementById('waTop').onclick = () => window.cccLead({src:'wa', car: full, detail: 'פנה בוואטסאפ מעמוד הרכב על ' + carTxt});
  document.getElementById('finWa').onclick = e => { let t = ''; try { t = decodeURIComponent(e.currentTarget.href.split('text=')[1] || ''); } catch(_) {} window.cccLead({src:'finance', car: full, detail: t.replace(/^שלום, /, '') || 'שלח חישוב מימון על ' + carTxt}); };
  document.getElementById('leadForm').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = e.target.querySelector('[type=submit]'); if (btn.disabled) return; btn.disabled = true;   // no double send
    const okP = window.cccLead({src:'car', req: true, name: document.getElementById('fName').value.trim(), phone: document.getElementById('fPhone').value.trim(), car: full, detail: 'השאיר פרטים בעמוד הרכב על ' + carTxt});
    const msg = `שלום, אני ${document.getElementById('fName').value.trim()}. טלפון: ${document.getElementById('fPhone').value.trim()}. רכב שמעניין אותי: ${carTxt}.`;
    const a = document.getElementById('waLink');
    a.href = 'https://wa.me/972545762802?text=' + encodeURIComponent(msg);
    const ok = await okP; a.hidden = ok; btn.disabled = false;
    window.cccDone({ok, phone: document.getElementById('fPhone').value.trim(), wa: a.href});
  });
  // finance calculator
  const nis = n => '₪' + Math.round(n).toLocaleString('he-IL');
  const el = id => document.getElementById(id);
  el('finPrice').value = c.price;
  el('finMethod').textContent = 'שיטת החישוב: ' + TERMS.method;
  function calc(){
    const price = Math.max(0, +el('finPrice').value || 0);
    const down = TERMS.downOf(Object.assign({}, c, {price})), q = TERMS.quote(price);
    el('finPriceOut').textContent = nis(price);
    el('finDownOut').textContent = nis(down);
    el('finMonthsOut').textContent = q.months + ' חודשים';
    el('finRateOut').textContent = q.rate + '%';
    el('finBalloonOut').textContent = TERMS.balloon + '% · ' + nis(q.balloon);
    el('finMonthly').textContent = price > 0 ? nis(Math.ceil(q.monthly)) : '—';
    el('finLoan').textContent = nis(price); el('finBal').textContent = nis(q.balloon);
    el('finTotal').textContent = nis(q.total); el('finInterest').textContent = nis(q.interest);
    el('finWa').href = 'https://wa.me/972545762802?text=' + encodeURIComponent(`שלום, אשמח להצעת מימון ל-${full}. מחיר הרכב: ${nis(price)}, מקדמה (בנוסף למחיר): ${nis(down)}, ${q.months} תשלומים, ריבית שנתית ${q.rate}%, בלון ${TERMS.balloon}% (${nis(q.balloon)}). החזר חודשי משוער: ${nis(Math.ceil(q.monthly))}.`);
  }
  el('finPrice').addEventListener('input', calc);
  el('finCta').addEventListener('click', e => { e.preventDefault(); if (openLoan()) return; el('offer').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); el('fName').focus({preventScroll:true}); });
  calc();
  window.scrollTo(0,0);
}
window.addEventListener('hashchange', () => { if (/^#car\d+$/.test(location.hash)) show(); });
show();
</script>
<script src="auth.js"></script>
<script src="loan.js"></script>
</body>
</html>
'''
import os
spec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'specs', 'specs.json'), encoding='utf-8'))
# Public pages never show where the data came from (owner, 2026-10-25): no source links, no "manufacturer data" labels,
# no notes about sources. specs.json keeps the sources for internal use only.
ESTIMATE_NOTE = 'חלק מהנתונים הטכניים בעמוד הזה משוערים ועשויים להשתנות בין גרסאות. לפרטים מדויקים פנו לנציג.'
def clean(v):
    v = re.sub(r'\s*\((?:נתוני יצרן|ממוצע יצרן|נתון יצרן)\)', '', str(v))
    v = re.sub(r'\(נתון יצרן ל-([^)]*)\)', r'(\1)', v)
    v = re.sub(r'\s*(?:לפי|על פי) (?:היצרן|היבואן|נתוני היצרן|נתוני היבואן)', '', v)
    return v.strip()
SPECS = {}
for g in spec['groups']:
    for r in g['rows']:
        SPECS[str(r)] = {k: clean(g[k]) for k in ('drive','engine','power','accel','gearbox','consumption','seats','trunk') if k in g}
        if 'הערכה' in str(g.get('note', '')): SPECS[str(r)]['note'] = ESTIMATE_NOTE
lead_js = html[html.index('window.cccLead = async function(info){'):html.index('\n};', html.index('window.cccLead = async function(info){'))+3]
page = page.replace('__LEAD__', lead_js)
page = page.replace('__SPECS__', json.dumps(SPECS, ensure_ascii=False))
page = page.replace('__CARS__', json.dumps(cars, ensure_ascii=False)).replace('__STATS__', json.dumps({str(k):v for k,v in stats.items()}, ensure_ascii=False))
open(f'{site}/car.html','w',encoding='utf-8').write(page)
SPECS_LITE = {k: {f: v[f] for f in ('drive','engine','power','accel','gearbox','consumption','seats','trunk') if f in v} for k, v in SPECS.items()}
open(f'{site}/specs.js','w',encoding='utf-8').write('/* GENERATED by tools/gen_car.py (keyed by index in CARS). Do not hand-edit. */\nwindow.CCC_SPECS = ' + json.dumps(SPECS_LITE, ensure_ascii=False) + ';\n')
print(len(cars), sorted(stats))
