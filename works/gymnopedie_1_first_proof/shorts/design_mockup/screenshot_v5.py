from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "mockup_v5.html"
OUT_FULL = HERE / "mockup_v5_overview.png"
OUT_FRAMES = HERE / "v5_frames"
OUT_FRAMES.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    page = browser.new_page(viewport={"width": 1700, "height": 780}, device_scale_factor=2)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=str(OUT_FULL), full_page=True)
    print(f"overview -> {OUT_FULL}")

    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    frames = page.locator(".frame").all()
    for i, frame in enumerate(frames, 1):
        out = OUT_FRAMES / f"frame_{i}.png"
        frame.screenshot(path=str(out), scale="device")
        print(f"frame {i} -> {out}")

    browser.close()
print("done")
