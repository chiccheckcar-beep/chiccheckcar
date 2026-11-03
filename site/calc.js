/* Chick Chack Car — finance calculator (owner, 2026-11-03, "exactly like the picture", 3.9%).
   One component for the home page and every car page: trim, route (balloon 50% / no balloon), term (60 / 100 months),
   down payment slider (0 to 50% of the price, lowers the financed amount). Rate and balloon come from terms.js.
   window.cccCalc.mount(el, {cars: CARS, ix: [CARS indexes of one model], sel: index, onLead(info), onLoan(info), onTrim(i)}) */
(function(){
  const T = () => window.CCC_TERMS;
  const nis = n => '₪' + Math.round(n).toLocaleString('he-IL');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const full = c => [c.maker, c.model, c.trim].filter(Boolean).join(' ');
  const MONTHS = [60, 100];

  function css(){
    if (document.getElementById('ccCalcCss')) return;
    const s = document.createElement('style'); s.id = 'ccCalcCss';
    s.textContent = `
.ccl{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:22px;align-items:start;max-width:1000px;margin:0 auto;font-family:Heebo,system-ui,"Segoe UI",Arial,sans-serif;color:#1f1519;text-align:right}
.ccl-box{background:#fff;border-radius:22px;padding:24px;box-shadow:0 14px 34px rgba(31,21,25,.08);border:1px solid rgba(122,42,74,.08)}
.ccl-in{display:flex;flex-direction:column;gap:20px}
.ccl-h{font-size:16px;font-weight:800;margin:0 0 10px}
.ccl-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.ccl-opt{display:flex;flex-direction:column;align-items:flex-start;gap:3px;text-align:right;border:1.5px solid #e6dde0;background:#fff;border-radius:14px;padding:12px 14px;font:inherit;color:#1f1519;cursor:pointer;transition:border-color .15s,background .15s}
.ccl-opt b{font-size:15px;font-weight:800}
.ccl-opt small{font-size:13px;color:#6a5a60;font-weight:600}
.ccl-opt:hover{border-color:#c9a7b6}
.ccl-opt[aria-pressed="true"]{border-color:#7a2a4a;background:#f9f1f5}
.ccl-opt[aria-pressed="true"] b,.ccl-opt[aria-pressed="true"] small.p{color:#7a2a4a}
.ccl-seg{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.ccl-seg .ccl-opt{align-items:center;text-align:center}
.ccl-seg .ccl-opt[aria-pressed="true"]{background:#7a2a4a;border-color:#7a2a4a}
.ccl-seg .ccl-opt[aria-pressed="true"] b{color:#fff}
.ccl-dn{display:flex;justify-content:space-between;align-items:baseline}
.ccl-dn output{font-weight:800;color:#7a2a4a;font-variant-numeric:tabular-nums}
.ccl-range{width:100%;accent-color:#7a2a4a;height:28px;margin:6px 0 0}
.ccl-scale{display:flex;justify-content:space-between;font-size:12.5px;color:#6a5a60}
.ccl-out{position:sticky;top:16px;display:flex;flex-direction:column;gap:14px}
.ccl-lbl{font-size:15px;font-weight:700;color:#6a5a60}
.ccl-big{font-family:"Unbounded",system-ui,"Segoe UI",Arial,sans-serif;font-weight:700;font-size:clamp(34px,4.4vw,48px);line-height:1;color:#7a2a4a;font-variant-numeric:tabular-nums;direction:ltr;text-align:right}
.ccl-big small{font-size:.5em;margin-inline-end:4px}
.ccl-dl{display:grid;grid-template-columns:1fr auto;gap:9px 14px;margin:0;padding-top:14px;border-top:1px solid #eee4e8;font-size:15px}
.ccl-dl dt{color:#6a5a60}.ccl-dl dd{margin:0;font-weight:800;text-align:left;direction:ltr;font-variant-numeric:tabular-nums}
.ccl-dl dd.t{direction:rtl}
.ccl-wa,.ccl-elig{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;border-radius:12px;padding:14px;font:inherit;font-size:16px;font-weight:800;text-decoration:none;cursor:pointer}
.ccl-wa{background:#25d366;color:#fff;border:0}
.ccl-wa:hover{background:#1ebe5b}
.ccl-elig{background:#fff;color:#1f1519;border:1.5px solid #d9cdd2}
.ccl-elig:hover{border-color:#7a2a4a}
.ccl-note{font-size:12px;color:#6a5a60;line-height:1.6;margin:0}
@media (max-width:820px){.ccl{grid-template-columns:1fr}.ccl-out{position:static}.ccl-box{padding:18px}}`;
    document.head.appendChild(s);
  }

  function mount(root, opt){
    css();
    const CARS = opt.cars || [];
    const st = {ix: opt.ix, i: opt.sel != null ? opt.sel : opt.ix[0], balloon: true, months: 60, downPct: 0};
    const car = () => CARS[st.i];
    const labels = ix => ix.map(i => CARS[i].trim || CARS[i].model);
    function calc(){
      const c = car(), price = +c.price || 0, down = Math.round(price * st.downPct / 100);
      const q = T().loan({price, down, months: st.months, balloon: st.balloon});
      return {c, price, down, q};
    }
    function render(){
      const {c, price, down, q} = calc(), lb = labels(st.ix);
      root.innerHTML = `<div class="ccl">
        <div class="ccl-box ccl-in">
          ${st.ix.length > 1 ? `<div><p class="ccl-h">רמת גימור</p><div class="ccl-opts" role="group" aria-label="רמת גימור">${st.ix.map((i, k) =>
            `<button type="button" class="ccl-opt" data-cc-trim="${i}" aria-pressed="${i === st.i}"><b>${esc(lb[k])}</b><small class="p">${nis(CARS[i].price)}</small></button>`).join('')}</div></div>` : ''}
          <div><p class="ccl-h">מסלול</p><div class="ccl-opts" role="group" aria-label="מסלול">
            <button type="button" class="ccl-opt" data-cc-bal="1" aria-pressed="${st.balloon}"><b>עם בלון</b><small>החזר נמוך, ${T().balloon}% מהמחיר נשאר לסוף</small></button>
            <button type="button" class="ccl-opt" data-cc-bal="0" aria-pressed="${!st.balloon}"><b>בלי בלון</b><small>פורסים את כל הסכום, בלי יתרה בסוף</small></button>
          </div></div>
          <div><p class="ccl-h">תקופה</p><div class="ccl-seg" role="group" aria-label="תקופה">${MONTHS.map(m =>
            `<button type="button" class="ccl-opt" data-cc-m="${m}" aria-pressed="${m === st.months}"><b>${m} חודשים</b></button>`).join('')}</div></div>
          <div><div class="ccl-dn"><label class="ccl-h" for="ccDown" style="margin:0">מקדמה</label><output id="ccDownOut">${nis(down)}</output></div>
            <input class="ccl-range" id="ccDown" type="range" min="0" max="50" step="1" value="${st.downPct}" aria-valuetext="${nis(down)}">
            <div class="ccl-scale"><span>בלי מקדמה</span><span>עד 50% מהמחיר</span></div></div>
        </div>
        <div class="ccl-box ccl-out" aria-live="polite">
          <div class="ccl-lbl">החזר חודשי החל מ-</div>
          <div class="ccl-big" id="ccMonthly"><small>₪</small>${Math.ceil(q.monthly).toLocaleString('he-IL')}</div>
          <dl class="ccl-dl">
            <dt>גימור</dt><dd class="t">${esc(c.trim || c.model)}${c.fuel ? ' · ' + esc(c.fuel) : ''}</dd>
            <dt>מחיר הרכב</dt><dd>${nis(price)}</dd>
            ${down ? `<dt>מקדמה</dt><dd>${nis(down)}</dd>` : ''}
            <dt>סכום המימון</dt><dd>${nis(q.financed)}</dd>
            ${st.balloon ? `<dt>תשלום בלון בסוף</dt><dd>${nis(q.balloon)}</dd>` : ''}
            <dt>תקופה</dt><dd class="t">${st.months} חודשים · ריבית ${T().rate}%</dd>
          </dl>
          <button type="button" class="ccl-wa" data-cc-wa><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>שלחו לי הצעה עם התנאים האלה</button>
          <button type="button" class="ccl-elig" data-cc-loan>בדיקת זכאות למימון</button>
          <p class="ccl-note">החישוב להמחשה בלבד. ההחזר משוער, והתנאים הסופיים נקבעים בבדיקת מימון אישית. תנאי העסקה כפופים לאישור מימון ולהסכם העסקה.</p>
        </div></div>`;
    }
    function info(){
      const {c, price, down, q} = calc();
      return {car: full(c), c, price, down, financed: q.financed, months: st.months, balloon: st.balloon ? q.balloon : 0, monthly: Math.ceil(q.monthly), rate: T().rate,
        text: `שלום, אשמח להצעה על ${full(c)}.\nמחיר הרכב: ${nis(price)}\nמקדמה: ${nis(down)}\nמסלול: ${st.balloon ? 'עם בלון ' + T().balloon + '% (' + nis(q.balloon) + ')' : 'בלי בלון'}\nתקופה: ${st.months} חודשים\nהחזר חודשי משוער: ${nis(Math.ceil(q.monthly))}`};
    }
    root.addEventListener('click', e => {
      const t = e.target.closest('[data-cc-trim]'); if (t){ st.i = +t.dataset.ccTrim; render(); if (opt.onTrim) opt.onTrim(st.i); return; }
      const b = e.target.closest('[data-cc-bal]'); if (b){ st.balloon = b.dataset.ccBal === '1'; render(); return; }
      const m = e.target.closest('[data-cc-m]'); if (m){ st.months = +m.dataset.ccM; render(); return; }
      if (e.target.closest('[data-cc-wa]')){ const x = info(); window.open('https://wa.me/972545762802?text=' + encodeURIComponent(x.text), '_blank', 'noopener'); if (opt.onLead) opt.onLead(x); return; }
      if (e.target.closest('[data-cc-loan]') && opt.onLoan) opt.onLoan(info());
    });
    root.addEventListener('input', e => { if (e.target.id !== 'ccDown') return;
      st.downPct = +e.target.value; const {down, q} = calc();
      // update in place so the slider keeps focus while dragging
      root.querySelector('#ccDownOut').textContent = nis(down); e.target.setAttribute('aria-valuetext', nis(down));
      root.querySelector('#ccMonthly').innerHTML = '<small>₪</small>' + Math.ceil(q.monthly).toLocaleString('he-IL');
    });
    root.addEventListener('change', e => { if (e.target.id === 'ccDown') { render(); const r = root.querySelector('#ccDown'); if (r) r.focus(); } });
    render();
    return {set(ix, sel){ st.ix = ix; st.i = sel != null ? sel : ix[0]; render(); }, info};
  }
  window.cccCalc = {mount};
})();
