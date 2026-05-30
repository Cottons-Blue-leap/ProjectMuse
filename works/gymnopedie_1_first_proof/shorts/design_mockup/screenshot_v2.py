from playwright.sync_api import sync_playwright
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "mockup_v2.html"
OUT_FULL = HERE / "mockup_v2_overview.png"
OUT_VARIATIONS = HERE / "v2_variations"
OUT_VARIATIONS.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Full overview
    page = browser.new_page(viewport={"width": 1440, "height": 2000}, device_scale_factor=2)
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path=str(OUT_FULL), full_page=True)
    print(f"overview -> {OUT_FULL}")

    # Per-variation screenshots
    variations = page.locator(".variation").all()
    for i, var in enumerate(variations, 1):
        labels = ["A_hook_forward", "B_mystery", "C_story_build"]
        out = OUT_VARIATIONS / f"v2_{labels[i-1]}.png"
        var.screenshot(path=str(out), scale="device")
        print(f"variation {i} -> {out}")

    browser.close()
print("done")
