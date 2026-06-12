from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "storyboard.html"
LABELS = ["1_before", "2_reveal", "3_number", "4_end"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    # filmstrip overview
    page = browser.new_page(viewport={"width": 4680, "height": 2120}, device_scale_factor=1)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(700)
    page.screenshot(path=str(HERE / "storyboard_overview.png"), full_page=True)
    print("overview ok")
    # clean frames
    page2 = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page2.goto(HTML.as_uri())
    page2.wait_for_load_state("networkidle")
    page2.wait_for_timeout(500)
    for label, frame in zip(LABELS, page2.locator(".frame").all()):
        out = HERE / f"frame_{label}.png"
        frame.screenshot(path=str(out), scale="device")
        print(f"frame {label} -> {out.name}")
    browser.close()
print("done")
