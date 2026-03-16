import sys, os
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:3000'
selector = sys.argv[2] if len(sys.argv) > 2 else 'body'
label = sys.argv[3] if len(sys.argv) > 3 else 'section'

out_dir = os.path.join(os.path.dirname(__file__), 'temporary screenshots')
os.makedirs(out_dir, exist_ok=True)

n = 1
while os.path.exists(os.path.join(out_dir, f'screenshot-{n}-{label}.png')):
    n += 1
out_path = os.path.join(out_dir, f'screenshot-{n}-{label}.png')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={'width': 390, 'height': 844},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    )
    page = context.new_page()
    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(1500)

    # Get position of element
    el = page.query_selector(selector)
    if el:
        box = el.bounding_box()
        print(f'Element top: {box["y"]}px')
        page.evaluate(f'window.scrollTo(0, {max(0, box["y"] - 60)})')
    page.wait_for_timeout(300)
    page.screenshot(path=out_path, full_page=False)
    browser.close()

print(f'Screenshot saved: temporary screenshots/screenshot-{n}-{label}.png')
