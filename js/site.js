/* ============================================================
   Norxten — site.js
   Shared nav, footer, EN/FR toggle, scroll effects
   ============================================================ */

// ── Translations ─────────────────────────────────────────────
const T = {
  en: {
    nav_home: "Home", nav_about: "About", nav_products: "Products",
    nav_support: "Support", nav_contact: "Contact",
    nav_cta: "Learn More",
    footer_tagline: "Building foundational technology platforms.",
    footer_company: "Company", footer_product: "Product", footer_legal: "Legal", footer_support: "Support",
    footer_home: "Home", footer_about: "About", footer_products: "Products",
    footer_core: "Norxten Core", footer_privacy: "Privacy Policy",
    footer_terms: "Terms of Service", footer_contact: "Contact",
    footer_support_link: "Support",
    footer_copy: "© 2026 Norxten Technologies Inc. All rights reserved.",
    footer_legal_name: "Norxten Technologies Inc. — Quebec, Canada",
  },
  fr: {
    nav_home: "Accueil", nav_about: "À propos", nav_products: "Produits",
    nav_support: "Assistance", nav_contact: "Contact",
    nav_cta: "En savoir plus",
    footer_tagline: "Construire des plateformes technologiques fondamentales.",
    footer_company: "Entreprise", footer_product: "Produit", footer_legal: "Légal", footer_support: "Assistance",
    footer_home: "Accueil", footer_about: "À propos", footer_products: "Produits",
    footer_core: "Norxten Core", footer_privacy: "Politique de confidentialité",
    footer_terms: "Conditions d'utilisation", footer_contact: "Contact",
    footer_support_link: "Assistance",
    footer_copy: "© 2026 Norxten Technologies Inc. Tous droits réservés.",
    footer_legal_name: "Norxten Technologies Inc. — Québec, Canada",
  }
};

// ── Language detection & storage ─────────────────────────────
function detectLang() {
  const stored = localStorage.getItem('nx-lang');
  if (stored) return stored;
  const browser = navigator.language || 'en';
  return browser.toLowerCase().startsWith('fr') ? 'fr' : 'en';
}
let currentLang = detectLang();

function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('nx-lang', lang);
  document.documentElement.lang = lang;
  // update all [data-i18n] elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (T[lang][key] !== undefined) el.textContent = T[lang][key];
  });
  // update lang toggle buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  // fire custom event for page-specific translations
  document.dispatchEvent(new CustomEvent('langchange', { detail: lang }));
}

// ── Inject Nav ────────────────────────────────────────────────
function injectNav(activePage) {
  const base = getBase();
  const nav = document.createElement('nav');
  nav.id = 'site-nav';
  nav.innerHTML = `
    <div class="container nav-inner">
      <a class="nav-logo" href="${base}index.html">
        <img src="${base}assets/logo.png" alt="Norxten">
      </a>
      <ul class="nav-links">
        <li><a href="${base}index.html" data-i18n="nav_home" data-page="home">Home</a></li>
        <li><a href="${base}about.html" data-i18n="nav_about" data-page="about">About</a></li>
        <li><a href="${base}products.html" data-i18n="nav_products" data-page="products">Products</a></li>
        <li><a href="${base}support.html" data-i18n="nav_support" data-page="support">Support</a></li>
        <li><a href="${base}contact.html" data-i18n="nav_contact" data-page="contact">Contact</a></li>
      </ul>
      <div class="nav-actions">
        <div class="lang-toggle">
          <button class="lang-btn" data-lang="en">EN</button>
          <button class="lang-btn" data-lang="fr">FR</button>
        </div>
        <a href="${base}norxten-core.html" class="btn btn-primary btn-sm" data-i18n="nav_cta">Learn More</a>
      </div>
      <button class="nav-hamburger" aria-label="Menu" onclick="toggleDrawer()">
        <span></span><span></span><span></span>
      </button>
    </div>
    <div class="nav-drawer" id="nav-drawer">
      <ul>
        <li><a href="${base}index.html" data-i18n="nav_home">Home</a></li>
        <li><a href="${base}about.html" data-i18n="nav_about">About</a></li>
        <li><a href="${base}products.html" data-i18n="nav_products">Products</a></li>
        <li><a href="${base}support.html" data-i18n="nav_support">Support</a></li>
        <li><a href="${base}contact.html" data-i18n="nav_contact">Contact</a></li>
      </ul>
      <div class="drawer-actions">
        <a href="${base}norxten-core.html" class="btn btn-primary" data-i18n="nav_cta">Learn More</a>
        <div class="lang-toggle" style="align-self:flex-start;">
          <button class="lang-btn" data-lang="en">EN</button>
          <button class="lang-btn" data-lang="fr">FR</button>
        </div>
      </div>
    </div>
  `;
  document.body.prepend(nav);

  // mark active
  nav.querySelectorAll('[data-page]').forEach(a => {
    if (a.dataset.page === activePage) a.classList.add('active');
  });

  // lang buttons
  nav.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLang(btn.dataset.lang));
  });

  // scroll effect
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 10);
  }, { passive: true });
}

function toggleDrawer() {
  document.getElementById('nav-drawer').classList.toggle('open');
}

// ── Inject Footer ─────────────────────────────────────────────
function injectFooter() {
  const base = getBase();
  const footer = document.createElement('footer');
  footer.id = 'site-footer';
  footer.innerHTML = `
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="${base}assets/logo.png" alt="Norxten">
          <p data-i18n="footer_tagline">Building foundational technology platforms.</p>
        </div>
        <div class="footer-col">
          <h5 data-i18n="footer_company">Company</h5>
          <ul>
            <li><a href="${base}index.html" data-i18n="footer_home">Home</a></li>
            <li><a href="${base}about.html" data-i18n="footer_about">About</a></li>
            <li><a href="${base}contact.html" data-i18n="footer_contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5 data-i18n="footer_product">Product</h5>
          <ul>
            <li><a href="${base}products.html" data-i18n="footer_products">Products</a></li>
            <li><a href="${base}norxten-core.html" data-i18n="footer_core">Norxten Core</a></li>
            <li><a href="${base}support.html" data-i18n="footer_support_link">Support</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5 data-i18n="footer_legal">Legal</h5>
          <ul>
            <li><a href="${base}privacy.html" data-i18n="footer_privacy">Privacy Policy</a></li>
            <li><a href="${base}terms.html" data-i18n="footer_terms">Terms of Service</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span data-i18n="footer_copy">© 2026 Norxten Technologies Inc. All rights reserved.</span>
        <span data-i18n="footer_legal_name">Norxten Technologies Inc. — Quebec, Canada</span>
        <a href="mailto:info@norxten.com">info@norxten.com</a>
      </div>
    </div>
  `;
  document.body.appendChild(footer);
}

// ── Helpers ───────────────────────────────────────────────────
function getBase() {
  // figure out relative path back to site root
  const path = window.location.pathname;
  if (path.includes('/products/')) return '../';
  return './';
}

// ── Init ──────────────────────────────────────────────────────
function siteInit(activePage) {
  injectNav(activePage);
  injectFooter();
  setLang(currentLang);
}

// Pricing helpers — used on index.html and norxten-core.html
const PRICES = {
  CAD: { starter: { mo: 49.99, yr: 499.90 }, field: { mo: 89.99, yr: 899.90 }, pro: { mo: 189.99, yr: 1899.90 } },
  USD: { starter: { mo: 36.99, yr: 369.90 }, field: { mo: 66.99, yr: 669.90 }, pro: { mo: 139.99, yr: 1399.90 } }
};
