// CRECE+ Suite · capa de autenticación (Supabase + Google)
// Protege toda la suite y aplica gating por rol (vendedor / admin).
(function () {
  var cfg = window.CRECE_SB || {};
  var sb;
  try {
    sb = window.supabase.createClient(cfg.url, cfg.key, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    });
  } catch (e) { console.error('No se pudo iniciar Supabase', e); }
  window.__creceSB = sb;

  var gate = document.getElementById('auth-gate');
  var box = document.getElementById('auth-box');

  function render(html) { if (box) box.innerHTML = html; if (gate) gate.style.display = 'flex'; }
  function hideGate() { if (gate) gate.style.display = 'none'; }

  function login() {
    sb.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: location.href.split('#')[0] }
    });
  }
  function logout() { sb.auth.signOut().then(function () { location.reload(); }); }
  window.creceLogout = logout;

  function showLogin() {
    render(
      '<div class="ag-logo">CRECE<sup>+</sup></div>' +
      '<div class="ag-sub">Suite Comercial</div>' +
      '<p class="ag-txt">Accede con tu correo corporativo autorizado.</p>' +
      '<button id="ag-login" class="ag-btn"><span class="ag-g">G</span> Entrar con Google</button>'
    );
    var b = document.getElementById('ag-login'); if (b) b.onclick = login;
  }

  function showDenied(email) {
    render(
      '<div class="ag-logo">CRECE<sup>+</sup></div>' +
      '<h2 class="ag-h">Acceso no autorizado</h2>' +
      '<p class="ag-txt">El correo <b>' + (email || '') + '</b> no está habilitado para la suite. ' +
      'Contacta al administrador para que te dé acceso.</p>' +
      '<button id="ag-out" class="ag-btn alt">Cerrar sesión</button>'
    );
    var b = document.getElementById('ag-out'); if (b) b.onclick = logout;
  }

  function applyRole(perfil) {
    hideGate();
    var foot = document.querySelector('.side-foot');
    if (foot) {
      foot.innerHTML =
        '<div class="user-badge"><div class="ub-email">' + perfil.email + '</div>' +
        '<div class="ub-rol">' + perfil.rol + (perfil.pais ? (' · ' + String(perfil.pais).toUpperCase()) : '') + '</div></div>' +
        '<button class="logout-btn" onclick="creceLogout()">Cerrar sesión</button>';
    }
    if (perfil.rol !== 'admin') {
      document.querySelectorAll('.nav-item').forEach(function (b) {
        if (b.dataset.t !== 'comis') b.style.display = 'none';
      });
      var comis = document.querySelector('.nav-item[data-t="comis"]');
      if (comis) comis.click();
    }
  }

  async function boot() {
    if (!sb) { render('<p class="ag-txt">No se pudo cargar la autenticación. Recarga la página.</p>'); return; }
    var sess = (await sb.auth.getSession()).data.session;
    if (!sess) { showLogin(); return; }
    var res = await sb.from('perfiles').select('*').eq('id', sess.user.id).maybeSingle();
    if (res.error) { showDenied(sess.user.email); return; }
    if (!res.data) { showDenied(sess.user.email); return; }
    applyRole(res.data);
  }
  boot();
})();
