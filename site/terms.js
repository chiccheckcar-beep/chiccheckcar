/* ChicCheckCar deal terms: one source for every page (catalog cards, car page, finance calculator, personal area).
   Owner's rules, 2026-10-21. Change the numbers here only. */
(function(){
  const T = {
    rate: 5.9,      // annual nominal interest, %
    months: 60,     // number of monthly payments
    balloon: 50     // balloon at the end, % of the car price
  };
  // Down payment tiers. Paid on top of the car price (not part of it).
  // Only a fully electric car ("חשמלי") uses the electric column; hybrid / plug-in hybrid / mild hybrid count as non-electric.
  const TIERS = [
    {max: 200000, fuel: 9900,  ev: 9900},
    {max: 300000, fuel: 14900, ev: 16900},
    {max: 400000, fuel: 16900, ev: 19000}
  ];
  const TOP = 24900; // above 400,000, commercial vehicles and Toyota Land Cruiser
  const isEV = c => (c && c.fuel) === 'חשמלי';
  const isCommercial = c => !!c && (c.cat === 'מסחרי' || /מסחרי/.test(c.model || ''));
  const isLandCruiser = c => !!c && c.maker === 'טויוטה' && /לנד\s*קרוזר|land\s*cruiser/i.test(c.model || '');
  // c = {price, fuel, cat, model, maker}; returns the down payment in NIS
  function downOf(c){
    const p = +c.price || 0;
    if (isCommercial(c) || isLandCruiser(c) || p > 400000) return TOP;
    const t = TIERS.find(t => p <= t.max);
    return isEV(c) ? t.ev : t.fuel;
  }
  // Monthly payment: the full car price is financed (the down payment is paid separately on top of it).
  // Annual nominal rate / 12 per month, 60 equal monthly payments, and a balloon of 50% of the price
  // paid together with the last payment. No fees, insurance or registration costs are included.
  function quote(price){
    price = Math.max(0, +price || 0);
    const r = T.rate / 100 / 12, n = T.months, B = price * T.balloon / 100;
    const pay = price > 0 ? (r === 0 ? (price - B) / n : (price - B / Math.pow(1 + r, n)) * r / (1 - Math.pow(1 + r, -n))) : 0;
    const total = pay * n + B;
    return {price, monthly: pay, balloon: B, months: n, rate: T.rate, total, interest: Math.max(0, total - price)};
  }
  window.CCC_TERMS = Object.assign({}, T, {TIERS, TOP, isEV, isCommercial, isLandCruiser, downOf, quote,
    monthlyOf: price => quote(price).monthly,
    method: 'ריבית שנתית נומינלית 5.9% (0.4917% לחודש), 60 תשלומים חודשיים שווים לפי לוח שפיצר, על מלוא מחיר הרכב. בלון של 50% ממחיר הרכב משולם עם התשלום האחרון. המקדמה משולמת בנוסף ואינה מקטינה את סכום המימון. לא כולל עמלות, ביטוח ואגרות.'});
})();

// 2026-10-25: catalog prices were rounded up to the next thousand. Saved carts store "maker|model|trim|price" keys,
// so update old keys once to the rounded price (otherwise those cars would drop out of the customer's cart).
try {
  const cart = JSON.parse(localStorage.getItem('ccc_cart') || '[]');
  if (Array.isArray(cart)) {
    const fixed = cart.map(k => { const p = String(k).split('|'); const n = +p[p.length - 1];
      if (p.length >= 4 && n > 0 && n % 1000) { p[p.length - 1] = String(Math.ceil(n / 1000) * 1000); return p.join('|'); } return k; });
    if (fixed.some((k, i) => k !== cart[i])) localStorage.setItem('ccc_cart', JSON.stringify(fixed));
  }
} catch (e) {}
