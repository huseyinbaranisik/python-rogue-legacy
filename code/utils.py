import os
import time
import sys
import threading

# --- RENK PALETI ---
class Colors:
    RESET  = "\033[0m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    GREY   = "\033[90m"
    ORANGE = "\033[38;5;208m"

    # Godlike
    RAINBOW_COLORS = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]

    # Arka plan
    BG_RED   = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE  = "\033[44m"
    BG_GREY  = "\033[100m"


# ---------------------------------------------------------------------------
# SES SİSTEMİ — winsound (Windows) / fallback
# ---------------------------------------------------------------------------
try:
    import winsound
    _SOUND_AVAILABLE = True
except ImportError:
    _SOUND_AVAILABLE = False


def _beep(freq, dur):
    """Arka planda ses çalar (bloke etmez)."""
    if not _SOUND_AVAILABLE:
        return
    def _play():
        try: winsound.Beep(int(freq), int(dur))
        except Exception: pass
    threading.Thread(target=_play, daemon=True).start()


class Sound:
    """Oyun sesleri. Hiçbiri bloke etmez."""

    @staticmethod
    def attack():
        _beep(440, 80)

    @staticmethod
    def hit():
        _beep(220, 120)

    @staticmethod
    def crit():
        _beep(660, 60)
        time.sleep(0.07)
        _beep(880, 100)

    @staticmethod
    def enemy_attack():
        _beep(180, 140)

    @staticmethod
    def level_up():
        for f in [523, 659, 784, 1047]:
            _beep(f, 120)
            time.sleep(0.11)

    @staticmethod
    def potion():
        _beep(784, 80)
        time.sleep(0.09)
        _beep(1047, 80)

    @staticmethod
    def escape_success():
        _beep(880, 60); time.sleep(0.06)
        _beep(1174, 120)

    @staticmethod
    def death():
        for f in [300, 250, 200, 150]:
            _beep(f, 160); time.sleep(0.15)

    @staticmethod
    def boss_intro():
        for f in [150, 140, 130, 120]:
            _beep(f, 250); time.sleep(0.2)


# ---------------------------------------------------------------------------
# YAZI YARDIMCILARI
# ---------------------------------------------------------------------------

def cprint(text, color=Colors.WHITE, end="\n", slow=False):
    if slow:
        print_slow(str(text), color=color)
    else:
        print(f"{color}{text}{Colors.RESET}", end=end)


def get_rainbow_text(text):
    colored = ""
    for i, char in enumerate(text):
        colored += f"{Colors.RAINBOW_COLORS[i % len(Colors.RAINBOW_COLORS)]}{char}"
    return colored + Colors.RESET


def print_rainbow(text, end="\n"):
    print(get_rainbow_text(text), end=end)


def print_rainbow_slow(text, delay=0.04):
    """Metni gökkuşağı renklerinde daktilo efektiyle yazar."""
    for i, char in enumerate(text):
        color = Colors.RAINBOW_COLORS[i % len(Colors.RAINBOW_COLORS)]
        print(f"{color}{char}{Colors.RESET}", end="", flush=True)
        time.sleep(delay)
    print()


def input_colored(text, color=Colors.CYAN):
    return input(f"{color}{text}{Colors.RESET}")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_slow(text, delay=0.018, color=Colors.WHITE):
    """Daktilo efekti."""
    for char in str(text):
        print(f"{color}{char}{Colors.RESET}", end="", flush=True)
        time.sleep(delay)
    print()


def battle_print(text, color=Colors.WHITE, delay=0.35):
    """Savaş mesajları — kısa gecikme + daktilo efekti."""
    time.sleep(delay)
    print_slow(text, delay=0.02, color=color)


def wait_with_dots(message="Devam", count=3, delay=0.4):
    sys.stdout.write(f"\n{Colors.GREY}{message}{Colors.RESET}")
    sys.stdout.flush()
    for _ in range(count):
        time.sleep(delay)
        sys.stdout.write(f"{Colors.GREY}.{Colors.RESET}")
        sys.stdout.flush()
    time.sleep(delay)
    print()
