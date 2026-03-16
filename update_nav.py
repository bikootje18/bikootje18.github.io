import os, re

BASE = '/Users/biko/Documents/New Website SP'

# ── NL dropdown variants ──────────────────────────────────────────────────────
def nl_dropdown(active=None):
    items = {
        'over-ons': '<a href="/over-ons.html" class="nav-active">Over ons</a>',
        'mvo':      '<a href="/mvo.html" class="nav-active">MVO</a>',
        'blog':     '<a href="/blog.html" class="nav-active">Blog</a>',
    }
    def item(key, label, href):
        cls = ' class="nav-active"' if active == key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    btn_cls = ' active' if active in ('over-ons','mvo','blog') else ''
    return (
        f'<div class="nav-dropdown">\n'
        f'          <button class="nav-dropdown-btn{btn_cls}" type="button">Over ons <span class="nav-dropdown-arrow">▾</span></button>\n'
        f'          <div class="nav-dropdown-menu">\n'
        f'            {item("over-ons","Over ons","/over-ons.html")}\n'
        f'            {item("mvo","MVO","/mvo.html")}\n'
        f'            {item("blog","Blog","/blog.html")}\n'
        f'          </div>\n'
        f'        </div>'
    )

# ── EN dropdown variants ──────────────────────────────────────────────────────
def en_dropdown(active=None):
    def item(key, label, href):
        cls = ' class="nav-active"' if active == key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    btn_cls = ' active' if active in ('about','mvo','blog') else ''
    return (
        f'<div class="nav-dropdown">\n'
        f'          <button class="nav-dropdown-btn{btn_cls}" type="button">About <span class="nav-dropdown-arrow">▾</span></button>\n'
        f'          <div class="nav-dropdown-menu">\n'
        f'            {item("about","About us","/en/about.html")}\n'
        f'            {item("mvo","CSR","/en/mvo.html")}\n'
        f'            {item("blog","Blog","/en/blog.html")}\n'
        f'          </div>\n'
        f'        </div>'
    )

# ── Mobile dropdown HTML ──────────────────────────────────────────────────────
NL_MOBILE_DD = (
    '\n    <div class="mobile-dropdown">\n'
    '      <button class="mobile-dropdown-btn" type="button" onclick="toggleMobileDropdown(this)">Over ons <span class="nav-dropdown-arrow">▾</span></button>\n'
    '      <div class="mobile-dropdown-items">\n'
    '        <a href="/over-ons.html">Over ons</a>\n'
    '        <a href="/mvo.html">MVO</a>\n'
    '        <a href="/blog.html">Blog</a>\n'
    '      </div>\n'
    '    </div>'
)

EN_MOBILE_DD = (
    '\n    <div class="mobile-dropdown">\n'
    '      <button class="mobile-dropdown-btn" type="button" onclick="toggleMobileDropdown(this)">About <span class="nav-dropdown-arrow">▾</span></button>\n'
    '      <div class="mobile-dropdown-items">\n'
    '        <a href="/en/about.html">About us</a>\n'
    '        <a href="/en/mvo.html">CSR</a>\n'
    '        <a href="/en/blog.html">Blog</a>\n'
    '      </div>\n'
    '    </div>'
)

TOGGLE_JS = '''function toggleMobileDropdown(btn) {
  btn.classList.toggle('open');
  btn.nextElementSibling.classList.toggle('open');
}'''

# ── Helpers ───────────────────────────────────────────────────────────────────
def inject_toggle_js(content):
    if 'toggleMobileDropdown' in content:
        return content
    return content.replace(
        'function toggleMenu()',
        TOGGLE_JS + '\nfunction toggleMenu()'
    )

def process_nl(filepath, active=None):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Desktop nav: remove Over ons link (with or without nav-active)
    content = re.sub(r'\n\s{8}<a href="/over-ons\.html"(?:\s+class="nav-active")?>\s*Over ons\s*</a>', '', content)

    # Desktop nav: insert dropdown before the nav-cta
    dd = nl_dropdown(active)
    content = content.replace(
        '\n        <a href="/contact.html" class="nav-cta">',
        f'\n        {dd}\n        <a href="/contact.html" class="nav-cta">'
    )

    # Mobile menu: process inside the mobile-menu div
    def fix_mobile(m):
        mob = m.group(0)
        mob = re.sub(r'<a href="/over-ons\.html">Over ons</a>', '', mob)
        mob = re.sub(
            r'(<a href="/contact\.html">Contact</a>)',
            r'\1' + NL_MOBILE_DD,
            mob
        )
        return mob
    content = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>\s*\n</nav>',
                     fix_mobile, content, flags=re.DOTALL)

    content = inject_toggle_js(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[NL] Updated: {os.path.relpath(filepath, BASE)}')


def process_en(filepath, active=None):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Desktop nav: remove About link (with or without nav-active)
    content = re.sub(r'\n\s{8}<a href="/en/about\.html"(?:\s+class="nav-active")?>\s*About\s*</a>', '', content)

    # Desktop nav: insert dropdown before the nav-cta
    dd = en_dropdown(active)
    content = content.replace(
        '\n        <a href="/en/contact.html" class="nav-cta">',
        f'\n        {dd}\n        <a href="/en/contact.html" class="nav-cta">'
    )

    # Mobile menu: process inside the mobile-menu div
    def fix_mobile(m):
        mob = m.group(0)
        mob = re.sub(r'<a href="/en/about\.html">About</a>', '', mob)
        mob = re.sub(
            r'(<a href="/en/contact\.html">Contact</a>)',
            r'\1' + EN_MOBILE_DD,
            mob
        )
        return mob
    content = re.sub(r'<div class="mobile-menu"[^>]*>.*?</div>\s*\n</nav>',
                     fix_mobile, content, flags=re.DOTALL)

    content = inject_toggle_js(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[EN] Updated: {os.path.relpath(filepath, BASE)}')


# ── File list ─────────────────────────────────────────────────────────────────
NL_FILES = [
    ('index.html', None),
    ('over-ons.html', 'over-ons'),
    ('sectoren.html', None),
    ('cases.html', None),
    ('contact.html', None),
    ('diensten/index.html', None),
    ('diensten/assembly.html', None),
    ('diensten/container-lossen.html', None),
    ('diensten/fulfillment.html', None),
    ('diensten/hub-services.html', None),
    ('diensten/labeling.html', None),
    ('diensten/repacking.html', None),
    ('diensten/rework.html', None),
    ('diensten/warehousing.html', None),
]

EN_FILES = [
    ('en/index.html', None),
    ('en/about.html', 'about'),
    ('en/sectors.html', None),
    ('en/cases.html', None),
    ('en/contact.html', None),
    ('en/services/index.html', None),
    ('en/services/assembly.html', None),
    ('en/services/container-unloading.html', None),
    ('en/services/fulfillment.html', None),
    ('en/services/hub-services.html', None),
    ('en/services/labeling.html', None),
    ('en/services/repacking.html', None),
    ('en/services/rework.html', None),
    ('en/services/warehousing.html', None),
]

for rel, active in NL_FILES:
    process_nl(os.path.join(BASE, rel), active)

for rel, active in EN_FILES:
    process_en(os.path.join(BASE, rel), active)

print('\nDone.')
