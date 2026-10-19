/* ChicCheckCar — customer account (registration, sign-in, password reset). Shared by index.html, car.html and me.html.
   The account lives in this browser (localStorage "ccc_me"). The password is stored only as a PBKDF2 hash and is never sent anywhere.
   Password reset is verified with ID number + date of birth (SMS is not available on this hosting). */
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
  const hasAccount = () => { const m = get(); return !!(m.username && m.hash); };
  const unlocked = () => { try { return sessionStorage.getItem('ccc_unlocked') === '1'; } catch(e){ return false; } };
  const setUnlocked = v => { try { v ? sessionStorage.setItem('ccc_unlocked','1') : sessionStorage.removeItem('ccc_unlocked'); } catch(e){} };
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
    <span class="au-logo" role="img" aria-label="ChicCheckCar"></span>
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
      <label class="au-ck"><input type="checkbox" id="auOk"><span>אני מאשר/ת ש-ChicCheckCar תשמור את הפרטים ותחזור אליי בנוגע לרכבים שבחרתי. <a href="index.html#privacy" target="_blank" rel="noopener">מדיניות הפרטיות</a></span></label>
      <p class="au-err" id="auErr" role="alert"></p>
      <button type="submit" class="au-go">פתיחת חשבון והמשך</button>
    </form>
    <form id="auLogin" novalidate hidden>
      ${F('cuLUser','שם משתמש','dir="ltr" autocomplete="username" autocapitalize="off" spellcheck="false"')}
      ${F('cuLPw','סיסמה','type="password" dir="ltr" autocomplete="current-password"')}
      <p class="au-err" id="cuLErr" role="alert"></p>
      <button type="submit" class="au-go">כניסה</button>
      <button type="button" class="au-link" id="cuForgot">שכחתי סיסמה</button>
    </form>
    <form id="auReset" novalidate hidden>
      <p class="au-sub" style="margin:0">לאיפוס הסיסמה, אמתו את הזהות שלכם עם הפרטים ששמרתם בחשבון.</p>
      ${F('cuRId','תעודת זהות','inputmode="numeric" dir="ltr" maxlength="9" autocomplete="off"')}
      ${F('cuRDob','תאריך לידה','type="date" dir="ltr"')}
      <div class="au-two"><div>${F('cuRPw','סיסמה חדשה','type="password" dir="ltr" autocomplete="new-password"','(8+ תווים)')}</div><div>${F('cuRPw2','אימות סיסמה','type="password" dir="ltr" autocomplete="new-password"')}</div></div>
      <p class="au-err" id="cuRErr" role="alert"></p><p class="au-ok" id="cuROk" role="status"></p>
      <button type="submit" class="au-go">איפוס הסיסמה</button>
      <button type="button" class="au-link" data-au-tab="login">חזרה לכניסה</button>
    </form>
    <p class="au-note">החשבון נשמר בדפדפן הזה. הסיסמה נשמרת מוצפנת ולא נשלחת לשום מקום.</p>
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
    $('auDob').max = ymd(yearsAgo(18)); $('auDob').min = ymd(yearsAgo(100)); $('cuRDob').max = $('auDob').max;
    $('auSub').textContent = reason || 'פתחו חשבון פעם אחת, ותוכלו לשמור רכבים בסל, לשלוח בקשות ולעקוב אחריהן.';
    root.hidden = false; document.documentElement.style.overflow = 'hidden';
    tab(startTab || (hasAccount() ? 'login' : 'reg'));
    if (hasAccount()) $('cuLUser').value = m.username;
  }
  function close(){ root.hidden = true; document.documentElement.style.overflow = ''; pending = null; if (last && last.focus) last.focus(); }
  function done(){ const cb = pending; pending = null; root.hidden = true; document.documentElement.style.overflow = ''; setUnlocked(true); document.dispatchEvent(new CustomEvent('ccc-signed-in')); if (cb) cb(); }
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
    const m = Object.assign(get(), {name: f.name, username: f.username, idn: f.idn.padStart(9,'0'), dob: f.dob, phone: f.phone, email: f.email, city: f.city});
    await setPassword(m, f.pw); put(m);
    if (window.cccLead) window.cccLead({src:'me', name: m.name, phone: m.phone, city: m.city, profile: profileOf(m), detail: 'פתח חשבון באזור האישי (שם משתמש: ' + m.username + ')'});
    $('auPw').value = $('auPw2').value = ''; done();
  });
  $('auLogin').addEventListener('submit', async e => {
    e.preventDefault(); const m = get(), u = $('cuLUser').value.trim(), pw = $('cuLPw').value;
    if (!m.hash){ $('cuLErr').textContent = 'לא נמצא חשבון בדפדפן הזה. פתחו חשבון חדש.'; return; }
    if (u.toLowerCase() !== String(m.username).toLowerCase() || await hashPw(pw, m.salt) !== m.hash){ $('cuLErr').textContent = 'שם המשתמש או הסיסמה שגויים.'; return; }
    $('cuLPw').value = ''; done();
  });
  $('auReset').addEventListener('submit', async e => {
    e.preventDefault(); const m = get(); $('cuRErr').textContent = ''; $('cuROk').textContent = '';
    if (!m.hash){ $('cuRErr').textContent = 'לא נמצא חשבון בדפדפן הזה.'; return; }
    if (digits($('cuRId').value).padStart(9,'0') !== m.idn || $('cuRDob').value !== m.dob){ $('cuRErr').textContent = 'תעודת הזהות או תאריך הלידה לא תואמים לחשבון.'; return; }
    const pw = $('cuRPw').value, pw2 = $('cuRPw2').value;
    if (pw.length < 8 || !/\d/.test(pw) || !/[A-Za-zא-ת]/.test(pw)){ $('cuRErr').textContent = 'סיסמה: לפחות 8 תווים, עם אותיות וספרות.'; return; }
    if (pw !== pw2){ $('cuRErr').textContent = 'הסיסמאות לא תואמות.'; return; }
    await setPassword(m, pw); put(m); $('cuRPw').value = $('cuRPw2').value = '';
    $('cuROk').textContent = 'הסיסמה עודכנה. אפשר להיכנס עם הסיסמה החדשה.'; setTimeout(() => { tab('login'); $('cuLUser').value = m.username; }, 1200);
  });

  window.cccAuth = {get, put, signedIn, hasAccount, unlocked, setUnlocked, checkFields, setPassword, hashPw, profileOf, idOk, mailOk, phoneOk, userOk, age, ymd, yearsAgo,
    open, require(reason, cb){ if (hasAccount() && unlocked()) cb(); else open(reason, cb); },
    signOut(){ setUnlocked(false); document.dispatchEvent(new CustomEvent('ccc-signed-out')); }};
})();
