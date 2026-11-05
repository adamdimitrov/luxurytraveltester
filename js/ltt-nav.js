/* ==========================================================================
   LUXURY TRAVEL TESTER — MODERN VANILLA NAVIGATION CONTROLLER
   Zero-dependency, semantic, responsive, WCAG-compliant (Desktop & Mobile)
   ========================================================================== */
(function() {
  function initNav() {
    var toggle = document.getElementById('lttNavToggle');
    var drawer = document.getElementById('lttMobileDrawer');
    var dropdown = document.getElementById('lttExploreDropdown');
    var dropBtn = dropdown ? dropdown.querySelector('.ltt-dropdown-btn') : null;

    if (toggle && drawer) {
      toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        var isOpen = drawer.classList.contains('is-open');
        if (isOpen) {
          drawer.classList.remove('is-open');
          toggle.classList.remove('is-active');
          toggle.setAttribute('aria-expanded', 'false');
          drawer.setAttribute('aria-hidden', 'true');
        } else {
          drawer.classList.add('is-open');
          toggle.classList.add('is-active');
          toggle.setAttribute('aria-expanded', 'true');
          drawer.setAttribute('aria-hidden', 'false');
        }
      });

      drawer.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
          drawer.classList.remove('is-open');
          toggle.classList.remove('is-active');
          toggle.setAttribute('aria-expanded', 'false');
          drawer.setAttribute('aria-hidden', 'true');
        });
      });
    }

    if (dropBtn && dropdown) {
      dropBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        var open = dropdown.classList.toggle('is-open');
        dropBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    document.addEventListener('click', function(e) {
      if (drawer && drawer.classList.contains('is-open') && !drawer.contains(e.target) && (!toggle || !toggle.contains(e.target))) {
        drawer.classList.remove('is-open');
        if (toggle) {
          toggle.classList.remove('is-active');
          toggle.setAttribute('aria-expanded', 'false');
        }
        drawer.setAttribute('aria-hidden', 'true');
      }
      if (dropdown && dropdown.classList.contains('is-open') && !dropdown.contains(e.target)) {
        dropdown.classList.remove('is-open');
        if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        if (drawer && drawer.classList.contains('is-open')) {
          drawer.classList.remove('is-open');
          if (toggle) {
            toggle.classList.remove('is-active');
            toggle.setAttribute('aria-expanded', 'false');
          }
          drawer.setAttribute('aria-hidden', 'true');
        }
        if (dropdown && dropdown.classList.contains('is-open')) {
          dropdown.classList.remove('is-open');
          if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNav);
  } else {
    initNav();
  }
})();
