"""Render SVG to PNG via Playwright (Windows-friendly · no cairo binary)."""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def render(svg_path: Path, png_path: Path, size: int = 800):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><style>
      body {{ margin: 0; padding: 0; background: transparent; }}
      svg {{ display: block; width: {size}px; height: {size}px; }}
    </style></head>
    <body>{svg_path.read_text(encoding='utf-8')}</body>
    </html>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": size, "height": size}, device_scale_factor=1)
        page = await ctx.new_page()
        await page.set_content(html, wait_until="domcontentloaded")
        elem = await page.query_selector("svg")
        await elem.screenshot(path=str(png_path), omit_background=False)
        await browser.close()


if __name__ == "__main__":
    svg_path = Path(sys.argv[1])
    png_path = Path(sys.argv[2])
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 800
    asyncio.run(render(svg_path, png_path, size))
    print(f"Wrote: {png_path} ({size}x{size})")
