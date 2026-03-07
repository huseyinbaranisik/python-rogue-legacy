from PIL import Image
import os

def image_to_ansi(image_path):
    if not os.path.exists(image_path):
        return None
    
    try:
        img = Image.open(image_path).convert('RGBA')
        img = img.resize((16, 16))
        
        lines = []
        for y in range(0, 16, 2):
            line = ""
            for x in range(16):
                r1, g1, b1, a1 = img.getpixel((x, y))
                r2, g2, b2, a2 = img.getpixel((x, y+1))
                
                # Case 1: Both transparent
                if a1 == 0 and a2 == 0:
                    line += "\033[0m "
                # Case 2: Only top has color
                elif a1 > 0 and a2 == 0:
                    line += f"\033[0;38;2;{r1};{g1};{b1}m▀"
                # Case 3: Only bottom has color
                elif a1 == 0 and a2 > 0:
                    line += f"\033[0;38;2;{r2};{g2};{b2}m▄"
                # Case 4: Both have color
                else:
                    line += f"\033[0;48;2;{r1};{g1};{b1};38;2;{r2};{g2};{b2}m▄"
            lines.append(line + "\033[0m")
        return lines
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def image_to_pixels(image_path, width=16, height=16):
    """Görsel dosyasını RGBA piksel verisine çevirir."""
    if not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path).convert('RGBA')
        img = img.resize((width, height))
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(img.getpixel((x, y)))
            pixels.append(row)
        return pixels
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

base_path = r"c:\Users\win\OneDrive\Masaüstü\Projeler\Dungeon\görseller"

# Temel canavarlar (Varyasyonları olanlar)
base_monsters = {
    'Iskelet': 'skeleton',
    'Goblin': 'goblin',
    'Zombi': 'zombi',
    'Ateş Ruhu': 'fire_spirit',
    'Buz Ruhu': 'ice_spirit',
    'Düz Slime': 'normal_slime',
    'Ateş Slime': 'fire_slime',
    'Su Slime': 'water_slime',
    'Zehir Slime': 'poison_slime',
    'Dev Akrep': 'giant_scorpion',
    'Vahşi Kurt': 'wild_wolf',
    'Yer Altı Solucanı': 'underground_worm',
    'Golem': 'golem'
}

# Karakterler ve Diğer Sabit Sprite'lar (Varyasyonları olmayanlar)
base_characters = {
    'Savasci': 'ch_knight',
    'Buyucu': 'ch_wizard'
}

all_sprites = {}
all_sprite_pixels = {}

# Canavarları işle (Normal, SAMPIYON, ALTIN)
for name, file_base in base_monsters.items():
    # Normal (basic_ prefix)
    if name == 'Düz Slime':
        path = os.path.join(base_path, "basic_normal_slime.png")
    else:
        path = os.path.join(base_path, f"basic_{file_base}.png")
        
    sprite = image_to_ansi(path)
    if sprite: all_sprites[name] = sprite
    px = image_to_pixels(path)
    if px: all_sprite_pixels[name] = px
    
    # SAMPIYON (champion_ prefix)
    if name == 'Düz Slime':
        champ_path = os.path.join(base_path, "champion_basic_slime.png")
    else:
        champ_path = os.path.join(base_path, f"champion_{file_base}.png")
        
    sprite = image_to_ansi(champ_path)
    if sprite: all_sprites[f"SAMPIYON {name}"] = sprite
    px = image_to_pixels(champ_path)
    if px: all_sprite_pixels[f"SAMPIYON {name}"] = px
        
    # ALTIN (golden_ prefix)
    if name == 'Düz Slime':
        gold_path = os.path.join(base_path, "golden_basic_slime.png")
    else:
        gold_path = os.path.join(base_path, f"golden_{file_base}.png")
        
    sprite = image_to_ansi(gold_path)
    if sprite: all_sprites[f"ALTIN {name}"] = sprite
    px = image_to_pixels(gold_path)
    if px: all_sprite_pixels[f"ALTIN {name}"] = px

# Karakterleri işle
for name, file_base in base_characters.items():
    path = os.path.join(base_path, f"{file_base}.png")
    sprite = image_to_ansi(path)
    if sprite: all_sprites[name] = sprite
    px = image_to_pixels(path)
    if px: all_sprite_pixels[name] = px

# Arka plan piksel verisi
bg_pixels = image_to_pixels(os.path.join(base_path, "background.png"), width=64, height=28)

# sprite_data.py dosyasına kaydet
output_path = os.path.join(os.path.dirname(__file__), "sprite_data.py")
with open(output_path, "w", encoding="utf-8") as f:
    # --- SPRITES (ANSI) ---
    f.write("SPRITES = {\n")
    for name, lines in all_sprites.items():
        f.write(f"    '{name}': [\n")
        for line in lines:
            escaped_line = line.replace("\033", "\\033")
            f.write(f"        '{escaped_line}',\n")
        f.write("    ],\n")
    f.write("}\n\n")

    # --- BG_PIXELS ---
    f.write("BG_PIXELS = [\n")
    if bg_pixels:
        for row in bg_pixels:
            f.write(f"    {row},\n")
    f.write("]\n\n")

    # --- SPRITE_PIXELS ---
    f.write("SPRITE_PIXELS = {\n")
    for name, pixels in all_sprite_pixels.items():
        f.write(f"    '{name}': [\n")
        for row in pixels:
            f.write(f"        {row},\n")
        f.write("    ],\n")
    f.write("}\n")

print("\nSprite verileri başarıyla güncellendi!")
