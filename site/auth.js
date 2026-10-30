/* Chick Chack Car — customer account (registration, sign-in, password reset). Shared by index.html, car.html and me.html.
   Since 2026-10-25 the account is a Firebase Auth email/password account (see fb.js): the same login works on every device,
   and the customer's data lives in Firestore leads/<uid> (readable only by the customer and the team, see firestore.rules).
   Registering upgrades the visitor's anonymous session, so the uid (and the lead document) does not change.
   Password reset = Firebase reset e-mail. This browser keeps only name / phone / city / e-mail / username for pre-filling forms;
   ID number, date of birth and passwords are never stored in the browser. Old browser-only accounts are moved to Firebase on
   their next sign-in (same password). */
(function(){
  const get = () => { try { return JSON.parse(localStorage.getItem('ccc_me') || '{}') || {}; } catch(e){ return {}; } };
  const put = m => { try { localStorage.setItem('ccc_me', JSON.stringify(m)); sessionStorage.setItem('ccc_name', m.name || ''); sessionStorage.setItem('ccc_phone', m.phone || ''); } catch(e){} };
  const digits = v => String(v || '').replace(/\D/g,'');
  const phoneOk = v => /^05\d{8}$/.test(digits(v).replace(/^972/,'0'));
  const mailOk = v => /^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(String(v || '').trim());
  const idOk = v => { v = digits(v); if (v.length < 5 || v.length > 9) return false; v = v.padStart(9,'0'); let s = 0; for (let i = 0; i < 9; i++){ const d = +v[i] * (i % 2 + 1); s += d > 9 ? d - 9 : d; } return s % 10 === 0; };
  const userOk = v => /^[A-Za-z0-9א-ת._-]{3,20}$/.test(String(v || ''));
  const pad = n => String(n).padStart(2,'0');
  const ymd = dt => dt.getFullYear() + '-' + pad(dt.getMonth()+1) + '-' + pad(dt.getDate());
  const yearsAgo = y => { const t = new Date(); t.setFullYear(t.getFullYear() - y); return t; };
  const age = s => { const b = new Date(s + 'T00:00:00'), t = new Date(); let a = t.getFullYear() - b.getFullYear(); if (t.getMonth() < b.getMonth() || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--; return a; };
  const b64 = buf => btoa(String.fromCharCode(...new Uint8Array(buf)));
  async function hashPw(pw, salt){
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveBits']);
    const bits = await crypto.subtle.deriveBits({name:'PBKDF2', hash:'SHA-256', salt: Uint8Array.from(atob(salt), c => c.charCodeAt(0)), iterations: 120000}, key, 256);
    return b64(bits);
  }
  async function setPassword(m, pw){ m.salt = b64(crypto.getRandomValues(new Uint8Array(16))); m.hash = await hashPw(pw, m.salt); return m; }
  const signedIn = () => { const m = get(); return String(m.name || '').trim().length >= 2 && phoneOk(m.phone); };
  // Firebase account state (null = visitor). "ready" resolves once Firebase reported the session.
  let acct = null, readyRes; const ready = new Promise(r => readyRes = r); setTimeout(() => readyRes(), 6000);
  const legacy = () => { const m = get(); return !!(m.username && m.hash); };            // old browser-only account, not yet moved
  const hasAccount = () => !!acct || legacy();
  const unlocked = () => !!acct;
  const setUnlocked = () => {};
  const keepLocal = m => { const o = {}; ['name','phone','city','email','username'].forEach(k => { if (m[k]) o[k] = m[k]; }); return o; };
  async function pullProfile(){            // after sign-in on any device: fill this browser from the account's lead document
    try { const db = await claude.use('db'); const s = await db.collection('leads').doc(acct.uid).get(); if (!s.exists) return;
      const d = s.data() || {}, p = d.profile || {};
      put(Object.assign(keepLocal(get()), {name: d.name || get().name, phone: d.phone || get().phone, city: d.city || get().city, email: p.email || acct.email, username: p.username || get().username}));
    } catch(e) {}
  }
  if (window.cccFb) cccFb.onAuth(u => { const was = acct; acct = u && !u.isAnonymous && !(cccFb.isOwnerUser && cccFb.isOwnerUser(u)) ? u : null;   // a manager signed in on this browser is not a customer account readyRes();
    if (acct && (!was || was.uid !== acct.uid)) pullProfile().then(() => document.dispatchEvent(new CustomEvent('ccc-signed-in')));
    if (!acct && was) document.dispatchEvent(new CustomEvent('ccc-signed-out')); }).catch(() => readyRes());
  else readyRes();
  const fbErr = c => ({'auth/email-already-in-use':'כבר קיים חשבון עם האימייל הזה. היכנסו עם האימייל והסיסמה.', 'auth/credential-already-in-use':'כבר קיים חשבון עם האימייל הזה. היכנסו עם האימייל והסיסמה.',
    'auth/invalid-credential':'האימייל או הסיסמה שגויים.', 'auth/wrong-password':'האימייל או הסיסמה שגויים.', 'auth/user-not-found':'האימייל או הסיסמה שגויים.', 'auth/invalid-email':'כתובת האימייל לא תקינה.',
    'auth/too-many-requests':'היו יותר מדי ניסיונות. נסו שוב בעוד כמה דקות.', 'auth/network-request-failed':'אין חיבור לרשת. נסו שוב.', 'auth/operation-not-allowed':'פתיחת חשבונות לא זמינה כרגע. פנו אלינו בוואטסאפ.',
    'auth/weak-password':'הסיסמה חלשה מדי.'})[c] || 'הפעולה לא הצליחה. נסו שוב.';
  const profileOf = m => ({username: m.username || '', idn: m.idn || '', dob: m.dob || '', email: m.email || ''});

  // validation shared by the registration modal and the personal details page
  function checkFields(f, needPw){
    const e = {};
    if (String(f.name || '').trim().split(/\s+/).filter(Boolean).length < 2) e.name = 'כתבו שם פרטי ושם משפחה.';
    if (!userOk(f.username)) e.username = 'שם משתמש: 3–20 תווים, אותיות, ספרות, נקודה, מקף או קו תחתון, בלי רווחים.';
    if (needPw){
      if (String(f.pw || '').length < 8 || !/\d/.test(f.pw) || !/[A-Za-zא-ת]/.test(f.pw)) e.pw = 'סיסמה: לפחות 8 תווים, עם אותיות וספרות.';
      else if (f.pw !== f.pw2) e.pw2 = 'הסיסמאות לא תואמות.';
    }
    if (!idOk(f.idn)) e.idn = 'מספר תעודת הזהות לא תקין. בדקו את כל 9 הספרות, כולל ספרת הביקורת.';
    if (!f.dob) e.dob = 'בחרו תאריך לידה.'; else if (isNaN(age(f.dob)) || age(f.dob) > 100) e.dob = 'תאריך הלידה לא תקין.'; else if (age(f.dob) < 18) e.dob = 'פתיחת אזור אישי אפשרית מגיל 18.';
    if (!phoneOk(f.phone)) e.phone = 'הזינו מספר נייד תקין, לדוגמה 0501234567.';
    if (!mailOk(f.email)) e.email = 'הזינו כתובת אימייל תקינה, לדוגמה name@gmail.com.';
    return e;
  }

  const css = `
.au{position:fixed;inset:0;z-index:380;display:grid;place-items:center;padding:16px;font-family:"Heebo",system-ui,"Segoe UI",Arial,sans-serif;color:#1f1519}
.au[hidden]{display:none}
.au-bg{position:absolute;inset:0;background:rgba(20,12,16,.5);backdrop-filter:blur(4px)}
.au-card{position:relative;width:min(480px,100%);max-height:94vh;overflow:auto;background:#fbf9f8;border-radius:24px;padding:22px 20px 20px;box-shadow:0 30px 70px -20px rgba(0,0,0,.5);animation:auIn .3s cubic-bezier(.2,.9,.3,1.1)}
@keyframes auIn{from{transform:translateY(14px);opacity:0}}
@media (prefers-reduced-motion:reduce){.au-card{animation:none}}
.au-x{position:absolute;top:12px;left:12px;width:36px;height:36px;border-radius:50%;border:0;background:#f1ecec;color:#6a5a60;font-size:20px;cursor:pointer}
.au-logo{display:block;height:44px;aspect-ratio:600/316;margin:0 auto 6px;background:#7a2a4a;-webkit-mask:var(--logo-m,url(logo-wide.png)) center/contain no-repeat;mask:var(--logo-m,url(logo-wide.png)) center/contain no-repeat}
.au h2{margin:4px 0 2px;text-align:center;font-size:22px;font-weight:800;letter-spacing:-.01em}
.au h2::before{display:none}
.au-sub{margin:0 0 12px;text-align:center;color:#6a5a60;font-size:14px;line-height:1.5}
.au-tabs{display:grid;grid-template-columns:1fr 1fr;background:#f1ecec;border-radius:12px;padding:4px;gap:4px;margin-bottom:12px}
.au-tabs button{border:0;background:transparent;border-radius:9px;padding:9px;font:inherit;font-size:14px;font-weight:700;color:#6a5a60;cursor:pointer}
.au-tabs button.on{background:#fff;color:#7a2a4a;box-shadow:0 1px 3px rgba(31,21,25,.12)}
.au form{display:flex;flex-direction:column;gap:10px}
.au form[hidden]{display:none}
.au-sec{font-size:12px;font-weight:800;color:#7a2a4a;letter-spacing:.06em;margin:6px 0 -2px}
.au label{display:flex;flex-direction:column;gap:5px;font-size:13px;font-weight:700}
.au label small{font-weight:400;color:#6a5a60}
.au input:not([type=checkbox]){font:inherit;font-size:16px;padding:11px 13px;border:1.5px solid rgba(31,21,25,.14) !important;border-radius:13px !important;background:#fff !important;color:#1f1519 !important;width:100%;box-sizing:border-box;box-shadow:none !important;height:auto !important}
.au input:focus{outline:none;border-color:#7a2a4a !important;box-shadow:0 0 0 3px rgba(122,42,74,.14) !important}
.au .bad{border-color:#c0392b !important}
.au-e{margin:-4px 0 0;color:#b3261e;font-size:12px;font-weight:600}
.au-e:empty{display:none}
.au-two{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:start}
@media (max-width:420px){.au-two{grid-template-columns:1fr}}
.au-ck{flex-direction:row !important;align-items:flex-start;gap:8px !important;font-weight:400 !important;color:#6a5a60;font-size:12.5px !important;line-height:1.5}
.au-ck input{width:19px;height:19px;accent-color:#7a2a4a;flex:none;margin-top:1px}
.au-ck a,.au-link{color:#7a2a4a}
.au-link{border:0;background:none;padding:0;font:inherit;font-size:13px;text-decoration:underline;cursor:pointer;align-self:center}
.au-err{margin:0;color:#b3261e;font-size:13px;font-weight:600}
.au-err:empty{display:none}
.au-ok{margin:0;padding:10px 12px;border-radius:10px;background:#e7f6ee;color:#156b43;font-size:13.5px}
.au-ok:empty{display:none}
.au-go{margin-top:4px;border:0;border-radius:999px;padding:14px;background:#7a2a4a;color:#fff;font:inherit;font-size:16px;font-weight:800;cursor:pointer;box-shadow:0 12px 26px -12px rgba(122,42,74,.7)}
.au-go:disabled{opacity:.6}
.au-note{margin:10px 0 0;text-align:center;font-size:12px;color:#6a5a60;line-height:1.5}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  const F = (id, label, attrs, hint) => `<label>${hint ? `<span>${label} <small>${hint}</small></span>` : label}<input id="${id}" ${attrs}></label><p class="au-e" data-e="${id}"></p>`;
  const root = document.createElement('div'); root.className = 'au'; root.hidden = true;
  root.setAttribute('role','dialog'); root.setAttribute('aria-modal','true'); root.setAttribute('aria-labelledby','auT');
  root.innerHTML = `<div class="au-bg" data-au-close></div><div class="au-card">
    <button type="button" class="au-x" data-au-close aria-label="סגירה">×</button>
    <span class="au-logo" role="img" aria-label="Chick Chack Car"></span>
    <h2 id="auT">האזור האישי</h2>
    <p class="au-sub" id="auSub"></p>
    <div class="au-tabs" role="tablist"><button type="button" data-au-tab="reg">פתיחת חשבון</button><button type="button" data-au-tab="login">כניסה</button></div>
    <form id="auReg" novalidate>
      <p class="au-sec">פרטים אישיים</p>
      ${F('auName','שם מלא','autocomplete="name" placeholder="שם פרטי ושם משפחה"')}
      <div class="au-two"><div>${F('auId','תעודת זהות','inputmode="numeric" dir="ltr" maxlength="9" autocomplete="off"')}</div><div>${F('auDob','תאריך לידה','type="date" dir="ltr" autocomplete="bday"')}</div></div>
      <div class="au-two"><div>${F('auPhone','טלפון נייד','type="tel" inputmode="tel" dir="ltr" autocomplete="tel" placeholder="050-0000000"')}</div><div>${F('auMail','אימייל','type="email" dir="ltr" autocomplete="email" placeholder="name@gmail.com"')}</div></div>
      ${F('auCity','עיר','autocomplete="address-level2"','(לא חובה)')}
      <p class="au-sec">פרטי כניסה</p>
      ${F('auUser','שם משתמש','dir="ltr" autocomplete="username" autocapitalize="off" spellcheck="false"')}
      <div class="au-two"><div>${F('auPw','סיסמה','type="password" dir="ltr" autocomplete="new-password"','(8+ תווים)')}</div><div>${F('auPw2','אימות סיסמה','type="password" dir="ltr" autocomplete="new-password"')}</div></div>
      <label class="au-ck"><input type="checkbox" id="auOk"><span>אני מאשר/ת ש-Chick Chack Car תשמור את הפרטים ותחזור אליי בנוגע לרכבים שבחרתי. <a href="index.html#privacy" target="_blank" rel="noopener">מדיניות הפרטיות</a></span></label>
      <p class="au-err" id="auErr" role="alert"></p>
      <button type="submit" class="au-go">פתיחת חשבון והמשך</button>
    </form>
    <form id="auLogin" novalidate hidden>
      ${F('cuLUser','אימייל','type="email" dir="ltr" autocomplete="username" autocapitalize="off" spellcheck="false" placeholder="name@gmail.com"')}
      ${F('cuLPw','סיסמה','type="password" dir="ltr" autocomplete="current-password"')}
      <p class="au-err" id="cuLErr" role="alert"></p>
      <button type="submit" class="au-go">כניסה</button>
      <button type="button" class="au-link" id="cuForgot">שכחתי סיסמה</button>
    </form>
    <form id="auReset" novalidate hidden>
      <p class="au-sub" style="margin:0">הזינו את האימייל של החשבון, ונשלח אליו קישור לבחירת סיסמה חדשה.</p>
      ${F('cuRMail','אימייל','type="email" dir="ltr" autocomplete="email" placeholder="name@gmail.com"')}
      <p class="au-err" id="cuRErr" role="alert"></p><p class="au-ok" id="cuROk" role="status"></p>
      <button type="submit" class="au-go">שליחת קישור לאיפוס</button>
      <button type="button" class="au-link" data-au-tab="login">חזרה לכניסה</button>
    </form>
    <p class="au-note">החשבון שמור במערכת של Chick Chack Car ופועל מכל מכשיר. הסיסמה מנוהלת באמצעות Firebase ואיננו רואים אותה.</p>
  </div>`;
  document.body.appendChild(root);
  const $ = id => document.getElementById(id);
  let pending = null, last = null;
  function tab(t){
    root.querySelectorAll('.au-tabs [data-au-tab]').forEach(b => b.classList.toggle('on', b.dataset.auTab === t));
    $('auReg').hidden = t !== 'reg'; $('auLogin').hidden = t !== 'login'; $('auReset').hidden = t !== 'reset';
    root.querySelector('.au-tabs').hidden = t === 'reset';
    $('auT').textContent = t === 'reset' ? 'איפוס סיסמה' : 'האזור האישי';
    root.querySelectorAll('.au-err,.au-e,.au-ok').forEach(x => x.textContent = ''); root.querySelectorAll('.bad').forEach(x => x.classList.remove('bad'));
    const f = root.querySelector('form:not([hidden]) input'); if (f) setTimeout(() => f.focus(), 30);
  }
  function showErrs(map, firstMsgEl){
    root.querySelectorAll('.au-e').forEach(x => x.textContent = ''); root.querySelectorAll('.bad').forEach(x => x.classList.remove('bad'));
    const ids = {name:'auName', username:'auUser', pw:'auPw', pw2:'auPw2', idn:'auId', dob:'auDob', phone:'auPhone', email:'auMail'};
    Object.entries(map).forEach(([k, m]) => { const id = ids[k]; const e = root.querySelector('[data-e="' + id + '"]'); if (e) e.textContent = m; if ($(id)) $(id).classList.add('bad'); });
    const b = root.querySelector('.bad'); if (b) b.focus();
  }
  function open(reason, cb, startTab){
    pending = cb || null; last = document.activeElement;
    const m = get(); let sn = '', sp = ''; try { sn = sessionStorage.getItem('ccc_name') || ''; sp = sessionStorage.getItem('ccc_phone') || ''; } catch(e){}
    $('auName').value = m.name || sn; $('auPhone').value = m.phone || sp; $('auCity').value = m.city || ''; $('auMail').value = m.email || '';
    $('auId').value = m.idn || ''; $('auDob').value = m.dob || ''; $('auUser').value = m.username || '';
    $('auDob').max = ymd(yearsAgo(18)); $('auDob').min = ymd(yearsAgo(100));
    $('auSub').textContent = reason || 'פתחו חשבון פעם אחת, ותוכלו לשמור רכבים בסל, לשלוח בקשות ולעקוב אחריהן.';
    root.hidden = false; document.documentElement.style.overflow = 'hidden';
    tab(startTab || (hasAccount() ? 'login' : 'reg'));
    if (hasAccount()) $('cuLUser').value = m.email || '';
  }
  function close(){ root.hidden = true; document.documentElement.style.overflow = ''; pending = null; if (last && last.focus) last.focus(); }
  function done(){ const cb = pending; pending = null; root.hidden = true; document.documentElement.style.overflow = ''; document.dispatchEvent(new CustomEvent('ccc-signed-in')); if (cb) cb(); }
  root.addEventListener('click', e => {
    if (e.target.closest('[data-au-close]')) return close();
    const t = e.target.closest('[data-au-tab]'); if (t) return tab(t.dataset.auTab);
    if (e.target.closest('#cuForgot')) return tab('reset');
  });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !root.hidden) close(); });
  root.addEventListener('input', e => { if (e.target.classList) e.target.classList.remove('bad'); const x = root.querySelector('[data-e="' + e.target.id + '"]'); if (x) x.textContent = ''; });

  $('auReg').addEventListener('submit', async e => {
    e.preventDefault();
    const f = {name: $('auName').value.trim().replace(/\s+/g,' ').slice(0,60), username: $('auUser').value.trim(), pw: $('auPw').value, pw2: $('auPw2').value,
      idn: digits($('auId').value), dob: $('auDob').value, phone: digits($('auPhone').value).replace(/^972/,'0'), email: $('auMail').value.trim().toLowerCase(), city: $('auCity').value.trim().slice(0,40)};
    const errs = checkFields(f, true); $('auErr').textContent = '';
    if (Object.keys(errs).length){ showErrs(errs); return; }
    if (!$('auOk').checked){ $('auErr').textContent = 'צריך לאשר את שמירת הפרטים.'; return; }
    const btn = e.submitter || $('auReg').querySelector('[type=submit]'); btn.disabled = true;
    try { acct = await cccFb.customerRegister(f.email, f.pw); }
    catch(err){ btn.disabled = false; $('auErr').textContent = fbErr(err && err.code); return; }
    const m = {name: f.name, username: f.username, phone: f.phone, email: f.email, city: f.city};
    put(m);
    if (window.cccLead) await window.cccLead({src:'me', name: m.name, phone: m.phone, city: m.city, profile: {username: f.username, idn: f.idn.padStart(9,'0'), dob: f.dob, email: f.email}, detail: 'פתח חשבון באזור האישי (' + f.email + ')'});
    $('auPw').value = $('auPw2').value = ''; btn.disabled = false; done();
  });
  $('auLogin').addEventListener('submit', async e => {
    e.preventDefault(); const em = $('cuLUser').value.trim().toLowerCase(), pw = $('cuLPw').value; $('cuLErr').textContent = '';
    if (!mailOk(em)){ $('cuLErr').textContent = 'הזינו את כתובת האימייל של החשבון.'; return; }
    const btn = $('auLogin').querySelector('[type=submit]'); btn.disabled = true;
    try { acct = await cccFb.signIn(em, pw); }
    catch(err){
      // an account that so far lived only in this browser: move it to Firebase with the same password
      const m = get();
      if (m.hash && (String(m.email || '').toLowerCase() === em || String(m.username || '').toLowerCase() === em) && await hashPw(pw, m.salt) === m.hash){
        try { acct = await cccFb.customerRegister(m.email || em, pw);
          if (window.cccLead) await window.cccLead({src:'me', name: m.name, phone: m.phone, city: m.city, profile: {username: m.username || '', idn: m.idn || '', dob: m.dob || '', email: m.email || em}, detail: 'החשבון הועבר מהדפדפן למערכת'});
          put(keepLocal(m));
        } catch(err2){ btn.disabled = false; $('cuLErr').textContent = fbErr(err2 && err2.code); return; }
      } else { btn.disabled = false; $('cuLErr').textContent = fbErr(err && err.code); return; }
    }
    btn.disabled = false; $('cuLPw').value = ''; await pullProfile(); done();
  });
  $('auReset').addEventListener('submit', async e => {
    e.preventDefault(); $('cuRErr').textContent = ''; $('cuROk').textContent = '';
    const em = $('cuRMail').value.trim().toLowerCase(); if (!mailOk(em)){ $('cuRErr').textContent = 'הזינו כתובת אימייל תקינה.'; return; }
    try { await cccFb.resetPassword(em); $('cuROk').textContent = 'אם קיים חשבון עם האימייל הזה, נשלח אליו קישור לבחירת סיסמה חדשה. בדקו גם בתיקיית הספאם.'; }
    catch(err){ $('cuRErr').textContent = err && err.code === 'auth/user-not-found' ? 'אם קיים חשבון עם האימייל הזה, נשלח אליו קישור.' : fbErr(err && err.code); }
  });

  window.cccAuth = {get, put, signedIn, hasAccount, unlocked, setUnlocked, checkFields, setPassword, hashPw, profileOf, idOk, mailOk, phoneOk, userOk, age, ymd, yearsAgo,
    ready, user: () => acct,
    open, require(reason, cb){ ready.then(() => { if (acct) cb(); else open(reason, cb); }); },
    async signOut(){ try { await cccFb.signOut(); } catch(e) {} acct = null; try { ['ccc_me','ccc_cart','ccc_reqs'].forEach(k => localStorage.removeItem(k)); sessionStorage.removeItem('ccc_name'); sessionStorage.removeItem('ccc_phone'); } catch(e) {} document.dispatchEvent(new CustomEvent('ccc-signed-out')); }};
  // remove sensitive leftovers of old browser-only accounts once the account is in Firebase
  ready.then(() => { if (acct){ const m = get(); if (m.hash || m.idn || m.dob) put(keepLocal(m)); } });
})();
