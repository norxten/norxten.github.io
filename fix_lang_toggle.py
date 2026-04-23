import os, re

# ── Fix EN pages ───────────────────────────────────────────────
# Remove localStorage lang detection, fix FR button links

en_files = ['index.html', 'about.html', 'contact.html', 'support.html', 'products.html', 'norxten-core.html']

for fname in en_files:
    if not os.path.exists(fname):
        print(f"SKIP: {fname} not found")
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # 1. Remove localStorage/setLang JS block
    c = re.sub(
        r'const T = \{[\s\S]*?setLang\(lang\);',
        '// EN page',
        c, count=1
    )
    # Also remove standalone setLang calls
    c = re.sub(r'\n// EN page — no lang switching needed', '\n// EN page', c)

    # 2. Fix FR button - remove data-lang attr, add onclick navigation
    fr_dest = f'fr/{fname}'
    # Pattern 1: data-lang button
    c = re.sub(
        r'<button class="lang-btn"[^>]*data-lang="fr"[^>]*>FR</button>',
        f'<button class="lang-btn" onclick="window.location.href=\'{fr_dest}\'">FR</button>',
        c
    )
    # Pattern 2: already has onclick but wrong dest
    c = re.sub(
        r"<button class=\"lang-btn\" onclick=\"window\.location\.href='fr/[^']*'\">FR</button>",
        f'<button class="lang-btn" onclick="window.location.href=\'{fr_dest}\'">FR</button>',
        c
    )

    # 3. Fix EN button - remove data-lang attr
    c = re.sub(
        r'<button class="lang-btn active"[^>]*data-lang="en"[^>]*>EN</button>',
        '<button class="lang-btn active">EN</button>',
        c
    )

    # 4. Remove lang-btn event listeners that might re-trigger
    c = re.sub(
        r"document\.querySelectorAll\('\.lang-btn'\)\.forEach\(b => b\.addEventListener\('click', \(\) => setLang\(b\.dataset\.lang\)\)\);",
        '',
        c
    )

    if c != orig:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Fixed: {fname}")
    else:
        print(f"No changes: {fname}")

# ── Fix FR pages ───────────────────────────────────────────────
# Fix EN button to correctly navigate back to EN page

fr_files = ['fr/index.html', 'fr/about.html', 'fr/contact.html', 'fr/support.html', 'fr/products.html', 'fr/norxten-core.html']

for fpath in fr_files:
    if not os.path.exists(fpath):
        print(f"SKIP: {fpath} not found")
        continue
    fname = os.path.basename(fpath)
    en_dest = f'../{fname}'

    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # Replace EN button onclick with correct path
    c = re.sub(
        r"<button class=\"lang-btn\" onclick=\"[^\"]*\">EN</button>",
        f'<button class="lang-btn" onclick="window.location.href=\'{en_dest}\'">EN</button>',
        c
    )

    # Also remove any enMap JS that might conflict
    c = re.sub(
        r'const enMap = \{[\s\S]*?if \(enBtn\) enBtn\.onclick[^\n]*\n',
        '',
        c, count=1
    )

    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Fixed: {fpath}")
    else:
        print(f"No changes: {fpath}")

print("\nDone. Check above for any SKIPs.")
