import os, re

# This script adds language persistence to all EN pages.
# When user clicks FR, we save 'fr' to localStorage.
# On every EN page load, we check localStorage and redirect to fr/ if needed.
# On every FR page load, we save 'fr' to localStorage.
# On EN pages, clicking EN clears the preference.

LANG_PERSIST_EN = '''
<script>
// Language persistence
(function() {
  var saved = localStorage.getItem('nx-lang');
  if (saved === 'fr') {
    var page = window.location.pathname.split('/').pop() || 'index.html';
    window.location.replace('fr/' + page);
  }
})();
</script>'''

LANG_PERSIST_FR = '''
<script>
// Language persistence
localStorage.setItem('nx-lang', 'fr');
</script>'''

LANG_CLEAR_EN = "localStorage.removeItem('nx-lang');"

en_files = ['index.html', 'about.html', 'contact.html', 'support.html', 'products.html', 'norxten-core.html']
fr_files = ['fr/index.html', 'fr/about.html', 'fr/contact.html', 'fr/support.html', 'fr/products.html', 'fr/norxten-core.html']

# Fix EN pages: add redirect script at top of body + clear on EN click
for fname in en_files:
    if not os.path.exists(fname):
        print(f"SKIP: {fname}")
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # Add persist script right after <body> tag (before nav)
    if 'Language persistence' not in c:
        c = c.replace('<body>\n', '<body>\n' + LANG_PERSIST_EN + '\n', 1)
        print(f"Added redirect script to {fname}")

    # Add localStorage.removeItem to EN button onclick
    c = re.sub(
        r'<button class="lang-btn active">EN</button>',
        '<button class="lang-btn active" onclick="localStorage.removeItem(\'nx-lang\')">EN</button>',
        c, count=1
    )

    if c != orig:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Saved {fname}")

# Fix FR pages: save 'fr' to localStorage on load
for fpath in fr_files:
    if not os.path.exists(fpath):
        print(f"SKIP: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    if 'Language persistence' not in c:
        c = c.replace('<body>\n', '<body>\n' + LANG_PERSIST_FR + '\n', 1)
        print(f"Added FR save script to {fpath}")

    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Saved {fpath}")

print("\nDone.")
