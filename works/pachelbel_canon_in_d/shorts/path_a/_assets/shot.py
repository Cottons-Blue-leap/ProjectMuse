from playwright.sync_api import sync_playwright
from pathlib import Path
H=Path(__file__).parent
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":800,"height":1400},device_scale_factor=1)
    pg.goto((H/"miku_asset.html").as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
    for cid in ["wait","sing"]:
        pg.locator("#"+cid).screenshot(path=str(H/f"miku_{cid}.png"), omit_background=True)
        print(cid)
    b.close()
print("done")
