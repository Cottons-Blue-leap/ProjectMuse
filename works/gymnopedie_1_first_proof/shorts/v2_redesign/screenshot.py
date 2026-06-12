from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "mockup.html"
OUT_OVERVIEW = HERE / "overview.png"

LABELS = ["A_image_forward", "B_text_forward", "C_fan_signal"]

with sync_playwright() as p:
    browser = p.chromium.launch()

    # 1) overview with captions + safezone guides
    page = browser.new_page(viewport={"width": 3640, "height": 2200}, device_scale_factor=1)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(600)
    page.screenshot(path=str(OUT_OVERVIEW), full_page=True)
    print(f"overview -> {OUT_OVERVIEW}")

    # 2) clean individual frames (hide safezone guides)
    page2 = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page2.goto(HTML.as_uri())
    page2.wait_for_load_state("networkidle")
    page2.add_style_tag(content=".ui-bottom,.ui-right{display:none !important;}")
    page2.wait_for_timeout(400)
    frames = page2.locator(".frame").all()
    for label, frame in zip(LABELS, frames):
        out = HERE / f"frame_{label}.png"
        frame.screenshot(path=str(out), scale="device")
        print(f"frame {label} -> {out}")

    browser.close()
print("done")
