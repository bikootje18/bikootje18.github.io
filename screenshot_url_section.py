import sys, os
from playwright.sync_api import sync_playwright

url = sys.argv[1]
text = sys.argv[2]  # text to find in element
label = sys.argv[3] if len(sys.argv) > 3 else 'section'

out_dir = os.path.join(os.path.dirname(__file__), 'temporary screenshots')
os.makedirs(out_dir, exist_ok=True)
n = 1
while os.path.exists(os.path.join(out_dir, f'screenshot-{n}-{label}.png')):
    n += 1
out_path = os.path.join(out_dir, f'screenshot-{n}-{label}.png')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(1500)
    el = page.locator(f'text={text}').locator('xpath=ancestor::section[1]')
    if el.count():
        el.first.screenshot(path=out_path)
        print(f'Saved: {out_path}')
    else:
        print('Not found')
    browser.close()
