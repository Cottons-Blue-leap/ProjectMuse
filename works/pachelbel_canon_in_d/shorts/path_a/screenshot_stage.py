from playwright.sync_api import sync_playwright
from pathlib import Path
HERE = Path(__file__).parent
HTML = HERE / "storyboard_stage.html"
LABELS = ["stage_1", "stage_2", "stage_3"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
    pg.goto(HTML.as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(500)
    for label, fr in zip(LABELS, pg.locator(".frame").all()):
        fr.screenshot(path=str(HERE/f"frame_{label}.png"), scale="device"); print(label)
    b.close()
print("done")
