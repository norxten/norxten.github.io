with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find and replace the entire broken pricing JS block
old = """const __OLD = null; /* was: const PRICES */
  USD: { starter:{mo:36.99,yr:369.90}, field:{mo:66.99,yr:669.90}, pro:{mo:139.99,yr:1399.90} },
  CAD: { starter:{mo:49.99,yr:499.90}, field:{mo:89.99,yr:899.90}, pro:{mo:189.99,yr:1899.90} }
};
let currency = 'USD', billing = 'mo';
function updatePrices() {
  const p = PRICES[currency];
  const isYr = billing === 'yr';
  const sym = '$';
  const label = currency;
  document.getElementById('currency-label').textContent = label;
  const plans = [
    {id:'s', tier:'starter'},
    {id:'f', tier:'field'},
    {id:'p', tier:'pro'}
  ];
  plans.forEach(({id, tier}) => {
    const p = PRICES[tier];
    document.getElementById(id+'-sym').textContent = '$';
    if (isYr) {
      document.getElementById(id+'-amt').textContent = p.yr.toFixed(2);
      const perEl = document.getElementById(id+'-per');
      if (perEl) perEl.textContent = '/yr';
      document.getElementById(id+'-ann').textContent = 'Save $' + ((p.mo*12)-p.yr).toFixed(2) + ' \u2014 2 months free';
    } else {
      document.getElementById(id+'-amt').textContent = p.mo.toFixed(2);
      const perEl = document.getElementById(id+'-per');
      if (perEl) perEl.textContent = '/mo';
      document.getElementById(id+'-ann').textContent = ' ';
    }
  });
}
document.querySelectorAll('#billing-toggle button').forEach(btn => {
  btn.addEventListener('click', () => {
    billing = btn.dataset.val;
    document.querySelectorAll('#billing-toggle button').forEach(b => b.classList.toggle('active', b.dataset.val === billing));
    updatePrices();
  });
});
updatePrices();"""

new = """const PRICES = {
  starter: {mo: 49.99, yr: 499.90},
  field:   {mo: 89.99, yr: 899.90},
  pro:     {mo: 189.99, yr: 1899.90}
};
let billing = 'mo';
function updatePrices() {
  const isYr = billing === 'yr';
  const plans = [
    {id:'s', tier:'starter'},
    {id:'f', tier:'field'},
    {id:'p', tier:'pro'}
  ];
  plans.forEach(({id, tier}) => {
    const p = PRICES[tier];
    const symEl = document.getElementById(id+'-sym');
    const amtEl = document.getElementById(id+'-amt');
    const perEl = document.getElementById(id+'-per');
    const annEl = document.getElementById(id+'-ann');
    if (!amtEl) return;
    if (symEl) symEl.textContent = '$';
    if (isYr) {
      amtEl.textContent = p.yr.toFixed(2);
      if (perEl) perEl.textContent = '/yr';
      if (annEl) annEl.textContent = 'Save $' + ((p.mo*12)-p.yr).toFixed(2) + ' \u2014 2 months free';
    } else {
      amtEl.textContent = p.mo.toFixed(2);
      if (perEl) perEl.textContent = '/mo';
      if (annEl) annEl.textContent = '\u00a0';
    }
  });
}
document.querySelectorAll('#billing-toggle button').forEach(btn => {
  btn.addEventListener('click', () => {
    billing = btn.dataset.val;
    document.querySelectorAll('#billing-toggle button').forEach(b => b.classList.toggle('active', b.dataset.val === billing));
    updatePrices();
  });
});
updatePrices();"""

if old in c:
    c = c.replace(old, new)
    print("OK: Pricing JS replaced")
else:
    print("NOT FOUND")

# Remove USD/CAD toggle HTML
c = c.replace(
    '      <div class="toggle-group" id="currency-toggle">\n        <button class="active" data-val="USD">USD</button>\n        <button data-val="CAD">CAD</button>\n      </div>',
    ''
)
print("OK: Currency toggle HTML removed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Done")
