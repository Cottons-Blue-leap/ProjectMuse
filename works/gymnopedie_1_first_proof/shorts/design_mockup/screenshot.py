from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "mockup.html"
OUT_FULL = HERE / "mockup_overview.png"
OUT_FRAMES = HERE / "frames"
OUT_FRAMES.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Overview: all 4 frames side by side
    page = browser.new_page(viewport={"width": 1720, "height": 780}, device_scale_factor=2)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=str(OUT_FULL), full_page=True)
    print(f"overview -> {OUT_FULL}")

    # Individual full-resolution frames (1080x1920 each)
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")

    frames = page.locator(".frame").all()
    for i, frame in enumerate(frames, 1):
        # render each frame at 1080x1920 by scaling up via element bounding box screenshot
        out = OUT_FRAMES / f"frame_{i}.png"
        frame.screenshot(path=str(out), scale="device")
        print(f"frame {i} -> {out}")

    browser.close()
print("done")
