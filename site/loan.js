/* ChicCheckCar — financing eligibility request (4 steps). Shared by index.html and car.html.
   Needs window.cccLead / window.cccDone from the host page. Does NOT decide eligibility: it collects the request for a finance rep. */
(function(){
  const BANKS = ['בנק הפועלים','בנק לאומי','בנק דיסקונט','בנק מזרחי טפחות','הבנק הבינלאומי','בנק מרכנתיל','בנק ירושלים','בנק מסד','בנק יהב','וואן זירו','אחר'];
  const nis = n => '₪' + Math.round(n).toLocaleString('he-IL');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const idOk = v => { v = String(v).replace(/\D/g,''); if (v.length < 5 || v.length > 9) return false; v = v.padStart(9,'0'); let s = 0; for (let i = 0; i < 9; i++){ let d = +v[i] * (i % 2 + 1); s += d > 9 ? d - 9 : d; } return s % 10 === 0; };
  const phoneOk = v => /^05\d{8}$/.test(String(v).replace(/\D/g,'').replace(/^972/,'0'));
  const pad = n => String(n).padStart(2,'0');
  const ymd = dt => dt.getFullYear() + '-' + pad(dt.getMonth()+1) + '-' + pad(dt.getDate());
  const yearsAgo = y => { const t = new Date(); t.setFullYear(t.getFullYear() - y); return t; };
  const dobMax = () => ymd(yearsAgo(18)), dobMin = () => ymd(yearsAgo(100));
  const age = s => { const b = new Date(s + 'T00:00:00'), t = new Date(); let a = t.getFullYear() - b.getFullYear(); if (t.getMonth() < b.getMonth() || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--; return a; };
  const dobTxt = s => s ? s.split('-').reverse().join('/') : '';
  const fmtPlate = v => { v = String(v).replace(/\D/g,'').slice(0,8); if (v.length === 8) return v.slice(0,3) + '-' + v.slice(3,5) + '-' + v.slice(5); if (v.length > 5) return v.slice(0,2) + '-' + v.slice(2,5) + '-' + v.slice(5); if (v.length > 2) return v.slice(0,2) + '-' + v.slice(2); return v; };
  const mailOk = v => /^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(String(v).trim());

  const css = `
.ln{position:fixed;inset:0;z-index:350;display:flex;justify-content:center;align-items:flex-end;font-family:"Heebo",system-ui,"Segoe UI",Arial,sans-serif;color:#1f1519}
.ln[hidden]{display:none}
.ln-bg{position:absolute;inset:0;background:rgba(20,12,16,.5);backdrop-filter:blur(4px);animation:lnFade .2s ease}
.ln-sheet{position:relative;width:min(520px,100%);max-height:94vh;background:#fbf9f8;border-radius:26px 26px 0 0;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 -20px 60px -20px rgba(0,0,0,.45);animation:lnUp .32s cubic-bezier(.2,.8,.2,1);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (min-width:700px){.ln{align-items:center}.ln-sheet{border-radius:26px;max-height:90vh}}
@keyframes lnUp{from{transform:translateY(40px);opacity:0}}@keyframes lnFade{from{opacity:0}}
@media (prefers-reduced-motion:reduce){.ln-sheet,.ln-bg{animation:none}}
.ln-top{display:flex;align-items:center;justify-content:center;position:relative;height:62px;background:#fff;border-bottom:1px solid rgba(31,21,25,.08);flex:none}
.ln-logo{height:40px;width:auto}
.ln-x{position:absolute;inset-inline-start:14px;top:12px;width:38px;height:38px;border-radius:50%;border:0;background:#f1ecec;font-size:20px;line-height:1;cursor:pointer;color:#6a5a60}
.ln-body{overflow:auto;padding:20px 20px 8px;flex:1}
.ln-prog{display:flex;gap:6px;margin-bottom:14px}
.ln-prog i{flex:1;height:4px;border-radius:4px;background:#e6dcdf}
.ln-prog i.on{background:#7a2a4a}
.ln-step{font-size:20px;font-weight:800;margin:0}
.ln-q{font-size:15px;color:#6a5a60;margin:2px 0 16px}
.ln-box{background:#fff;border:1px solid rgba(31,21,25,.08);border-radius:22px;padding:18px;display:flex;flex-direction:column;gap:12px}
.ln-car{display:flex;align-items:center;gap:12px;padding:12px;border:1px solid rgba(31,21,25,.1);border-radius:16px;background:#fff}
.ln-car img{width:92px;aspect-ratio:16/10;object-fit:contain;border-radius:10px;background:radial-gradient(90% 80% at 50% 30%,#fff 0,#ebe4e3 75%)}
.ln-car b{display:block;font-size:16px}.ln-car small{color:#6a5a60;font-size:13px}
.ln-amtl{text-align:center;font-size:14px;color:#6a5a60;margin-top:4px}
.ln-amt{text-align:center;font-size:44px;font-weight:800;color:#7a2a4a;line-height:1.1;font-variant-numeric:tabular-nums;direction:ltr}
.ln-pct{align-self:center;font-size:13px;font-weight:700;color:#7a2a4a;background:#f4e9ee;border-radius:999px;padding:3px 12px}
.ln input[type=range]{width:100%;accent-color:#7a2a4a;height:28px;margin:4px 0}
.ln-rng{display:flex;justify-content:space-between;font-size:12.5px;color:#6a5a60;font-variant-numeric:tabular-nums}
.ln-rng span{background:#f6f1f2;border-radius:999px;padding:3px 10px}
.ln-note{font-size:12px;color:#6a5a60;line-height:1.6;background:#f6f1f2;border-radius:14px;padding:12px;margin:0}
.ln label{display:flex;flex-direction:column;gap:6px;font-size:13.5px;font-weight:700;color:#1f1519}
.ln input:not([type=range]):not([type=checkbox]),.ln select{font:inherit;font-size:16px;font-weight:400;padding:12px 14px;border:1.5px solid rgba(31,21,25,.14);border-radius:14px;background:#fff;color:#1f1519;width:100%;box-sizing:border-box;box-shadow:none;height:auto}
.ln input:focus,.ln select:focus{outline:none;border-color:#7a2a4a;box-shadow:0 0 0 3px rgba(122,42,74,.14)}
.ln .bad{border-color:#c0392b !important}
.ln-err{color:#b3261e;font-size:12.5px;font-weight:600;min-height:0;margin:-4px 0 0}
.ln-err:empty{display:none}
.ln-seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.ln-seg button{font:inherit;font-size:15.5px;font-weight:700;padding:13px;border-radius:14px;border:1.5px solid rgba(31,21,25,.14);background:#fff;color:#1f1519;cursor:pointer}
.ln-seg button[aria-pressed=true]{background:#1f1519;border-color:#1f1519;color:#fff}
.ln-ck{flex-direction:row !important;align-items:flex-start;gap:10px !important;font-weight:400 !important;font-size:13px !important;color:#6a5a60 !important;line-height:1.55}
.ln-ck input{width:20px;height:20px;accent-color:#7a2a4a;flex:none;margin-top:1px}
.ln-ck a{color:#7a2a4a}
.ln-sum{display:grid;grid-template-columns:auto 1fr;gap:8px 14px;margin:0;font-size:14.5px}
.ln-sum dt{color:#6a5a60}.ln-sum dd{margin:0;font-weight:700;text-align:left;direction:rtl}
.ln-foot{display:flex;align-items:center;gap:10px;padding:14px 20px 18px;flex:none}
.ln-next{flex:1;font:inherit;font-size:17px;font-weight:800;padding:15px;border:0;border-radius:999px;background:#7a2a4a;color:#fff;cursor:pointer;box-shadow:0 12px 26px -12px rgba(122,42,74,.7)}
.ln-next:disabled{opacity:.5;cursor:default;box-shadow:none}
.ln-back{width:52px;height:52px;border-radius:50%;border:1.5px solid rgba(31,21,25,.14);background:#fff;font-size:20px;cursor:pointer;color:#1f1519;flex:none}
.ln-back[hidden]{display:none}
.ln-plate{display:flex;align-items:stretch;border:2.5px solid #1f1519;border-radius:10px;overflow:hidden;background:#ffd200;direction:ltr;max-width:280px;box-shadow:0 2px 0 rgba(0,0,0,.08)}
.ln-il{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;background:#1d3fa8;color:#fff;padding:4px 7px;flex:none}
.ln-il b{font-size:15px;line-height:1}.ln-il small{font-size:8px;font-weight:500}
.ln .ln-plate input{border:0 !important;border-radius:0 !important;background:transparent !important;box-shadow:none !important;font-size:24px !important;font-weight:800 !important;letter-spacing:.06em;text-align:center;color:#1f1519;padding:8px 10px !important}
.ln .ln-plate input::placeholder{color:rgba(31,21,25,.35)}
.ln .ln-plate:focus-within{box-shadow:0 0 0 3px rgba(122,42,74,.25)}
.ln-two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#lnTr{display:flex;flex-direction:column;gap:12px}
#lnTr[hidden]{display:none}
.ln-seg button{line-height:1.3}
.ln-pinfo{font-size:12.5px;color:#6a5a60;margin:-4px 0 0}.ln-pinfo:empty{display:none}.ln-pinfo.ok{color:#18794e;font-weight:600}
.ln-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  const root = document.createElement('div'); root.className = 'ln'; root.hidden = true;
  root.setAttribute('role','dialog'); root.setAttribute('aria-modal','true'); root.setAttribute('aria-labelledby','lnStep');
  root.innerHTML = `<div class="ln-bg" data-ln-close></div>
  <div class="ln-sheet">
    <div class="ln-top"><img class="ln-logo" src="logo-wide.png" alt="ChicCheckCar"><button type="button" class="ln-x" data-ln-close aria-label="סגירה">×</button></div>
    <div class="ln-body"><div class="ln-prog" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div id="lnPane"></div></div>
    <div class="ln-foot"><button type="button" class="ln-next" id="lnNext">המשך</button><button type="button" class="ln-back" id="lnBack" aria-label="חזרה לשלב הקודם">›</button></div>
  </div>`;
  document.body.appendChild(root);
  const $ = s => root.querySelector(s);

  let step = 1, d = {};
  function saved(){ let m = {}; try { m = JSON.parse(localStorage.getItem('ccc_me') || '{}') || {}; } catch(e){} let n = '', p = ''; try { n = sessionStorage.getItem('ccc_name') || ''; p = sessionStorage.getItem('ccc_phone') || ''; } catch(e){} return {name: m.name || n, phone: m.phone || p}; }

  function head(n, q){ root.querySelectorAll('.ln-prog i').forEach((x, i) => x.classList.toggle('on', i < n)); return `<h2 class="ln-step" id="lnStep">שלב ${n} מתוך 5</h2><p class="ln-q">${q}</p>`; }
  function render(){
    const P = $('#lnPane'); $('#lnBack').hidden = step === 1;
    $('#lnNext').textContent = step === 5 ? 'שליחת בקשה לבדיקת זכאות' : 'המשך';
    if (step === 1){
      const max = d.price || 0, min = max ? Math.min(max, Math.max(10000, Math.round(max * 0.1 / 1000) * 1000)) : 0;
      P.innerHTML = head(1, 'מה גובה המימון הנדרש?') + `<div class="ln-box">
        ${d.car ? `<div class="ln-car">${d.img ? `<img src="${esc(d.img)}" alt="">` : ''}<div><b>${esc(d.car)}</b><small>מחיר: ${nis(d.price)}</small></div></div>` : ''}
        ${max ? `<div class="ln-amtl" id="lnAmtL">סכום המימון</div><div class="ln-amt" id="lnAmt" aria-live="polite"></div><span class="ln-pct" id="lnPct"></span>
        <input type="range" id="lnR" min="${min}" max="${max}" step="1000" value="${d.amount || max}" aria-labelledby="lnAmtL">
        <div class="ln-rng"><span>${nis(min)}</span><span>${nis(max)}</span></div>` :
        `<label>סכום המימון המבוקש (₪)<input id="lnAmtIn" inputmode="numeric" value="${d.amount || ''}" placeholder="לדוגמה 120,000"></label><p class="ln-err" id="lnE1"></p>`}
        <p class="ln-note">זו בקשה לבדיקת זכאות בלבד, ולא אישור הלוואה. ההחלטה על המימון, הריבית והתנאים מתקבלת על ידי הגוף המממן, אחרי שיחה עם נציג ובדיקת הנתונים שלכם.</p></div>`;
      const r = $('#lnR');
      if (r){ const upd = () => { d.amount = +r.value; d.amount = Math.min(d.amount, max); if (+r.value >= max - 999) d.amount = max; $('#lnAmt').textContent = nis(d.amount); $('#lnPct').textContent = Math.round(d.amount / max * 100) + '% מימון'; }; r.addEventListener('input', upd); upd(); }
    }
    if (step === 2){
      const s = saved();
      P.innerHTML = head(2, 'שנכיר קצת?') + `<div class="ln-box">
        <label>שם מלא<input id="lnName" autocomplete="name" value="${esc(d.name ?? s.name)}"></label><p class="ln-err" data-e="name"></p>
        <label>תעודת זהות<input id="lnId" inputmode="numeric" autocomplete="off" maxlength="9" dir="ltr" value="${esc(d.idn || '')}"></label><p class="ln-err" data-e="idn"></p>
        <label>תאריך לידה<input id="lnDob" type="date" dir="ltr" autocomplete="bday" max="${dobMax()}" min="${dobMin()}" value="${esc(d.dob || '')}"></label><p class="ln-err" data-e="dob"></p>
        <label>טלפון נייד<input id="lnPhone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" value="${esc(d.phone ?? s.phone)}"></label><p class="ln-err" data-e="phone"></p>
        <label>אימייל<input id="lnMail" type="email" autocomplete="email" dir="ltr" value="${esc(d.email || '')}"></label><p class="ln-err" data-e="email"></p></div>`;
    }
    if (step === 3){
      P.innerHTML = head(3, 'קצת על ההכנסה שלכם') + `<div class="ln-box">
        <div><span class="ln-sr" id="lnEmpL">סוג תעסוקה</span><div class="ln-seg" role="group" aria-labelledby="lnEmpL"><button type="button" data-emp="שכיר" aria-pressed="${d.emp === 'שכיר'}">שכיר/ה</button><button type="button" data-emp="עצמאי" aria-pressed="${d.emp === 'עצמאי'}">עצמאי/ת</button></div></div><p class="ln-err" data-e="emp"></p>
        <label>הכנסה חודשית נטו (₪)<input id="lnInc" inputmode="numeric" dir="ltr" value="${d.income ? Number(d.income).toLocaleString('he-IL') : ''}" placeholder="לדוגמה 12,000"></label><p class="ln-err" data-e="income"></p>
        <label>הבנק שלכם<select id="lnBank"><option value="">בחרו בנק</option>${BANKS.map(b => `<option${d.bank === b ? ' selected' : ''}>${b}</option>`).join('')}</select></label><p class="ln-err" data-e="bank"></p></div>`;
      root.querySelectorAll('[data-emp]').forEach(b => b.addEventListener('click', () => { d.emp = b.dataset.emp; root.querySelectorAll('[data-emp]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); }));
      $('#lnInc').addEventListener('input', e => { const v = e.target.value.replace(/\D/g,''); e.target.value = v ? Number(v).toLocaleString('he-IL') : ''; });
    }
    if (step === 4){
      const T = d.trade || {};
      const yrs = []; for (let y = new Date().getFullYear(); y >= 1990; y--) yrs.push(y);
      P.innerHTML = head(4, 'יש לכם רכב לטרייד-אין?') + `<div class="ln-box">
        <div class="ln-seg" role="group" aria-label="רכב לטרייד-אין"><button type="button" data-tr="yes" aria-pressed="${d.hasTrade === true}">כן, יש לי רכב למסור</button><button type="button" data-tr="no" aria-pressed="${d.hasTrade === false}">לא, תודה</button></div><p class="ln-err" data-e="hasTrade"></p>
        <div id="lnTr" ${d.hasTrade ? '' : 'hidden'}>
          <label>מספר הרכב שלכם<span class="ln-plate" dir="ltr"><span class="ln-il" aria-hidden="true"><b>IL</b><small>ישראל</small></span><input id="lnPlate" inputmode="numeric" dir="ltr" autocomplete="off" placeholder="00-000-00" maxlength="10" value="${esc(T.plate || '')}" aria-label="מספר רישוי"></span></label><p class="ln-err" data-e="plate"></p><p class="ln-pinfo" id="lnPInfo" role="status" aria-live="polite"></p>
          <label>יצרן ודגם<input id="lnTMod" autocomplete="off" placeholder="לדוגמה: טויוטה קורולה" value="${esc(T.model || '')}"></label><p class="ln-err" data-e="tmod"></p>
          <div class="ln-two"><label>שנת עלייה לכביש<select id="lnTYear"><option value="">בחרו שנה</option>${yrs.map(y => `<option${String(T.year) === String(y) ? ' selected' : ''}>${y}</option>`).join('')}</select></label>
          <label>קילומטראז'<input id="lnTKm" inputmode="numeric" dir="ltr" placeholder="לדוגמה 85,000" value="${T.km ? Number(T.km).toLocaleString('he-IL') : ''}"></label></div><p class="ln-err" data-e="tyear"></p><p class="ln-err" data-e="tkm"></p>
          <p class="ln-note">שווי הרכב לטרייד-אין נקבע על ידי שמאי, אחרי בדיקה של הרכב. נציג יתאם אתכם את הבדיקה.</p>
        </div></div>`;
      root.querySelectorAll('[data-tr]').forEach(b => b.addEventListener('click', () => { d.hasTrade = b.dataset.tr === 'yes'; root.querySelectorAll('[data-tr]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); $('#lnTr').hidden = !d.hasTrade; err('hasTrade',''); if (d.hasTrade) setTimeout(() => $('#lnPlate').focus(), 30); }));
      const pl = $('#lnPlate'); pl.addEventListener('input', () => { pl.value = fmtPlate(pl.value); plateLookup(pl.value); });
      $('#lnTKm').addEventListener('input', e => { const v = e.target.value.replace(/\D/g,''); e.target.value = v ? Number(v).toLocaleString('he-IL') : ''; });
    }
    if (step === 5){
      const row = (k, v) => v ? `<dt>${k}</dt><dd>${esc(v)}</dd>` : '';
      const T = d.hasTrade && d.trade ? d.trade : null;
      P.innerHTML = head(5, 'בדקו שהכול נכון ושלחו') + `<div class="ln-box"><dl class="ln-sum">
        ${row('רכב', d.car)}${row('סכום מימון', d.amount ? nis(d.amount) : '')}${row('שם', d.name)}${row('ת"ז', d.idn)}${row('תאריך לידה', dobTxt(d.dob))}${row('טלפון', d.phone)}${row('אימייל', d.email)}
        ${row('תעסוקה', d.emp)}${row('הכנסה נטו', d.income ? nis(d.income) : '')}${row('בנק', d.bank)}${row('טרייד-אין', T ? T.model + ' · ' + T.year + ' · ' + Number(T.km).toLocaleString('he-IL') + ' ק"מ · מס׳ ' + T.plate : 'ללא')}</dl>
        <label class="ln-ck"><input type="checkbox" id="lnOk" ${d.agree ? 'checked' : ''}><span>אני מאשר/ת ש-ChicCheckCar תשמור את הפרטים, תחזור אליי בנוגע למימון, ותעביר לגוף המממן רק את מה שנדרש לבדיקה. <a href="index.html#privacy" target="_blank" rel="noopener">מדיניות הפרטיות</a></span></label><p class="ln-err" data-e="agree"></p></div>`;
      const ok = $('#lnOk'); const sync = () => { d.agree = ok.checked; $('#lnNext').disabled = !ok.checked; }; ok.addEventListener('change', sync); sync();
    } else $('#lnNext').disabled = false;
    const f = step === 4 ? null : P.querySelector('input:not([type=range]),select,[data-emp]'); if (f && step > 1) setTimeout(() => f.focus(), 50);
  }
  // Trade-in: fill make/model and first-registration year from the Ministry of Transport open data (data.gov.il).
  // Only fills what the registry returns; if the lookup fails the customer simply types the details.
  const GOV = 'https://data.gov.il/api/3/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3&limit=1&filters=';
  let plateSeq = 0, autoModel = '', autoYear = '';
  // The registry stores the maker with its country, often cut off: "קיה ד. קוריאה", "מרצדס בנץ גרמנ", "אלפא רומיאו_אי".
  // Drop the country part so the customer sees just the maker.
  const COUNTRIES = ['גרמניה','סלובקיה','ספרד','פולין','תאילנד','ארהב','הולנד','סין','רומניה','יפן','אנגליה','הודו','טורקיה','תורכיה','צרפת','קוריאה','ד.קוריאה','צ\'כיה','מקסיקו','קנדה','איטליה','הונגריה','פורטוגל','בלגיה','שבדיה','ברזיל','ארגנטינה','אוסטריה','אוסטרליה','סלובניה','רוסיה','אינדונזיה','מלזיה','פינלנד','מרוקו','טייוואן','וייטנאם','ישראל','דרום'];
  function makerName(s){
    let out = String(s || '').replace(/["']+$/,'').trim();
    for (let k = 0; k < 2; k++){
      const m = out.match(/^(.+?)[\s_\-]+([^\s_\-]+)$/); if (!m) break;
      const t = m[2].replace(/["']/g,'');
      const hit = t === 'אי' || t === 'ד.' || (t.length >= 3 && COUNTRIES.some(c => c.replace(/'/g,'').startsWith(t.replace(/'/g,''))));
      if (!hit) break;
      out = m[1].trim();
    }
    return out || String(s || '').trim();
  }
  async function plateLookup(v){
    const num = String(v).replace(/\D/g,''), info = $('#lnPInfo'), seq = ++plateSeq;
    if (!info) return;
    if (!/^\d{7,8}$/.test(num)){ info.textContent = ''; info.classList.remove('ok'); return; }
    info.classList.remove('ok'); info.textContent = 'מחפשים את הרכב במאגר משרד התחבורה…';
    let rec = null;
    try {
      const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), 8000);
      const r = await fetch(GOV + encodeURIComponent(JSON.stringify({mispar_rechev: +num})), {signal: ctl.signal});
      clearTimeout(t);
      const j = await r.json(); rec = j && j.success && j.result && j.result.records && j.result.records[0] || null;
    } catch(e) { rec = null; }
    if (seq !== plateSeq) return;
    if (!rec){ const m = $('#lnTMod'), y = $('#lnTYear'); if (m && autoModel && m.value === autoModel){ m.value = ''; autoModel = ''; } if (y && autoYear && y.value === autoYear){ y.value = ''; autoYear = ''; } info.textContent = 'לא מצאנו את הרכב במאגר. אפשר למלא את הפרטים ידנית.'; return; }
    const model = [makerName(rec.tozeret_nm), rec.kinuy_mishari || rec.degem_nm].map(x => String(x || '').trim()).filter(Boolean).join(' ');
    const yr = parseInt(String(rec.moed_aliya_lakvish || '').slice(0,4), 10);
    const m = $('#lnTMod'), y = $('#lnTYear');
    if (m && model && (!m.value.trim() || m.value === autoModel)){ m.value = model; autoModel = model; err('tmod',''); }
    if (y && yr && [...y.options].some(o => o.value === String(yr)) && (!y.value || y.value === autoYear)){ y.value = String(yr); autoYear = y.value; err('tyear',''); }
    info.classList.add('ok'); info.textContent = 'מצאנו: ' + model + (yr ? ' · עלייה לכביש ' + yr : '') + '. אפשר לתקן אם צריך.';
  }
  function err(k, m){ const e = root.querySelector('[data-e="' + k + '"]'); if (e) e.textContent = m || ''; const map = {plate:'#lnPlate', tmod:'#lnTMod', tyear:'#lnTYear', tkm:'#lnTKm', name:'#lnName', idn:'#lnId', dob:'#lnDob', phone:'#lnPhone', email:'#lnMail', income:'#lnInc', bank:'#lnBank'}; const i = map[k] && $(map[k]); if (i) i.classList.toggle('bad', !!m); return !m; }
  function validate(){
    if (step === 1){ const i = $('#lnAmtIn'); if (i){ d.amount = +i.value.replace(/\D/g,''); const e = $('#lnE1'); if (!(d.amount >= 5000)){ e.textContent = 'הזינו סכום מימון של ₪5,000 לפחות.'; return false; } e.textContent = ''; } return true; }
    if (step === 2){
      d.name = $('#lnName').value.trim(); d.idn = $('#lnId').value.replace(/\D/g,''); d.dob = $('#lnDob').value; d.phone = $('#lnPhone').value.replace(/\D/g,'').replace(/^972/,'0'); d.email = $('#lnMail').value.trim();
      const a = err('name', d.name.split(/\s+/).filter(Boolean).length >= 2 ? '' : 'כתבו שם פרטי ושם משפחה.');
      const b = err('idn', idOk(d.idn) ? '' : 'מספר תעודת הזהות לא תקין. בדקו שהקלדתם את כל 9 הספרות, כולל ספרת הביקורת.');
      const g = err('dob', !d.dob ? 'בחרו תאריך לידה.' : (isNaN(age(d.dob)) || age(d.dob) > 100) ? 'תאריך הלידה לא תקין.' : age(d.dob) < 18 ? 'בדיקת זכאות למימון אפשרית מגיל 18.' : '');
      const c = err('phone', phoneOk(d.phone) ? '' : 'הזינו מספר נייד תקין, לדוגמה 0501234567.');
      const e = err('email', mailOk(d.email) ? '' : 'הזינו כתובת אימייל תקינה, לדוגמה name@gmail.com.');
      if (b) d.idn = d.idn.padStart(9, '0');
      const first = root.querySelector('.bad'); if (first) first.focus();
      return a && b && g && c && e;
    }
    if (step === 3){
      d.income = +$('#lnInc').value.replace(/\D/g,''); d.bank = $('#lnBank').value;
      const a = err('emp', d.emp ? '' : 'בחרו שכיר/ה או עצמאי/ת.');
      const b = err('income', d.income >= 1000 ? '' : 'הזינו הכנסה חודשית נטו בשקלים.');
      const c = err('bank', d.bank ? '' : 'בחרו את הבנק שלכם.');
      return a && b && c;
    }
    if (step === 4){
      if (d.hasTrade === undefined) return err('hasTrade', 'בחרו אם יש לכם רכב לטרייד-אין.');
      if (!d.hasTrade){ d.trade = null; return true; }
      const plate = $('#lnPlate').value.replace(/\D/g,''), model = $('#lnTMod').value.trim(), year = $('#lnTYear').value, km = +$('#lnTKm').value.replace(/\D/g,'');
      const a = err('plate', /^\d{7,8}$/.test(plate) ? '' : 'מספר רכב צריך להכיל 7 או 8 ספרות.');
      const b = err('tmod', model.length >= 2 ? '' : 'כתבו את היצרן והדגם.');
      const c = err('tyear', year ? '' : 'בחרו שנת עלייה לכביש.');
      const e = err('tkm', $('#lnTKm').value.trim() !== '' && km >= 0 && km < 2000000 ? '' : 'הזינו קילומטראז\' משוער.');
      d.trade = {plate: fmtPlate(plate), model, year: +year, km};
      return a && b && c && e;
    }
    if (step === 5) return err('agree', d.agree ? '' : 'צריך לאשר כדי לשלוח.');
    return true;
  }
  async function submit(){
    const btn = $('#lnNext'); btn.disabled = true; btn.textContent = 'שולחים…';
    const summary = 'בקשה לבדיקת זכאות למימון' + (d.car ? ' על ' + d.car : '') + ': סכום ' + nis(d.amount) + ', ' + d.emp + ', הכנסה נטו ' + nis(d.income) + ', ' + d.bank + (d.trade ? ' · טרייד-אין: ' + d.trade.model + ' ' + d.trade.year + ', ' + Number(d.trade.km).toLocaleString('he-IL') + ' ק"מ, מס׳ ' + d.trade.plate : '');
    const ok = await window.cccLead({src:'loan', req: true, name: d.name, phone: d.phone, car: d.car || '', detail: summary,
      loan: {amount: d.amount, car: d.car || '', price: d.price || 0, idn: d.idn, dob: d.dob, email: d.email, emp: d.emp, income: d.income, bank: d.bank, trade: d.trade || null, ts: new Date().toISOString()}});
    const msg = 'שלום, אני ' + d.name + '. אשמח לבדיקת זכאות למימון' + (d.car ? ' לרכב ' + d.car : '') + '.\nסכום מימון: ' + nis(d.amount) + '\nתעסוקה: ' + d.emp + '\nהכנסה חודשית נטו: ' + nis(d.income) + '\nבנק: ' + d.bank + '\nטלפון: ' + d.phone + '\nאימייל: ' + d.email + (d.trade ? '\nטרייד-אין: ' + d.trade.model + ', ' + d.trade.year + ', ' + Number(d.trade.km).toLocaleString('he-IL') + ' ק"מ, מספר רכב ' + d.trade.plate : '');
    close();
    window.cccDone({ok, phone: d.phone, wa: 'https://wa.me/972545762802?text=' + encodeURIComponent(msg),
      title: ok ? 'בקשתכם התקבלה' : null, text: ok ? 'קיבלנו את הבקשה לבדיקת זכאות למימון. נציג מימון יחזור אליכם בהקדם למספר ' + d.phone + ' עם התשובה והתנאים.' : null});
    btn.disabled = false;
  }
  // clear a field's error as soon as the customer fixes it
  root.addEventListener('input', e => { const k = {lnPlate:'plate', lnTMod:'tmod', lnTYear:'tyear', lnTKm:'tkm', lnName:'name', lnId:'idn', lnDob:'dob', lnPhone:'phone', lnMail:'email', lnInc:'income', lnBank:'bank'}[e.target.id]; if (k) err(k, ''); });
  root.addEventListener('change', e => { const k = {lnTYear:'tyear', lnBank:'bank', lnDob:'dob'}[e.target.id]; if (k) err(k, ''); });
  $('#lnNext').addEventListener('click', () => { if (!validate()) return; if (step === 5) return submit(); step++; render(); $('.ln-body').scrollTop = 0; });
  $('#lnBack').addEventListener('click', () => { if (step > 1){ if (step < 5) validate(); step--; render(); } });
  root.addEventListener('click', e => { if (e.target.closest('[data-ln-close]')) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !root.hidden) close(); });
  let last = null;
  function open(o){
    o = o || {};
    // quick purchase starts with the customer's account: open one (or sign in), then continue to the questionnaire
    const A = window.cccAuth;
    if (A && !(A.hasAccount() && A.unlocked())){ A.require(o.car ? 'כדי להתחיל רכישה זריזה של ' + o.car + ', פתחו חשבון או היכנסו.' : 'כדי להתחיל רכישה זריזה, פתחו חשבון או היכנסו.', () => open(o)); return; }
    last = document.activeElement;
    d = Object.assign({}, d, {car: o.car || '', price: o.price || 0, img: o.img || '', amount: o.price || d.amount || 0});
    if (A){ const m = A.get(); ['name','idn','dob','phone','email'].forEach(k => { if (!d[k] && m[k]) d[k] = m[k]; }); }
    step = 1; render(); root.hidden = false; document.documentElement.style.overflow = 'hidden'; $('#lnNext').focus();
  }
  function close(){ root.hidden = true; document.documentElement.style.overflow = ''; if (last && last.focus) last.focus(); }
  window.cccLoan = {open, close};
})();
