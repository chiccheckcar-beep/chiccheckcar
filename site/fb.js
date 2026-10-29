/* Firebase connection for ChicCheckCar.
   The site was built on the claude.ai runtime (window.claude.use('db' | 'user' | 'downloads')).
   This file provides the same calls on top of Firebase, so the rest of the site works unchanged.
   - db        -> Firestore (compat API: collection().doc().get/set/update/delete, onSnapshot, orderBy, limit)
   - user.id() -> Firebase Auth uid (visitors are signed in anonymously on their first request)
   - user.isOwner() -> signed in with the owner's email
   - customer accounts: cccFb.customerRegister / signIn / resetPassword (Firebase Auth email+password, same uid as the anonymous visitor)
   Who may read what is enforced by firestore.rules (in the repo root), not by this file. */
(function(){
  const CFG = {
    apiKey: "AIzaSyDTinzrK9dXX5FMsRSS1Bqzu5t8UboadVA",
    authDomain: "chiccheckcar-8003f.firebaseapp.com",
    projectId: "chiccheckcar-8003f",
    storageBucket: "chiccheckcar-8003f.firebasestorage.app",
    messagingSenderId: "825808735609",
    appId: "1:825808735609:web:cdc3104069c9effba473a8"
  };
  const OWNER = 'ankermeir2005@gmail.com';
  const BASE = 'https://www.gstatic.com/firebasejs/10.14.1/';

  const load = f => new Promise((ok, no) => {
    const s = document.createElement('script'); s.src = BASE + f; s.onload = ok; s.onerror = no; document.head.appendChild(s);
  });
  let ready = null;
  function init(){
    if (!ready) ready = (async () => {
      if (!window.firebase) await load('firebase-app-compat.js');
      if (!firebase.auth) await load('firebase-auth-compat.js');
      if (!firebase.firestore) await load('firebase-firestore-compat.js');
      if (!firebase.apps.length) firebase.initializeApp(CFG);
      const auth = firebase.auth(), db = firebase.firestore();
      await new Promise(r => { const off = auth.onAuthStateChanged(() => { off(); r(); }); });
      return {auth, db};
    })();
    ready.catch(() => { ready = null; });
    return ready;
  }
  const isOwnerUser = u => !!(u && !u.isAnonymous && String(u.email || '').toLowerCase() === OWNER);

  const user = {
    async id(){
      const {auth} = await init();
      if (!auth.currentUser) await auth.signInAnonymously();
      return auth.currentUser.uid;
    },
    async isOwner(){ const {auth} = await init(); return isOwnerUser(auth.currentUser); }
  };

  const downloads = {
    async save({filename, data}){
      const url = URL.createObjectURL(new Blob([data], {type: 'text/csv;charset=utf-8'}));
      const a = document.createElement('a'); a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
    }
  };

  // customer accounts (Firebase Auth email/password). Registering upgrades the visitor's anonymous session, so the
  // visitor keeps the same uid and their lead document (leads/<uid>) stays theirs on every device.
  async function customerRegister(email, pw){
    const {auth} = await init(); const u = auth.currentUser;
    if (u && u.isAnonymous){ const cred = firebase.auth.EmailAuthProvider.credential(email, pw); return (await u.linkWithCredential(cred)).user; }
    if (u) await auth.signOut();
    return (await auth.createUserWithEmailAndPassword(email, pw)).user;
  }
  // staff / owner sign-in used by the admin area
  // New-request e-mail to the owner through EmailJS (free plan). Empty publicKey = off. Only name, phone, car and request type
  // are sent (never ID number, income or bank). Fill these three from the owner's EmailJS account to turn it on.
  const NOTIFY = {serviceId: 'service_4exnb1g', templateId: 'template_jud24li', publicKey: 'tyUlM4P6Ih7wbUt7D'};
  window.cccFb = {
    OWNER, CFG, NOTIFY, init, isOwnerUser, customerRegister,
    async resetPassword(email){ const {auth} = await init(); auth.languageCode = 'he'; await auth.sendPasswordResetEmail(email); },
    async onAuth(cb){ const {auth} = await init(); return auth.onAuthStateChanged(cb); },
    async current(){ const {auth} = await init(); return auth.currentUser; },
    async signIn(email, pw){ const {auth} = await init(); return (await auth.signInWithEmailAndPassword(email, pw)).user; },
    async signUp(email, pw){ const {auth} = await init(); return (await auth.createUserWithEmailAndPassword(email, pw)).user; },
    async signOut(){ const {auth} = await init(); await auth.signOut(); }
  };

  window.claude = {
    async use(kind){
      if (kind === 'db') return (await init()).db;
      if (kind === 'user'){ await init(); return user; }
      if (kind === 'downloads') return downloads;
      return null;
    }
  };
})();
