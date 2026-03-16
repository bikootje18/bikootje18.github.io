import sys, os
from playwright.sync_api import sync_playwright

url = sys.argv[1]
selector = sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else 'el'

out_dir = os.path.join(os.path.dirname(__file__), 'temporary screenshots')
os.makedirs(out_dir, exist_ok=True)
n = 1
while os.path.exists(os.path.join(out_dir, f'screenshot-{n}-{label}.png')):
    n += 1
out_path = os.path.join(out_dir, f'screenshot-{n}-{label}.png')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={'width': 390, 'height': 6000},  # tall viewport = no scroll needed
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
    )
    page = context.new_page()
    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(1500)
    el = page.query_selector(selector)
    if el:
        el.screenshot(path=out_path)
        print(f'Element screenshot saved: temporary screenshots/screenshot-{n}-{label}.png')
    else:
        print('Element not found')
    browser.close()
