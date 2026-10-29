import re, json, sys
site = sys.argv[1]
idx = open(f'{site}/index.html', encoding='utf-8').read()
cars = json.loads(re.search(r'const CARS\s*=\s*(\[.*?\]);', idx, re.S).group(1))
def between(a, b, inclusive_end=True):
    i = idx.index(a); j = idx.index(b, i)
    return idx[i:j + (len(b) if inclusive_end else 0)]
lead_js = between('window.cccLead = async function(info){', '\n};')
done_js = between('// Confirmation after a request', "if (b && !b.hidden) b.hidden = true; } });")
ok_html = between('<div class="okbox" id="okBox"', '</div>\n</div>')
ok_css = between('.okbox{position:fixed', '.okbox-close{', False) + between('.okbox-close{', '}')
logo_m = re.search(r':root\{--logo-m:url\("([^"]+)"\)\}', idx).group(1)

page = r'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>האזור האישי · ChicCheckCar</title>
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&family=Unbounded:wght@600;700&display=swap">
<style>
:root{--ink:#1f1519;--mut:#6a5a60;--acc:#7a2a4a;--pink:#f4e9ee;--card:#fbf9f8;--line:rgba(31,21,25,.1);color-scheme:light;--logo-m:url("__LOGO__")}
*{box-sizing:border-box}
[hidden]{display:none !important}
html,body{margin:0;min-height:100%}
body{display:flex;flex-direction:column;min-height:100vh;background:radial-gradient(120% 80% at 50% 0,#efe9e8 0,#d9d0cf 100%) fixed,#d9d0cf;color:var(--ink);font:15px/1.55 "Heebo",system-ui,"Segoe UI",Arial,sans-serif}
a{color:inherit}
.wrap{max-width:820px;margin:0 auto;padding-inline:20px}
.top{position:sticky;top:0;z-index:20;background:rgba(251,249,248,.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding-top:env(safe-area-inset-top,0px)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.logo{display:block;height:46px;aspect-ratio:600/316;background:var(--acc);-webkit-mask:var(--logo-m) center/contain no-repeat;mask:var(--logo-m) center/contain no-repeat}
.back{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;font-size:14.5px;padding:10px 18px;border-radius:999px}
.back:hover{background:var(--acc)}
.hero{display:flex;align-items:center;gap:16px;padding:30px 0 18px}
.av{width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--acc),#b24a76);color:#fff;display:grid;place-items:center;font-size:22px;font-weight:800;flex:none;box-shadow:0 10px 24px -12px var(--acc)}
.hero small{color:var(--acc);font-weight:600;font-size:14px}
.hero h1{margin:0;font-size:clamp(26px,5vw,34px);font-weight:800;letter-spacing:-.02em;line-height:1.15}
.tabs{display:flex;gap:6px;background:rgba(255,255,255,.6);border:1px solid var(--line);border-radius:16px;padding:5px;margin-bottom:18px}
.tabs a{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;padding:11px 8px;border-radius:12px;text-decoration:none;font-weight:700;font-size:14.5px;color:var(--mut)}
.tabs a[aria-current="page"]{background:var(--ink);color:#fff}
.tabs b{font-size:12px;background:var(--acc);color:#fff;border-radius:999px;padding:0 7px;min-width:20px;text-align:center}
.tabs b:empty{display:none}
.tabs a{white-space:nowrap}
@media (max-width:420px){.tabs a{font-size:13px;padding:10px 4px;gap:4px}}
.panel{padding-bottom:60px}
.card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 18px 40px -32px rgba(31,21,25,.5)}
.empty{text-align:center;padding:46px 16px;color:var(--mut);display:flex;flex-direction:column;align-items:center;gap:8px}
.empty b{color:var(--ink);font-size:18px}
.empty svg{color:var(--acc);opacity:.55}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:14px;padding:14px 20px;background:var(--ink);color:#fff;font:inherit;font-weight:700;font-size:15.5px;cursor:pointer;text-decoration:none}
.btn:hover{background:var(--acc)}
.btn.block{width:100%}
.items{display:grid;gap:12px}
.item{display:grid;grid-template-columns:150px 1fr auto;gap:16px;align-items:center;background:var(--pink);border-radius:20px;padding:12px}
.thumb{aspect-ratio:16/10;border-radius:14px;background:radial-gradient(90% 80% at 50% 30%,#fff 0,#ebe4e3 75%);display:grid;place-items:center;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:contain}
.iname{display:flex;flex-direction:column;gap:1px;text-decoration:none;min-width:0}
.iname small{color:var(--acc);font-weight:700;font-size:12px;letter-spacing:.06em}
.iname b{font-size:17px}
.iname .tr{color:var(--mut);font-size:13px}
.iname .pr{font-weight:800;font-size:16px;margin-top:4px}
.iname .mo{color:var(--mut);font-size:12.5px}
.rm{width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--mut);font-size:20px;cursor:pointer}
.rm:hover{color:#b23838;border-color:#b23838}
.sum{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:16px;flex-wrap:wrap}
.sum span{color:var(--mut);font-size:14px}
@media (max-width:560px){.item{grid-template-columns:96px 1fr auto;gap:10px}.iname b{font-size:15px}.sum .btn{width:100%}}
.req{background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.reqs{display:grid;gap:12px}
.req-top{display:flex;justify-content:space-between;align-items:center;gap:10px}
.req-top small{color:var(--mut)}
.st{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;padding:3px 10px;border-radius:999px;background:color-mix(in srgb,var(--c,#7a2a4a) 13%,transparent);color:var(--c,#7a2a4a)}
.st::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.req ul{margin:0;padding:0 18px 0 0}
.req .x{color:var(--mut);font-size:13px}
.req-no{font-family:"Unbounded",system-ui,sans-serif;font-size:11.5px;letter-spacing:.06em;color:var(--mut);direction:ltr;unicode-bidi:isolate}
.req-warn{background:#fff6e6;color:#7a4a00;border-radius:12px;padding:8px 12px;font-size:13px}
.req dl.deal{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:6px 0 2px;font-size:13.5px}
.req dl.deal dt{color:var(--mut)}
.req dl.deal dd{margin:0;font-weight:600}
.req .deal-n{font-size:12px;color:var(--mut)}
.tl{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:0}
.tl li{position:relative;padding:0 26px 12px 0;font-size:13.5px;color:var(--mut)}
.tl li::before{content:"";position:absolute;right:5px;top:5px;width:10px;height:10px;border-radius:50%;border:2px solid #d8cdd2;background:#fff}
.tl li::after{content:"";position:absolute;right:10px;top:17px;bottom:-2px;width:2px;background:#e9e1e4}
.tl li:last-child::after{display:none}
.tl li.done{color:#1f1519}
.tl li.done::before{background:#7a2a4a;border-color:#7a2a4a}
.tl li.done::after{background:#7a2a4a}
.tl li.cur{color:#7a2a4a;font-weight:800}
.tl li.cur::before{background:#fff;border-color:#7a2a4a;box-shadow:0 0 0 4px rgba(122,42,74,.15)}
.tl li.stop{color:#b3261e;font-weight:800}
.tl li.stop::before{background:#b3261e;border-color:#b3261e}
.tl li small{display:block;font-weight:400;color:var(--mut);font-size:11.5px}
.tl-more{border:0;background:none;color:#7a2a4a;font:inherit;font-size:13px;text-decoration:underline;cursor:pointer;padding:0;align-self:flex-start}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
.stats a{display:flex;flex-direction:column;padding:14px 16px;border-radius:18px;background:#fff;border:1px solid var(--line);text-decoration:none}
.stats a:hover{border-color:var(--acc)}
.stats b{font-size:26px;font-weight:800;color:var(--acc);line-height:1.1}
.stats span{color:var(--mut);font-size:13px}
form{display:flex;flex-direction:column;gap:12px}
form h2{margin:0;font-size:13px;font-weight:800;color:var(--acc);letter-spacing:.04em}
label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:700}
input{font:inherit;font-size:16px;padding:12px 14px;border:1.5px solid rgba(31,21,25,.14);border-radius:14px;background:#fff;color:var(--ink);width:100%}
input:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px rgba(122,42,74,.14)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:480px){.two{grid-template-columns:1fr}}
.msg{margin:0;padding:10px 12px;border-radius:10px;background:#e7f6ee;color:#156b43;font-size:14px}
.msg.err{background:#fdecec;color:#a32a2a}
.priv{margin-top:14px;padding:14px 16px;border-radius:16px;background:var(--pink);font-size:13px;color:var(--mut);display:flex;flex-direction:column;gap:6px;align-items:flex-start}
.fe{margin:-6px 0 0;color:#b3261e;font-size:12.5px;font-weight:600}
.fe:empty{display:none}
input.bad{border-color:#c0392b !important}
.h2b{margin-top:8px !important;padding-top:12px;border-top:1px solid var(--line)}
.link2{border:0;background:none;padding:0;font:inherit;font-size:13px;color:var(--acc);text-decoration:underline;cursor:pointer;align-self:flex-start}
.link{border:0;background:none;padding:0;font:inherit;font-size:13px;color:#b23838;text-decoration:underline;cursor:pointer}
main{flex:1;width:100%}
body.locked main{filter:blur(6px);pointer-events:none;user-select:none}
footer{background:#140d10;color:#d9d0cf;text-align:center;font-size:13px;padding:24px 16px calc(24px + env(safe-area-inset-bottom,0px))}
footer a{color:#e8c7d4}
__OKCSS__
@keyframes meFade{from{opacity:0}}
</style>
</head>
<body>
<header class="top"><div class="wrap"><a href="index.html" aria-label="ChicCheckCar, לעמוד הראשי"><span class="logo" role="img" aria-label="ChicCheckCar"></span></a><a class="back" href="index.html#catalog">לקטלוג הרכבים ←</a></div></header>
<main class="wrap">
  <section class="hero"><span class="av" id="av" aria-hidden="true">?</span><div><small id="hi">שלום</small><h1>האזור האישי</h1></div></section>
  <nav class="tabs" aria-label="האזור האישי"><a href="#cart" data-tab="cart">הסל שלי <b id="nCart"></b></a><a href="#req" data-tab="req">הפניות שלי <b id="nReq"></b></a><a href="#info" data-tab="info">הפרטים שלי</a></nav>
  <section class="panel" id="pCart" hidden></section>
  <section class="panel" id="pReq" hidden></section>
  <section class="panel" id="pInfo" hidden>
    <div class="stats"><a href="#cart"><b id="sCart">0</b><span>רכבים בסל</span></a><a href="#req"><b id="sReq">0</b><span>פניות</span></a></div>
    <form class="card" id="fInfo" novalidate>
      <h2>פרטים אישיים</h2>
      <label>שם מלא<input id="iName" autocomplete="name" placeholder="שם פרטי ושם משפחה"></label><p class="fe" data-f="name"></p>
      <div class="two"><div><label>תעודת זהות<input id="iId" inputmode="numeric" dir="ltr" maxlength="9" autocomplete="off"></label><p class="fe" data-f="idn"></p></div><div><label>תאריך לידה<input id="iDob" type="date" dir="ltr" autocomplete="bday"></label><p class="fe" data-f="dob"></p></div></div>
      <div class="two"><div><label>טלפון נייד<input id="iPhone" type="tel" dir="ltr" autocomplete="tel" placeholder="050-0000000"></label><p class="fe" data-f="phone"></p></div><div><label>אימייל<input id="iMail" type="email" dir="ltr" autocomplete="email" placeholder="name@gmail.com"></label><p class="fe" data-f="email"></p></div></div>
      <label>עיר <input id="iCity" autocomplete="address-level2" placeholder="לא חובה"></label>
      <h2 class="h2b">פרטי כניסה</h2>
      <label>שם משתמש<input id="iUser" dir="ltr" autocomplete="username" autocapitalize="off" spellcheck="false"></label><p class="fe" data-f="username"></p>
      <div class="two"><div><label>סיסמה חדשה <input id="iPw" type="password" dir="ltr" autocomplete="new-password" placeholder="רק אם רוצים להחליף"></label><p class="fe" data-f="pw"></p></div><div><label>אימות סיסמה<input id="iPw2" type="password" dir="ltr" autocomplete="new-password"></label><p class="fe" data-f="pw2"></p></div></div>
      <button type="button" class="link2" id="iReset">שכחתי סיסמה? איפוס עם תעודת זהות ותאריך לידה</button>
      <p class="msg" id="iMsg" role="status" hidden></p>
      <button type="submit" class="btn block">שמירת הפרטים</button>
    </form>
    <div class="priv"><span>🔒 החשבון שלך שמור בשרת מאובטח ואפשר להיכנס אליו מכל מכשיר. הסיסמה מוצפנת, ואנחנו לא רואים אותה.</span><button type="button" class="link2" id="iOut">יציאה מהחשבון</button><button type="button" class="link" id="iClear">מחיקת החשבון, הסל והפניות מהדפדפן</button></div>
  </section>
</main>
<footer>ChicCheckCar · <a href="index.html#privacy">מדיניות פרטיות</a> · <a href="index.html#settings">הגדרות פרטיות</a> · <a href="index.html#accessibility">הצהרת נגישות</a></footer>
__OKHTML__
<script src="fb.js"></script>
<script src="terms.js"></script>
<script>
const CARS = __CARS__;
__LEAD__
__DONE__
(function(){
  const $ = id => document.getElementById(id);
  const fmt = n => '₪' + Math.round(n).toLocaleString('he-IL');
  const monthly = p => window.CCC_TERMS.monthlyOf(p);
  const fullName = c => [c.maker, c.model, c.trim].filter(Boolean).join(' ');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const LS = { get(k, d){ try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch(e){ return d; } }, set(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }, del(k){ try { localStorage.removeItem(k); } catch(e){} } };
  const keyOf = c => [c.maker, c.model, c.trim, c.price].join('|');
  const idxOf = k => CARS.findIndex(c => keyOf(c) === k);
  const me = () => { const d = LS.get('ccc_me', {}); let n = d.name, p = d.phone; try { n = n || sessionStorage.getItem('ccc_name') || ''; p = p || sessionStorage.getItem('ccc_phone') || ''; } catch(e){} return {name: n || '', phone: p || '', city: d.city || ''}; };
  const CST = {new:['הפנייה התקבלה','#2f6fed'], work:['נציג מטפל בפנייה','#e08a00'], meet:['נקבעה פגישה','#7c4ddb'], quote:['נשלחה אליך הצעת מחיר','#0c97b8'], uw:['בתהליך אישור מימון','#c2417a'], won:['העסקה נסגרה','#18965a'], lost:['הפנייה נסגרה','#8b9098'], noans:['ניסינו להשיג אותך','#d64545']};
  const RT = {form:'פנייה בטופס יצירת קשר', car:'פנייה מעמוד רכב', cart:'בקשת הצעה על רכבים מהסל', loan:'בקשה לבדיקת זכאות למימון'};
  const ic = '<svg viewBox="0 0 24 24" width="56" height="56" aria-hidden="true"><circle cx="9.5" cy="19.5" r="1.5" fill="currentColor"/><circle cx="17" cy="19.5" r="1.5" fill="currentColor"/><path d="M2.5 3.5h2.2l2.4 11.1a1.5 1.5 0 0 0 1.5 1.2h8.7a1.5 1.5 0 0 0 1.5-1.1L21 7.5H5.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  let cart = LS.get('ccc_cart', []).filter(k => idxOf(k) >= 0), remote = null, prog = null, tab = 'cart'; const openTl = new Set();

  function head(){
    const d = me(), p = d.name.trim().split(/\s+/).filter(Boolean);
    $('av').textContent = p.length ? p[0][0] + (p[1] ? p[1][0] : '') : '?';
    $('hi').textContent = d.name ? 'שלום ' + d.name : 'שלום, אורח/ת';
    $('nCart').textContent = cart.length || ''; $('nReq').textContent = reqList().length || '';
  }
  function drawCart(){
    const items = cart.map(idxOf).filter(i => i >= 0), P = $('pCart');
    if (!items.length){ P.innerHTML = '<div class="card empty">' + ic + '<b>הסל שלך ריק</b><span>לחצו על סמל הסל בכרטיס של רכב בקטלוג כדי לשמור אותו כאן, ואז שלחו בקשה לנציג על כמה רכבים יחד.</span><a class="btn" href="index.html#catalog">לקטלוג הרכבים</a></div>'; return; }
    P.innerHTML = '<div class="items">' + items.map(i => { const c = CARS[i];
      return '<div class="item"><a class="thumb" href="car.html#car' + i + '"><img src="' + esc(c.img || 'car-sample.png') + '" alt=""></a>' +
        '<a class="iname" href="car.html#car' + i + '"><small>' + esc(c.maker) + '</small><b>' + esc(c.model) + '</b>' + (c.trim ? '<span class="tr">' + esc(c.trim) + '</span>' : '') +
        '<span class="pr">החל מ- ' + fmt(c.price) + '</span><span class="mo">מקדמה ' + fmt(window.CCC_TERMS.downOf(c)) + ' בנוסף למחיר · החזר חודשי משוער ₪' + Math.ceil(monthly(c.price)).toLocaleString('he-IL') + '</span></a>' +
        '<button type="button" class="rm" data-rm="' + esc(keyOf(c)) + '" aria-label="הסרה מהסל: ' + esc(fullName(c)) + '">×</button></div>'; }).join('') + '</div>' +
      '<div class="sum"><span>' + items.length + (items.length === 1 ? ' רכב בסל · נציג יחזור אליכם עם הצעה' : ' רכבים בסל · נציג יחזור אליכם עם הצעה') + '</span><button type="button" class="btn" id="send">שליחת בקשה לנציג על הרכבים בסל</button></div>';
  }
  // requests come from the server (leads/<uid>.reqs), so they are the same on every device; requests this browser sent
  // that are not on the server are listed too, marked as not saved
  const reqList = () => {
    const log = LS.get('ccc_reqs', []), rq = (remote && Array.isArray(remote.reqs) ? remote.reqs : []).filter(q => !q.mergedInto), have = new Set(rq.map(q => q.rid));
    return rq.map(q => Object.assign({saved: true}, q)).concat(log.filter(r => r.rid && !have.has(r.rid)).map(r => ({rid: r.rid, ts: r.ts, src: r.src, car: (r.cars || []).join(', '), cars: r.cars, loan: r.amount ? {amount: r.amount, trade: r.trade} : null, saved: false})))
      .sort((a, b) => String(b.ts).localeCompare(String(a.ts)));
  };
  const carByName = n => CARS.find(c => fullName(c) === String(n || '').trim());
  function dealHtml(q){
    const T = window.CCC_TERMS, rows = [], names = (q.cars && q.cars.length ? q.cars : String(q.car || '').split(', ')).filter(Boolean);
    if (names.length) rows.push(['רכב', names.join(' · ')]);
    let d = q.deal, live = false;
    if (!d && names.length === 1){ const c = carByName(names[0]); if (c && T){ d = {price: c.price, down: T.downOf(c), monthly: Math.ceil(T.monthlyOf(c.price)), months: T.months, rate: T.rate, balloon: T.balloon}; live = true; } }
    if (d){ rows.push(['מחיר הרכב', fmt(d.price)], ['מקדמה (בנוסף למחיר)', fmt(d.down)], ['מסלול מימון', d.months + ' תשלומים · ריבית ' + d.rate + '% · בלון ' + d.balloon + '%'], ['תקופת המימון', d.months + ' חודשים'], ['החזר חודשי משוער', fmt(d.monthly)]); }
    else if (names.length > 1) names.forEach(n => { const c = carByName(n); if (c) rows.push(['', n + ': ' + fmt(c.price)]); });
    if (q.loan && q.loan.amount) rows.push(['סכום מימון מבוקש', fmt(q.loan.amount)]);
    const tr = q.loan && q.loan.trade; if (tr) rows.push(['טרייד-אין', typeof tr === 'object' ? [tr.plate, tr.make, tr.model, tr.year, tr.km ? Number(tr.km).toLocaleString('he-IL') + ' ק"מ' : ''].filter(Boolean).join(' · ') || 'כן' : 'כן']);
    rows.push(['תאריך הבקשה', new Date(q.ts).toLocaleString('he-IL', {day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit'})]);
    return '<dl class="deal">' + rows.map(([k, v]) => '<dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd>').join('') + '</dl>' + (live ? '<span class="deal-n">המחיר וההחזר לפי מחירי האתר היום (הבקשה נשלחה לפני שמירת פרטי העסקה).</span>' : '');
  }
  function tlHtml(q){
    const S = window.CCC_STAGES, L = window.CCC_STAGE_LABEL; if (!S) return '';
    const p = prog && prog.reqs && prog.reqs[q.rid], stage = p && p.stage ? +p.stage : 2, res = p && p.result, stop = stage === 7 && res === 'rejected';
    const last = stop ? 7 : 12, all = openTl.has(q.rid), upto = all ? last : Math.min(last, stage + 1);
    const items = []; for (let n = 1; n <= upto; n++){
      const cls = n < stage ? 'done' : n === stage ? (stop ? 'stop' : (stage === 12 ? 'done' : 'cur')) : '';
      const when = p && Array.isArray(p.log) ? (p.log.slice().reverse().find(x => +x.stage === n) || {}).ts : (n === 1 ? q.ts : null);
      items.push('<li class="' + cls + '">' + esc(n + '. ' + L(n, n === stage ? res : null)) + (when && n <= stage ? '<small>' + esc(new Date(when).toLocaleDateString('he-IL')) + '</small>' : '') + '</li>');
    }
    return '<ol class="tl" aria-label="מעקב אחר הבקשה">' + items.join('') + '</ol>' + (upto < last ? '<button type="button" class="tl-more" data-tl="' + esc(q.rid) + '">הצגת כל שלבי התהליך</button>' : (all && last > stage + 1 ? '<button type="button" class="tl-more" data-tl="' + esc(q.rid) + '">הסתרת השלבים הבאים</button>' : ''));
  }
  function drawReq(){
    const list = reqList(), P = $('pReq');
    if (!list.length){ P.innerHTML = '<div class="card empty"><b>עדיין לא שלחת פניות</b><span>כל פנייה שתשלחו באתר, מהטופס, מעמוד רכב, מהסל או מבדיקת הזכאות, תופיע כאן יחד עם הסטטוס שלה.</span></div>'; return; }
    P.innerHTML = '<div class="reqs">' + list.map(q => {
      const p = prog && prog.reqs && prog.reqs[q.rid], stage = p && p.stage ? +p.stage : 2;
      const s = !q.saved ? ['לא נשמרה במערכת', '#b3261e'] : [window.CCC_STAGE_LABEL ? window.CCC_STAGE_LABEL(stage, p && p.result) : (CST[q.status] || CST.new)[0], stage === 7 && p && p.result === 'rejected' ? '#b3261e' : '#7a2a4a'];
      return '<div class="req"><div class="req-top"><span class="st" style="--c:' + s[1] + '">' + esc(s[0]) + '</span><span class="req-no">#' + esc(String(q.rid || '').toUpperCase()) + '</span></div>' +
        '<b>' + esc(RT[q.src] || 'בקשה') + '</b>' + (!q.saved ? '<div class="req-warn">הבקשה נשמרה רק בדפדפן הזה ולא הגיעה אלינו. שלחו אותה שוב, או פנו אלינו בוואטסאפ 054-576-2802.</div>' : '') +
        dealHtml(q) + (q.saved ? tlHtml(q) : '') + '</div>'; }).join('') + '</div>';
  }
  function drawInfo(){ const d = me(), m = LS.get('ccc_me', {}); $('iName').value = d.name; $('iPhone').value = d.phone; $('iCity').value = d.city; $('iMail').value = (window.cccAuth && cccAuth.user() && cccAuth.user().email) || m.email || ''; $('iMail').readOnly = !!(window.cccAuth && cccAuth.user()); $('iId').value = (remote && remote.profile && remote.profile.idn) || ''; $('iDob').value = (remote && remote.profile && remote.profile.dob) || ''; $('iUser').value = m.username || ''; $('iPw').value = $('iPw2').value = '';
    $('sCart').textContent = cart.length; $('sReq').textContent = reqList().length; document.querySelectorAll('.fe').forEach(x => x.textContent = ''); document.querySelectorAll('input.bad').forEach(x => x.classList.remove('bad')); }
  function show(){
    tab = ['cart','req','info'].includes(location.hash.slice(1)) ? location.hash.slice(1) : 'cart';
    document.querySelectorAll('.tabs a').forEach(a => { if (a.dataset.tab === tab) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
    $('pCart').hidden = tab !== 'cart'; $('pReq').hidden = tab !== 'req'; $('pInfo').hidden = tab !== 'info';
    head(); if (tab === 'cart') drawCart(); if (tab === 'req') drawReq(); if (tab === 'info') drawInfo();
  }
  async function send(){
    const d = me(), items = cart.map(idxOf).filter(i => i >= 0); if (!items.length) return;
    if (!d.name || !/^0\d{8,9}$/.test(String(d.phone).replace(/\D/g,''))){ location.hash = '#info'; setTimeout(() => { const m = $('iMsg'); m.textContent = 'כדי שנציג יחזור אליכם, מלאו שם וטלפון ושמרו, ואז חזרו לסל.'; m.classList.add('err'); m.hidden = false; $('iName').focus(); }, 30); return; }
    const names = items.map(i => fullName(CARS[i]) + ' (החל מ-' + fmt(CARS[i].price) + ')');
    const msg = 'שלום, אני ' + d.name + '. טלפון: ' + d.phone + '.\nאשמח לקבל הצעה על הרכבים ששמרתי בסל:\n' + names.map(n => '• ' + n).join('\n');
    const b = $('send'); b.disabled = true; b.textContent = 'שולחים…';
    const ok = await window.cccLead({src:'cart', req: true, cars: items.map(i => fullName(CARS[i])), name: d.name, phone: d.phone, city: d.city, car: items.map(i => fullName(CARS[i])).join(', '), detail: 'שלח בקשה להצעה על ' + items.length + (items.length === 1 ? ' רכב מהסל: ' : ' רכבים מהסל: ') + names.join(', ')});
    b.disabled = false; b.textContent = 'שליחת בקשה לנציג על הרכבים בסל'; head();
    window.cccDone({ok, phone: d.phone, wa: 'https://wa.me/972545762802?text=' + encodeURIComponent(msg)});
    loadRemote();
  }
  async function loadRemote(){
    try { const [db, user] = await Promise.all([claude.use('db'), claude.use('user')]); if (!db || !user) return; const id = await user.id(); if (!id) return;
      const s = await db.collection('leads').doc(id).get(); remote = s.exists ? s.data() : null;
      try { const g = await db.collection('progress').doc(id).get(); prog = g.exists ? g.data() : null; } catch(e) { prog = null; }
      head(); if (tab === 'req') drawReq(); if (tab === 'info') drawInfo(); } catch(e){}
  }
  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-rm]'); if (rm){ cart = cart.filter(k => k !== rm.dataset.rm); LS.set('ccc_cart', cart); head(); drawCart(); return; }
    if (e.target.closest('#send')) send();
    const tl = e.target.closest('[data-tl]'); if (tl){ const r = tl.dataset.tl; openTl.has(r) ? openTl.delete(r) : openTl.add(r); drawReq(); }
  });
  $('fInfo').addEventListener('submit', async e => { e.preventDefault();
    const A = window.cccAuth, m0 = LS.get('ccc_me', {}), msg = $('iMsg'); msg.classList.remove('err'); msg.hidden = true;
    const f = {name: $('iName').value.trim().replace(/\s+/g,' ').slice(0,60), username: $('iUser').value.trim(), pw: $('iPw').value, pw2: $('iPw2').value, idn: $('iId').value.replace(/\D/g,''), dob: $('iDob').value,
      phone: $('iPhone').value.replace(/\D/g,'').replace(/^972/,'0'), email: $('iMail').value.trim().toLowerCase(), city: $('iCity').value.trim().slice(0,40)};
    const needPw = !!f.pw; const errs = A.checkFields(f, needPw);
    document.querySelectorAll('.fe').forEach(x => x.textContent = ''); document.querySelectorAll('input.bad').forEach(x => x.classList.remove('bad'));
    const ids = {name:'iName', username:'iUser', pw:'iPw', pw2:'iPw2', idn:'iId', dob:'iDob', phone:'iPhone', email:'iMail'};
    if (Object.keys(errs).length){ Object.entries(errs).forEach(([k, v]) => { const x = document.querySelector('.fe[data-f="' + k + '"]'); if (x) x.textContent = v; $(ids[k]).classList.add('bad'); }); document.querySelector('input.bad').focus(); return; }
    if (f.pw){ try { const u = A.user(); await u.updatePassword(f.pw); }
      catch(err){ msg.textContent = err && err.code === 'auth/requires-recent-login' ? 'כדי להחליף סיסמה, צאו מהחשבון והיכנסו שוב, ואז נסו שוב.' : 'לא הצלחנו להחליף את הסיסמה. נסו שוב.'; msg.classList.add('err'); msg.hidden = false; return; } }
    const m = {name: f.name, username: f.username, phone: f.phone, email: f.email, city: f.city};
    A.put(m); $('iPw').value = $('iPw2').value = '';
    const ok = await window.cccLead({src:'me', name: m.name, phone: m.phone, city: m.city, profile: {username: f.username, idn: f.idn.padStart(9,'0'), dob: f.dob, email: f.email}, detail: 'עדכן פרטים באזור האישי'});
    msg.textContent = ok ? (f.pw ? 'הפרטים והסיסמה החדשה נשמרו.' : 'הפרטים נשמרו בחשבון.') : 'הפרטים נשמרו בדפדפן, אבל לא הגיעו לשרת. נסו שוב בעוד רגע.'; if (!ok) msg.classList.add('err'); msg.hidden = false; head(); loadRemote();
  });
  $('iReset').addEventListener('click', () => window.cccAuth.open('', () => show(), 'reset'));
  $('iOut').addEventListener('click', async () => { await window.cccAuth.signOut(); location.href = 'index.html'; });
  $('iClear').addEventListener('click', () => { ['ccc_me','ccc_cart','ccc_reqs'].forEach(LS.del); try { sessionStorage.removeItem('ccc_unlocked'); } catch(_) {} cart = []; drawInfo(); head(); const m = $('iMsg'); m.classList.remove('err'); m.textContent = 'החשבון, הסל והפניות נמחקו מהדפדפן.'; m.hidden = false; });
  addEventListener('hashchange', show);
  // the personal area opens only after signing in (or opening an account)
  async function gate(){ const A = window.cccAuth; if (!A) return show();
    document.body.classList.add('locked'); await A.ready;
    if (A.unlocked()){ document.body.classList.remove('locked'); show(); loadRemote(); return; }
    A.open(A.hasAccount() ? 'היכנסו עם האימייל והסיסמה שלכם. החשבון פועל מכל מכשיר.' : 'פתחו חשבון כדי להשתמש באזור האישי: הסל, הפניות והמעקב אחריהן, מכל מכשיר.', () => { document.body.classList.remove('locked'); show(); loadRemote(); });
  }
  document.addEventListener('ccc-signed-in', () => { document.body.classList.remove('locked'); show(); loadRemote(); });
  window.addEventListener('load', gate);
})();
</script>
<script src="auth.js"></script>
</body>
</html>
'''
page = (page.replace('__LOGO__', logo_m).replace('__OKCSS__', ok_css).replace('__OKHTML__', ok_html)
        .replace('__LEAD__', lead_js).replace('__DONE__', done_js).replace('__CARS__', json.dumps(cars, ensure_ascii=False)))
open(f'{site}/me.html', 'w', encoding='utf-8').write(page)
print('me.html', len(page))
