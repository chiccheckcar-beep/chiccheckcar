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
    <div class="priv"><span>🔒 החשבון נשמר בדפדפן הזה. הסיסמה נשמרת מוצפנת ולא נשלחת לשום מקום.</span><button type="button" class="link2" id="iOut">יציאה מהחשבון</button><button type="button" class="link" id="iClear">מחיקת החשבון, הסל והפניות מהדפדפן</button></div>
  </section>
</main>
<footer>ChicCheckCar · <a href="index.html#privacy">מדיניות פרטיות</a> · <a href="index.html#settings">הגדרות פרטיות</a> · <a href="index.html#accessibility">הצהרת נגישות</a></footer>
__OKHTML__
<script src="fb.js"></script>
<script>
const CARS = __CARS__;
__LEAD__
__DONE__
(function(){
  const $ = id => document.getElementById(id);
  const fmt = n => '₪' + Math.round(n).toLocaleString('he-IL');
  const PLAN = {months:60, rate:3.9, balloon:50};
  const monthly = p => { const r = PLAN.rate/100/12, n = PLAN.months, B = p*PLAN.balloon/100; return (p - B/Math.pow(1+r,n)) * r / (1 - Math.pow(1+r,-n)); };
  const fullName = c => [c.maker, c.model, c.trim].filter(Boolean).join(' ');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const LS = { get(k, d){ try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch(e){ return d; } }, set(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }, del(k){ try { localStorage.removeItem(k); } catch(e){} } };
  const keyOf = c => [c.maker, c.model, c.trim, c.price].join('|');
  const idxOf = k => CARS.findIndex(c => keyOf(c) === k);
  const me = () => { const d = LS.get('ccc_me', {}); let n = d.name, p = d.phone; try { n = n || sessionStorage.getItem('ccc_name') || ''; p = p || sessionStorage.getItem('ccc_phone') || ''; } catch(e){} return {name: n || '', phone: p || '', city: d.city || ''}; };
  const CST = {new:['הפנייה התקבלה','#2f6fed'], work:['נציג מטפל בפנייה','#e08a00'], meet:['נקבעה פגישה','#7c4ddb'], quote:['נשלחה אליך הצעת מחיר','#0c97b8'], uw:['בתהליך אישור מימון','#c2417a'], won:['העסקה נסגרה','#18965a'], lost:['הפנייה נסגרה','#8b9098'], noans:['ניסינו להשיג אותך','#d64545']};
  const RT = {form:'פנייה בטופס יצירת קשר', car:'פנייה מעמוד רכב', cart:'בקשת הצעה על רכבים מהסל', loan:'בקשה לבדיקת זכאות למימון'};
  const ic = '<svg viewBox="0 0 24 24" width="56" height="56" aria-hidden="true"><circle cx="9.5" cy="19.5" r="1.5" fill="currentColor"/><circle cx="17" cy="19.5" r="1.5" fill="currentColor"/><path d="M2.5 3.5h2.2l2.4 11.1a1.5 1.5 0 0 0 1.5 1.2h8.7a1.5 1.5 0 0 0 1.5-1.1L21 7.5H5.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  let cart = LS.get('ccc_cart', []).filter(k => idxOf(k) >= 0), remote = null, tab = 'cart';

  function head(){
    const d = me(), p = d.name.trim().split(/\s+/).filter(Boolean);
    $('av').textContent = p.length ? p[0][0] + (p[1] ? p[1][0] : '') : '?';
    $('hi').textContent = d.name ? 'שלום ' + d.name : 'שלום, אורח/ת';
    $('nCart').textContent = cart.length || ''; $('nReq').textContent = LS.get('ccc_reqs', []).length || '';
  }
  function drawCart(){
    const items = cart.map(idxOf).filter(i => i >= 0), P = $('pCart');
    if (!items.length){ P.innerHTML = '<div class="card empty">' + ic + '<b>הסל שלך ריק</b><span>לחצו על סמל הסל בכרטיס של רכב בקטלוג כדי לשמור אותו כאן, ואז שלחו בקשה לנציג על כמה רכבים יחד.</span><a class="btn" href="index.html#catalog">לקטלוג הרכבים</a></div>'; return; }
    P.innerHTML = '<div class="items">' + items.map(i => { const c = CARS[i];
      return '<div class="item"><a class="thumb" href="car.html#car' + i + '"><img src="' + esc(c.img || 'car-sample.png') + '" alt=""></a>' +
        '<a class="iname" href="car.html#car' + i + '"><small>' + esc(c.maker) + '</small><b>' + esc(c.model) + '</b>' + (c.trim ? '<span class="tr">' + esc(c.trim) + '</span>' : '') +
        '<span class="pr">החל מ- ' + fmt(c.price) + '</span><span class="mo">החזר חודשי החל מ- ₪' + Math.ceil(monthly(c.price)).toLocaleString('he-IL') + '</span></a>' +
        '<button type="button" class="rm" data-rm="' + esc(keyOf(c)) + '" aria-label="הסרה מהסל: ' + esc(fullName(c)) + '">×</button></div>'; }).join('') + '</div>' +
      '<div class="sum"><span>' + items.length + (items.length === 1 ? ' רכב בסל · נציג יחזור אליכם עם הצעה' : ' רכבים בסל · נציג יחזור אליכם עם הצעה') + '</span><button type="button" class="btn" id="send">שליחת בקשה לנציג על הרכבים בסל</button></div>';
  }
  function drawReq(){
    const log = LS.get('ccc_reqs', []), P = $('pReq');
    if (!log.length){ P.innerHTML = '<div class="card empty"><b>עדיין לא שלחת פניות</b><span>כל פנייה שתשלחו באתר, מהטופס, מעמוד רכב, מהסל או מבדיקת הזכאות, תופיע כאן יחד עם הסטטוס שלה.</span></div>'; return; }
    const rreqs = remote && Array.isArray(remote.reqs) ? remote.reqs : [];
    P.innerHTML = '<div class="reqs">' + log.slice().reverse().map((r, j) => {
      const rq = r.rid ? rreqs.find(q => q.rid === r.rid) : null;
      const rs = rq ? rq.status : (j === 0 && !rreqs.length && remote ? remote.status : '');
      const s = rs && CST[rs] ? CST[rs] : ['הפנייה נשלחה', '#7a2a4a'];
      const extra = [r.amount ? 'סכום מימון ' + fmt(r.amount) : '', r.trade ? 'כולל טרייד-אין' : ''].filter(Boolean).join(' · ');
      return '<div class="req"><div class="req-top"><span class="st" style="--c:' + s[1] + '">' + s[0] + '</span><small>' + esc(new Date(r.ts).toLocaleString('he-IL',{day:'2-digit',month:'2-digit',year:'2-digit',hour:'2-digit',minute:'2-digit'})) + '</small></div>' +
        '<b>' + esc(RT[r.src] || 'בקשת הצעה על רכבים מהסל') + '</b>' + ((r.cars || []).length ? '<ul>' + r.cars.map(n => '<li>' + esc(n) + '</li>').join('') + '</ul>' : '') + (extra ? '<span class="x">' + esc(extra) + '</span>' : '') + '</div>'; }).join('') + '</div>';
  }
  function drawInfo(){ const d = me(), m = LS.get('ccc_me', {}); $('iName').value = d.name; $('iPhone').value = d.phone; $('iCity').value = d.city; $('iMail').value = m.email || ''; $('iId').value = m.idn || ''; $('iDob').value = m.dob || ''; $('iUser').value = m.username || ''; $('iPw').value = $('iPw2').value = '';
    $('sCart').textContent = cart.length; $('sReq').textContent = LS.get('ccc_reqs', []).length; document.querySelectorAll('.fe').forEach(x => x.textContent = ''); document.querySelectorAll('input.bad').forEach(x => x.classList.remove('bad')); }
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
      const s = await db.collection('leads').doc(id).get(); remote = s.exists ? s.data() : null; if (tab === 'req') drawReq(); } catch(e){}
  }
  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-rm]'); if (rm){ cart = cart.filter(k => k !== rm.dataset.rm); LS.set('ccc_cart', cart); head(); drawCart(); return; }
    if (e.target.closest('#send')) send();
  });
  $('fInfo').addEventListener('submit', async e => { e.preventDefault();
    const A = window.cccAuth, m0 = LS.get('ccc_me', {}), msg = $('iMsg'); msg.classList.remove('err'); msg.hidden = true;
    const f = {name: $('iName').value.trim().replace(/\s+/g,' ').slice(0,60), username: $('iUser').value.trim(), pw: $('iPw').value, pw2: $('iPw2').value, idn: $('iId').value.replace(/\D/g,''), dob: $('iDob').value,
      phone: $('iPhone').value.replace(/\D/g,'').replace(/^972/,'0'), email: $('iMail').value.trim().toLowerCase(), city: $('iCity').value.trim().slice(0,40)};
    const needPw = !!f.pw || !m0.hash; const errs = A.checkFields(f, needPw);
    document.querySelectorAll('.fe').forEach(x => x.textContent = ''); document.querySelectorAll('input.bad').forEach(x => x.classList.remove('bad'));
    const ids = {name:'iName', username:'iUser', pw:'iPw', pw2:'iPw2', idn:'iId', dob:'iDob', phone:'iPhone', email:'iMail'};
    if (Object.keys(errs).length){ Object.entries(errs).forEach(([k, v]) => { const x = document.querySelector('.fe[data-f="' + k + '"]'); if (x) x.textContent = v; $(ids[k]).classList.add('bad'); }); document.querySelector('input.bad').focus(); return; }
    const m = Object.assign(m0, {name: f.name, username: f.username, idn: f.idn.padStart(9,'0'), dob: f.dob, phone: f.phone, email: f.email, city: f.city});
    if (f.pw) await A.setPassword(m, f.pw);
    A.put(m); A.setUnlocked(true); $('iPw').value = $('iPw2').value = '';
    msg.textContent = f.pw ? 'הפרטים והסיסמה החדשה נשמרו.' : 'הפרטים נשמרו.'; msg.hidden = false; head();
    window.cccLead({src:'me', name: m.name, phone: m.phone, city: m.city, profile: A.profileOf(m), detail: 'עדכן פרטים באזור האישי'});
  });
  $('iReset').addEventListener('click', () => window.cccAuth.open('', () => show(), 'reset'));
  $('iOut').addEventListener('click', () => { window.cccAuth.signOut(); location.href = 'index.html'; });
  $('iClear').addEventListener('click', () => { ['ccc_me','ccc_cart','ccc_reqs'].forEach(LS.del); try { sessionStorage.removeItem('ccc_unlocked'); } catch(_) {} cart = []; drawInfo(); head(); const m = $('iMsg'); m.classList.remove('err'); m.textContent = 'החשבון, הסל והפניות נמחקו מהדפדפן.'; m.hidden = false; });
  addEventListener('hashchange', show);
  // the personal area opens only after signing in (or opening an account)
  function gate(){ const A = window.cccAuth; if (!A) return show();
    if (A.hasAccount() && A.unlocked()){ document.body.classList.remove('locked'); show(); loadRemote(); return; }
    document.body.classList.add('locked');
    A.open(A.hasAccount() ? 'היכנסו עם שם המשתמש והסיסמה שלכם.' : 'פתחו חשבון כדי להשתמש באזור האישי: הסל, הפניות והפרטים שלכם.', () => { document.body.classList.remove('locked'); show(); loadRemote(); });
  }
  document.addEventListener('ccc-signed-in', () => { document.body.classList.remove('locked'); show(); });
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
