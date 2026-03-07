from utils import Colors, cprint, wait_with_dots
try:
    from sprite_data import SPRITES, BG_PIXELS, SPRITE_PIXELS
except ImportError:
    SPRITES = {}
    BG_PIXELS = []
    SPRITE_PIXELS = {}

import copy
import time

# --- Sabitler ---
BG_WIDTH = 64
BG_HEIGHT = 28
SPRITE_SIZE = 16

# Oyuncu: soldan 6px, aşağıdan 4px
PLAYER_X = 6
PLAYER_Y = BG_HEIGHT - SPRITE_SIZE - 4  # 28 - 16 - 4 = 8

# Düşman: sağdan 6px, aşağıdan 4px
ENEMY_X = BG_WIDTH - SPRITE_SIZE - 6  # 64 - 16 - 6 = 42
ENEMY_Y = PLAYER_Y 


# --- ARKA PLAN + SPRITE BIRLESTIRME ---
def composite_battle_scene(player_rol, enemy_ad):
    """
    64x28 arka plan uzerine oyuncu ve dusman sprite'larini yerlestirir.
    Sonuc: 14 satir ANSI terminal ciktisi.
    """
    if not BG_PIXELS:
        return None

    scene = [row[:] for row in BG_PIXELS]

    # Oyuncu
    p_pixels = SPRITE_PIXELS.get(player_rol)
    if p_pixels:
        for y in range(SPRITE_SIZE):
            for x in range(SPRITE_SIZE):
                r, g, b, a = p_pixels[y][x]
                if a > 0:
                    px, py = x + PLAYER_X, y + PLAYER_Y
                    if 0 <= px < BG_WIDTH and 0 <= py < BG_HEIGHT:
                        scene[py][px] = (r, g, b, a)

    # Dusman
    e_pixels = SPRITE_PIXELS.get(enemy_ad)
    if e_pixels:
        for y in range(SPRITE_SIZE):
            for x in range(SPRITE_SIZE):
                r, g, b, a = e_pixels[y][x]
                if a > 0:
                    px, py = x + ENEMY_X, y + ENEMY_Y
                    if 0 <= px < BG_WIDTH and 0 <= py < BG_HEIGHT:
                        scene[py][px] = (r, g, b, a)

    lines = []
    for y in range(0, BG_HEIGHT, 2):
        line = ""
        for x in range(BG_WIDTH):
            r1, g1, b1, a1 = scene[y][x]
            r2, g2, b2, a2 = scene[y + 1][x]
            if a1 == 0 and a2 == 0: line += "\033[0m "
            elif a1 > 0 and a2 == 0: line += f"\033[0;38;2;{r1};{g1};{b1}m▀"
            elif a1 == 0 and a2 > 0: line += f"\033[0;38;2;{r2};{g2};{b2}m▄"
            else: line += f"\033[0;48;2;{r1};{g1};{b1};38;2;{r2};{g2};{b2}m▄"
        lines.append(line + "\033[0m")
    return lines


def _make_bar(current, maximum, length, fill_color, empty_char="-"):
    perc = int((current / max(1, maximum)) * length)
    return f"{fill_color}{'█' * perc}{Colors.RESET}{empty_char * (length - perc)}"


def battle_ui(player, enemy, turn_info=None):
    """
    Savas ekrani: Oyuncu solda, Dusman sagda. 
    Eski tarza donus: Barlar yanyana, basit etiketler.
    """
    ui_width = 64
    scene_lines = composite_battle_scene(player.rol, enemy.ad)

    if scene_lines:
        print("\n" + "=" * ui_width)
        for line in scene_lines: print(line)
    else:
        print("\n" + "=" * ui_width + "\n[SAHNE YOK]\n" + "=" * ui_width)

    print("-" * ui_width)

    # --- OYUNCU BILGILERI ---
    total_hp = player.can + player.kalkan
    hp_color = Colors.WHITE if player.kalkan > 0 else Colors.GREEN
    p_hp_bar = _make_bar(player.can, player.maks_can, 15, Colors.GREEN)
    if player.kalkan > 0:
        s_units = int((player.kalkan / player.maks_can) * 15)
        p_hp_bar = p_hp_bar[:-(s_units if s_units > 0 else 0)] + f"{Colors.WHITE}{'█' * s_units}{Colors.RESET}"

    p_info = [
        f" {Colors.GREEN}{player.ad}{Colors.RESET} [Lv.{player.seviye}]",
        f" HP: [{p_hp_bar}] {hp_color}{total_hp}/{player.maks_can}{Colors.RESET}",
        f" MP:[{_make_bar(player.mana, player.maks_mana, 8, Colors.BLUE)}] EP:[{_make_bar(player.enerji, player.maks_enerji, 8, Colors.YELLOW)}]",
        f" {Colors.GREY}HIZ:{player.hiz} ZIRH:{player.savunma} HASAR:{player.saldiri}{Colors.RESET}"
    ]
    
    # Savasci Ofke
    from oyuncu_bilgileri.savasci import Savasci
    if isinstance(player, Savasci):
        p_info.insert(3, f" \033[38;5;208mÖFKE:[{_make_bar(player.adrenalin, player.maks_adrenalin, 10, Colors.PURPLE)}]{Colors.RESET}")

    # --- DUSMAN BILGILERI ---
    e_hp_bar = _make_bar(enemy.can, enemy.maks_can, 15, Colors.RED)
    e_info = [
        f" {Colors.RED}{enemy.ad}{Colors.RESET} [Lv.{player.kat}]",
        f" HP: [{e_hp_bar}] {enemy.can}/{enemy.maks_can}",
        f" {Colors.GREY}HIZ:{enemy.hiz} ZIRH:{enemy.savunma} HASAR:{enemy.saldiri}{Colors.RESET}"
    ]

    # --- Ekrana Bas (Yanyana) ---
    # Not: Eski padding olan <45'i geri getiriyoruz.
    max_l = max(len(p_info), len(e_info))
    for i in range(max_l):
        p_line = p_info[i] if i < len(p_info) else ""
        e_line = e_info[i] if i < len(e_info) else ""
        # ANSI renk kodlarini hesaba katmadan padding yapmak zor, o yuzden manuel bosluk
        print(f"{p_line:<50} {e_line}")

    print("=" * ui_width + "\n")

    if turn_info:
        for info in turn_info: print(f"> {info}"); time.sleep(0.02)
        print("-" * ui_width)
    time.sleep(0.02)
