"""Renders the README figures in assets/: hero.png, demo.gif, sprites.png.

usage:
  python tools/record_terminal.py frames.pkl --inputs "Ayla|1|1|2|2|2|2|2"   # real game, seed 7
  python tools/render_figures.py frames.pkl
Needs Pillow. Fonts (OFL) are in tools/fonts/: Silkscreen and Fira Code.
Colours: the dungeon background (görseller/background.png) for the page, Windows Terminal "Campbell" for the terminal.
"""
import os, pickle, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "tools", "fonts")
OUT = os.path.join(ROOT, "assets")
SPRITES = os.path.join(ROOT, "görseller")

# From görseller/background.png: stone, brick, dark brown, moss.
STONE, STONE_DK, BRICK, BROWN, MOSS = "#232323", "#171514", "#8F563B", "#663931", "#3F5F21"
TORCH, PARCH, ASH, LINE = "#E0A458", "#EDE3D1", "#A39C92", "#3A3330"
# Windows Terminal "Campbell", the console the game's run.bat opens.
TERM_BG, TERM_FG = (12, 12, 12), (204, 204, 204)
CAMPBELL = {"black": (12, 12, 12), "red": (197, 15, 31), "green": (19, 161, 14), "brown": (193, 156, 0),
            "yellow": (193, 156, 0), "blue": (0, 55, 218), "magenta": (136, 23, 152), "cyan": (58, 150, 221),
            "white": (204, 204, 204), "brightblack": (118, 118, 118), "brightred": (231, 72, 86),
            "brightgreen": (22, 198, 12), "brightyellow": (249, 241, 165), "brightblue": (59, 120, 255),
            "brightmagenta": (180, 0, 158), "brightcyan": (97, 214, 214), "brightwhite": (242, 242, 242)}

def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight:
        f.set_variation_by_axes([weight])
    return f

PIXEL = lambda s: font("Silkscreen-Regular.ttf", s)
PIXEL_B = lambda s: font("Silkscreen-Bold.ttf", s)
MONO = lambda s: font("FiraCode.ttf", s, 400)
MONO_B = lambda s: font("FiraCode.ttf", s, 600)

def colour(c, default):
    if c in ("default", None):
        return default
    if c in CAMPBELL:
        return CAMPBELL[c]
    if len(c) == 6:
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return default

def render_screen(frame, cols, rows, cw=11, ch=22, last_row=None):
    """Draws a pyte screen snapshot. Half blocks are filled rectangles so the pixel art stays crisp."""
    rows_used = rows if last_row is None else last_row
    im = Image.new("RGB", (cols * cw, rows_used * ch), TERM_BG)
    d = ImageDraw.Draw(im)
    f, fb = MONO(18), MONO_B(18)
    for y, row in enumerate(frame["rows"][:rows_used]):
        for x, (char, fg, bg, bold) in enumerate(row):
            x0, y0 = x * cw, y * ch
            fgc, bgc = colour(fg, TERM_FG), colour(bg, TERM_BG)
            if bgc != TERM_BG:
                d.rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1], fill=bgc)
            if char == "▄":
                d.rectangle([x0, y0 + ch // 2, x0 + cw - 1, y0 + ch - 1], fill=fgc)
            elif char == "▀":
                d.rectangle([x0, y0, x0 + cw - 1, y0 + ch // 2 - 1], fill=fgc)
            elif char == "█":
                d.rectangle([x0, y0 + 3, x0 + cw - 1, y0 + ch - 4], fill=fgc)
            elif char.strip():
                d.text((x0, y0 + 1), char, font=fb if bold else f, fill=fgc)
    return im

def shadow(im, box, r, offset=16, blur=24, alpha=170):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(layer).rounded_rectangle([x0, y0 + offset, x1, y1 + offset], r, fill=(0, 0, 0, alpha))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))

def terminal_window(im, xy, content, title):
    """Windows Terminal style frame (tab bar + body) around a rendered screen."""
    x0, y0 = xy
    w, h = content.width + 4, content.height + 46
    shadow(im, (x0, y0, x0 + w, y0 + h), 10)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 10, fill=(32, 32, 32), outline=(60, 60, 60), width=2)
    d.rounded_rectangle([x0 + 10, y0 + 8, x0 + 330, y0 + 44], 8, fill=TERM_BG)
    d.text((x0 + 26, y0 + 16), title, font=MONO(16), fill=TERM_FG)
    for i, sym in enumerate(["—", "□", "×"]):
        d.text((x0 + w - 110 + i * 36, y0 + 12), sym, font=MONO(18), fill=(170, 170, 170))
    im.paste(content, (x0 + 2, y0 + 44))
    return w, h

def sprite(name, scale):
    return Image.open(os.path.join(SPRITES, name)).convert("RGBA").resize((16 * scale, 16 * scale), Image.NEAREST)

def chip(d, xy, text, f, fill, color):
    x, y = xy
    w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 28, y + f.size + 18], fill=fill)
    d.text((x + 14, y + 7), text, font=f, fill=color)
    return x + w + 28

def caption(d, x, y, fig, title):
    nx = chip(d, (x, y), f"FIG. {fig}", PIXEL(16), BRICK, PARCH)
    d.text((nx + 16, y + 2), title, font=MONO_B(24), fill=PARCH)

def brick_strip(d, x0, y0, x1, h=14):
    """A row of bricks in the background tile's colours, used as a divider."""
    x, row = x0, 0
    while x < x1:
        w = 44
        d.rectangle([x, y0, min(x + w - 3, x1), y0 + h - 3], fill=BRICK if (x // w) % 3 else BROWN)
        x += w

def hero(battle):
    W, H = 1800, 880
    im = Image.new("RGBA", (W, H), STONE_DK)
    d = ImageDraw.Draw(im)
    x = 100
    nx = x
    for t in ["Python", "Terminal RPG", "ANSI pixel art"]:
        nx = chip(d, (nx, 118), t, PIXEL(16), STONE, TORCH) + 10
    d.text((x - 4, 182), "DUNGEON", font=PIXEL_B(96), fill=PARCH)
    d.text((x - 4, 282), "ASCENT", font=PIXEL_B(96), fill=TORCH)
    d.text((x, 404), "Zindan Macerası", font=MONO_B(30), fill=ASH)
    y = 466
    desc = ["A turn-based RPG that runs in", "your terminal: 4 classes, 100 floors,",
            "boss fights, loot and a shop, with", "pixel-art battles drawn in text."]
    for line in desc:
        d.text((x, y), line, font=MONO(25), fill=PARCH); y += 38
    brick_strip(d, x, 640, 700)
    d.text((x, 670), "Hüseyin Baran Işık", font=MONO(18), fill=ASH)

    shot = render_screen(battle, 80, 40, cw=11, ch=22, last_row=23)  # scene + both stat blocks
    shot = shot.crop((0, 0, 66 * 11, shot.height))
    terminal_window(im, (W - 100 - shot.width - 4, 110), shot, "py main.py")

    # floating card: the sprites the scene is built from
    cx0, cy0, cx1, cy1 = 900, 636, 1390, 796
    shadow(im, (cx0, cy0, cx1, cy1), 6, offset=10, blur=18, alpha=200)
    d = ImageDraw.Draw(im)
    d.rectangle([cx0, cy0, cx1, cy1], fill=STONE, outline=BRICK, width=3)
    d.text((cx0 + 22, cy0 + 16), "16 x 16 SPRITES", font=PIXEL(16), fill=TORCH)
    for i, n in enumerate(["ch_knight.png", "ch_wizard.png", "basic_goblin.png", "basic_skeleton.png", "basic_normal_slime.png"]):
        im.alpha_composite(sprite(n, 5), (cx0 + 20 + i * 92, cy0 + 56))
    return im.convert("RGB")

def demo(rec):
    cols, frames = rec["cols"], rec["frames"]
    base = Image.new("RGB", (cols * 11 + 4 + 80, 40 * 22 + 46 + 120), STONE_DK)
    out, durs = [], []
    for i, fr in enumerate(frames):
        nxt = frames[i + 1]["t"] if i + 1 < len(frames) else fr["t"] + 1.5
        ms = int(max(60, min(1600, (nxt - fr["t"] + fr["hold"]) * 1000 * 0.75)))  # 0.75: a little faster than real
        img = base.copy().convert("RGBA")
        d = ImageDraw.Draw(img)
        caption(d, 40, 30, 2, "Real run: seed 7, a Savasci clears floor 1")
        terminal_window(img, (40, 90), render_screen(fr, cols, 40), "py main.py")
        out.append(img.convert("RGB").quantize(colors=192, method=Image.Quantize.FASTOCTREE)); durs.append(ms)
    out[0].save(os.path.join(OUT, "demo.gif"), save_all=True, append_images=out[1:], duration=durs, loop=0, optimize=True)
    return out[-1]

def sprites_fig():
    """How a 16x16 PNG becomes 8 rows of half-block characters (convert_sprites.py / ui_helper.py)."""
    W, H = 1600, 660
    im = Image.new("RGBA", (W, H), STONE_DK)
    d = ImageDraw.Draw(im)
    caption(d, 70, 44, 3, "From a 16x16 PNG to terminal characters")
    src = Image.open(os.path.join(SPRITES, "ch_knight.png")).convert("RGBA")
    # 1: the sprite
    px = 20
    ox, oy = 70, 130
    d.rectangle([ox - 2, oy - 2, ox + 16 * px + 1, oy + 16 * px + 1], outline=LINE, width=2)
    for y in range(16):
        for x in range(16):
            r, g, b, a = src.getpixel((x, y))
            fill = (r, g, b) if a else ((40, 40, 40) if (x + y) % 2 else (30, 30, 30))
            d.rectangle([ox + x * px, oy + y * px, ox + x * px + px - 1, oy + y * px + px - 1], fill=fill)
    d.text((ox, oy + 16 * px + 18), "görseller/ch_knight.png", font=MONO(17), fill=ASH)
    # 2: one pair of pixel rows becomes one text row
    ax = ox + 16 * px + 70
    d.text((ax, oy), "2 pixel rows = 1 text row", font=MONO_B(22), fill=PARCH)
    pair_y = 4  # the helmet rows: the most colour in one pair
    for x in range(16):
        for k in range(2):
            r, g, b, a = src.getpixel((x, pair_y + k))
            fill = (r, g, b) if a else (30, 30, 30)
            d.rectangle([ax + x * 26, oy + 50 + k * 26, ax + x * 26 + 24, oy + 50 + k * 26 + 24], fill=fill)
    # one example cell per rule, drawn (the half-block glyphs render poorly at this size)
    top_c, bot_c = (205, 205, 205), (150, 150, 150)
    rules = [("top + bottom", (top_c, bot_c), "lower half block, background = top"),
             ("top only", (top_c, None), "upper half block, top colour"),
             ("bottom only", (None, bot_c), "lower half block, bottom colour"),
             ("transparent", (None, None), "a space")]
    for i, (k, (tc, bc), v) in enumerate(rules):
        yy = oy + 130 + i * 54
        d.text((ax, yy + 8), k, font=MONO_B(19), fill=TORCH)
        cx = ax + 170
        d.rectangle([cx, yy, cx + 21, yy + 43], fill=TERM_BG, outline=LINE)
        if tc: d.rectangle([cx + 1, yy + 1, cx + 20, yy + 21], fill=tc)
        if bc: d.rectangle([cx + 1, yy + 22, cx + 20, yy + 42], fill=bc)
        d.text((cx + 40, yy + 8), v, font=MONO(19), fill=PARCH)
    d.text((ax, oy + 360), "ESC[0;48;2;R;G;B;38;2;R;G;Bm + U+2584 (24-bit colour)", font=MONO(17), fill=ASH)
    # 3: the result, as the terminal draws it
    rx = W - 70 - 16 * 22
    d.text((rx, oy), "in the terminal: 16 x 8 cells", font=MONO_B(22), fill=PARCH)
    cell_w, cell_h = 22, 44
    for ty in range(8):
        for x in range(16):
            top, bot = src.getpixel((x, ty * 2)), src.getpixel((x, ty * 2 + 1))
            x0, y0 = rx + x * cell_w, oy + 50 + ty * cell_h
            d.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h - 1], fill=TERM_BG)
            if top[3]:
                d.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h // 2 - 1], fill=top[:3])
            if bot[3]:
                d.rectangle([x0, y0 + cell_h // 2, x0 + cell_w - 1, y0 + cell_h - 1], fill=bot[:3])
    d.text((rx, oy + 50 + 8 * cell_h + 18), "battle scene: 64 x 28 px -> 64 x 14 cells", font=MONO(17), fill=ASH)
    return im.convert("RGB")

if __name__ == "__main__":
    rec = pickle.load(open(sys.argv[1], "rb"))
    first_battle = next(f for f in rec["frames"] if any("Hamlen" in "".join(c[0] for c in r) for r in f["rows"]))
    hero(first_battle).save(os.path.join(OUT, "hero.png"), optimize=True)
    demo(rec)
    sprites_fig().save(os.path.join(OUT, "sprites.png"), optimize=True)
    print("figures ->", OUT)
