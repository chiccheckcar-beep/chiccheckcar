/* Maintenance switch (owner, 2026-11-09: "לעצור את האתר").
   true  = visitors see the "האתר בשדרוג" page; car pages and the personal area send them to it.
   false = the site works as usual.
   The leads center stays open for the team at index.html#admin (and the system audit at audit.html). */
window.CCC_MAINT = true;
(function(){
  if (!window.CCC_MAINT) return;
  var p = location.pathname.split('/').pop() || 'index.html';
  if (p !== 'index.html' && p !== '') { location.replace('index.html'); return; }
  var set = function(){ document.documentElement.classList.toggle('maint', !/^#admin/.test(location.hash)); };
  set(); addEventListener('hashchange', set);
})();
