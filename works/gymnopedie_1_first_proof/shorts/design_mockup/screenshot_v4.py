from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "mockup_v4.html"
OUT_FULL = HERE / "mockup_v4_overview.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 540, "height": 2200}, device_scale_factor=2)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=str(OUT_FULL), full_page=True)
    print(f"overview -> {OUT_FULL}")
    browser.close()
print("done")
