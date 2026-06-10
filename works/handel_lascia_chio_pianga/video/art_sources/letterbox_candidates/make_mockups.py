# Letterbox candidate mockups — ⑩ Handel Lascia ch'io pianga (cover 실측 팔레트 기반)
# 1280x720 preview: vertical 3-stop gradient + cover center + waveform mock + text stack
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
COVER = HERE.parent.parent / "cover" / "Miku_rossetti_proserpine_1874_gap.png"

W, H = 1280, 720
COVER_SIZE = 480  # 720/1080 비율 정합

# round 1 (컬러 3안): A_shaft_of_light #0F1B17/#4A4226/#9C8B60 · B_captive_teal #0E1D1B/#2F4D46/#8FB0A6
#                       · C_pomegranate_bronze #16100C/#54301F/#B08355 (1차 LOCK → 무채 round로 재검토)
# round 2 (무채 3안 · 코튼 제안 2026-06-11): 파리넬리 흰색 = 카스트라토 순수·텅 빈 마음 상징
CANDIDATES = {
    "D_farinelli_ivory": ["#181614", "#6F6A60", "#D8D2C4"],
    "E_pure_silver": ["#121212", "#5C5C5C", "#CCCCCC"],
    "F_cool_ash": ["#121416", "#565C61", "#BFC7CD"],
}

TEXT = "#e8e0c8"


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient(colors):
    img = Image.new("RGB", (W, H))
    c0, c1, c2 = [hex2rgb(c) for c in colors]
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        c = lerp(c0, c1, t / 0.5) if t <= 0.5 else lerp(c1, c2, (t - 0.5) / 0.5)
        for x in range(W):
            px[x, y] = c
    return img


def waveform(draw, cx, color, seed):
    rnd = random.Random(seed)
    n, gap = 22, 9
    x0 = cx - (n * gap) // 2
    for i in range(n):
        h = rnd.randint(8, 90)
        x = x0 + i * gap
        draw.rounded_rectangle([x, H // 2 - h // 2, x + 3, H // 2 + h // 2], radius=2, fill=color)


def font(size, italic=False):
    try:
        name = "georgiai.ttf" if italic else "georgia.ttf"
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


cover = Image.open(COVER).convert("RGB").resize((COVER_SIZE, COVER_SIZE), Image.LANCZOS)

for name, colors in CANDIDATES.items():
    img = gradient(colors)
    img.paste(cover, ((W - COVER_SIZE) // 2, (H - COVER_SIZE) // 2))
    d = ImageDraw.Draw(img)
    bar = hex2rgb(colors[2])
    waveform(d, (W - COVER_SIZE) // 4, bar, 7)
    waveform(d, W - (W - COVER_SIZE) // 4, bar, 13)
    d.text((54, H - 96), "George Frideric Handel", font=font(20), fill=TEXT)
    d.text((54, H - 68), "Lascia ch'io pianga", font=font(34), fill=TEXT)
    d.text((W - 54, H - 44), "Atelier Miku Acappella", font=font(16), fill=TEXT, anchor="ra")
    out = HERE / f"{name}.png"
    img.save(out)
    print(out.name, colors)
