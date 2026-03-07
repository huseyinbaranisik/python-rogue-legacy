"""
main.py — Zindan Macerası | Ana oyun kontrolcüsü
"""
import random
import time
import pickle
import os

from utils import Colors, cprint, input_colored, clear_screen, print_slow, wait_with_dots
from ui_helper import battle_ui
from entity import Entity
from oyuncu_bilgileri.player import Player
from oyuncu_bilgileri.savasci import Savasci
from oyuncu_bilgileri.buyucu import Buyucu
from oyuncu_bilgileri.haydut import Haydut
from oyuncu_bilgileri.tank import Tank
from dusman_bilgileri.canavarlar import (
    Skeleton, Goblin, Zombie, Wolf, Golem, Worm, Scorpion,
    AtesRuhu, BuzRuhu, Basilisk, Slime, rastgele_slime_getir
)
from dusman_bilgileri.golden_enemy import GoldenEnemy
from dusman_bilgileri.champion_enemy import ChampionEnemy
from dusman_bilgileri.bosslar.boss import Boss
from dusman_bilgileri.bosslar.goblin_generali import GoblinGenerali
from dusman_bilgileri.bosslar.ejder_prens import EjderPrens
from dusman_bilgileri.bosslar.perona import HirsizlarKiralicesi
from dusman_bilgileri.bosslar.void import Void
from esya_bilgileri.savasci_items import get_savasci_weapons, get_savasci_armors
from esya_bilgileri.buyucu_items import get_buyucu_weapons, get_buyucu_armors
from esya_bilgileri.haydut_items import get_haydut_weapons, get_haydut_armors
from esya_bilgileri.tank_items import get_tank_weapons, get_tank_armors
from esya_bilgileri.takilar.yuzukler import get_accessories

# Modüler mixin'ler
from savas import SavasMixin, get_potion_info
from dukkan import DukkanMixin

# --- SABITLER ---
QUALITY_LEVELS = ["Temel", "Basit", "Orta Kalite", "Kaliteli", "Üstün",
                  "Görkemli", "Efsanevi", "Ruhani", "İlahi", "Kadim"]
MONUMENT_BASE_PROB  = 0.02
MONUMENT_RARE_CHANCE = 0.20
MONUMENT_RARE_BOOST  = 0.2
MONUMENT_NORMAL_BOOST = 0.1


# ---------------------------------------------------------------------------
# OYUN KONTROLCÜSÜ
# ---------------------------------------------------------------------------
class Game(SavasMixin, DukkanMixin):
    def __init__(self):
        self.oyuncu       = None
        self.monument_prob = MONUMENT_BASE_PROB
        self.tum_esyalar  = []
        self.battle_log   = []
        self.boss_katlari = {
            25: GoblinGenerali,
            50: EjderPrens,
            75: HirsizlarKiralicesi,
            100: Void
        }

    # -----------------------------------------------------------------------
    # BAŞLANGIÇ & KAYIT
    # -----------------------------------------------------------------------
    def start(self):
        clear_screen()
        cprint("\n=== ZINDAN MACERASI ===", Colors.PURPLE)
        if self.check_save_exists():
            print("1. Yeni Oyun")
            print("2. Devam Et (Kayitli Oyun)")
            if input_colored("Secim: ") == "2":
                if self.load_game():
                    print_slow(f"\n{self.oyuncu.ad} geri dondu! Macera devam ediyor...", color=Colors.GREEN)
                    time.sleep(1)
                    self.game_loop()
                    return
        isim = input_colored("Kahramanin Adi: ")
        cprint("\nSINIFINI SEC:", Colors.CYAN)
        print("1. Savasci\n2. Buyucu\n3. Haydut\n4. Tank")
        secim = ""
        while secim not in ["1", "2", "3", "4"]:
            secim = input_colored("Secim (1-4): ")
        self.oyuncu = {"1": Savasci, "2": Buyucu, "3": Haydut, "4": Tank}[secim](isim)
        self._load_class_items()
        cprint(f"\n{self.oyuncu.ad} hazir! Zindana giriliyor...", color=Colors.GREEN, slow=True)
        time.sleep(1)
        self.game_loop()

    def save_game(self):
        try:
            with open("savegame.dat", "wb") as f:
                pickle.dump({"player": self.oyuncu, "floor": self.oyuncu.kat}, f)
            cprint("\n[OYUN BASARIYLA KAYDEDILDI]", Colors.GREEN)
            time.sleep(1)
        except Exception as e:
            cprint(f"\n[KAYIT HATASI: {e}]", Colors.RED)
            time.sleep(2)

    def load_game(self):
        if not self.check_save_exists(): return False
        try:
            with open("savegame.dat", "rb") as f:
                data = pickle.load(f)
            self.oyuncu = data["player"]
            self._load_class_items()
            return True
        except Exception as e:
            cprint(f"\n[YUKLEME HATASI: {e}]", Colors.RED)
            time.sleep(2)
            return False

    def check_save_exists(self):
        return os.path.exists("savegame.dat")

    def _load_class_items(self):
        loaders = {
            Savasci: (get_savasci_weapons, get_savasci_armors),
            Buyucu:  (get_buyucu_weapons,  get_buyucu_armors),
            Haydut:  (get_haydut_weapons,  get_haydut_armors),
            Tank:    (get_tank_weapons,    get_tank_armors),
        }
        self.tum_esyalar = []
        for cls, (get_w, get_a) in loaders.items():
            if isinstance(self.oyuncu, cls):
                self.tum_esyalar.extend(get_w())
                self.tum_esyalar.extend(get_a())
                break
        self.tum_esyalar.extend(get_accessories())

    # -----------------------------------------------------------------------
    # ANA DÖNGÜ
    # -----------------------------------------------------------------------
    def game_loop(self):
        while self.oyuncu.hayatta_mi():
            clear_screen()
            self.oyuncu.istatistikleri_goster()
            cprint("\nNE YAPACAKSIN?", Colors.CYAN)
            print("1. Ilerle (Savas/Macera)")
            print("2. Envanter & Iksir")
            print("3. Ekipman Yonetimi")
            print("4. Karakter & Yetenek Puani")
            print("5. Kaydet ve Cik")
            choice = input_colored("\n>> ")
            if   choice == "1": self.advance_floor()
            elif choice == "2": self.inventory_menu()
            elif choice == "3": self.equipment_menu()
            elif choice == "4": self.character_menu()
            elif choice == "5": self.save_game(); break
        cprint("\n--- OYUN BITTI ---", Colors.RED)

    # -----------------------------------------------------------------------
    # KAT ILERLEME & ETKİNLİKLER
    # -----------------------------------------------------------------------
    def advance_floor(self):
        cprint(f"\n[{self.oyuncu.kat}. KAT]", Colors.PURPLE)
        time.sleep(0.5)
        if self.oyuncu.kat in self.boss_katlari:
            cprint(f"\n!!! {self.oyuncu.kat}. KAT: BOSS KAPISI !!!", Colors.RED, slow=True)
            time.sleep(1)
            self.boss_battle(self.boss_katlari[self.oyuncu.kat])
        else:
            if self.oyuncu.kat % 5 == 0:
                self.merchant_event()
            elif random.random() < self.monument_prob:
                self.monument_event()
                self.monument_prob = MONUMENT_BASE_PROB
            else:
                self.monument_prob += MONUMENT_BASE_PROB
                self.battle_phase()
        self.oyuncu.kat += 1

    def monument_event(self):
        cprint("\n--- ANTIK GUC ANITI ---", Colors.PURPLE)
        if random.random() < MONUMENT_RARE_CHANCE:
            cprint("!!! NADIR GOKSEL ANIT BULDUN !!!", Colors.YELLOW)
            boost = MONUMENT_RARE_BOOST
        else:
            cprint("Taslanmis bir guc aniti buldun.", Colors.CYAN)
            boost = MONUMENT_NORMAL_BOOST
        print("Hangi yeteneginin gucunu kalici olarak arttiracaksin?")
        for i, s in enumerate(self.oyuncu.yetenekler):
            print(f"{i+1}. {s} (Su an: x{self.oyuncu.yetenek_carpanlari[i]:.2f})")
        try:
            sel = int(input_colored("Secim: ")) - 1
            if 0 <= sel < len(self.oyuncu.yetenekler):
                self.oyuncu.yetenek_carpanlari[sel] += boost
                cprint(f"!!! {self.oyuncu.yetenekler[sel]} GUCU ARTTI! (Yeni: x{self.oyuncu.yetenek_carpanlari[sel]:.2f})", Colors.GREEN)
        except (ValueError, IndexError):
            pass
        wait_with_dots()

    # -----------------------------------------------------------------------
    # MENÜLER
    # -----------------------------------------------------------------------
    def character_menu(self):
        stat_map = {
            "1": ("max_hp",     "+25 HP",  "maks_can"),
            "2": ("max_mana",   "+15 MP",  "maks_mana"),
            "3": ("max_energy", "+10 EP",  "maks_enerji"),
            "4": ("attack",     "+5 ATK",  "saldiri"),
            "5": ("defense",    "+3 DEF",  "savunma"),
            "6": ("speed",      "+2 HIZ",  "hiz"),
        }
        while True:
            clear_screen()
            cprint(f"\n--- KARAKTER GELISIMI ({self.oyuncu.yetenek_puanlari} Puan) ---", Colors.CYAN)
            for k, (stat, label, base_key) in stat_map.items():
                print(f"{k}. {label:<12} Su an: {self.oyuncu.temel_istatistikler[base_key]}")
            print("0. Geri Don")
            c = input_colored("Secim: ")
            if c == "0": break
            if c in stat_map:
                self.oyuncu.istatistik_arttır(stat_map[c][0])
                time.sleep(1)

    def inventory_menu(self):
        color_map = {"Can": Colors.RED, "Mana": Colors.BLUE, "Enerji": Colors.YELLOW,
                     "Dayanıklılık": Colors.WHITE, "Taze": Colors.GREEN}
        while True:
            clear_screen()
            cprint(f"--- CANTA | HP:{self.oyuncu.can}/{self.oyuncu.maks_can} "
                   f"MP:{self.oyuncu.mana}/{self.oyuncu.maks_mana} "
                   f"EP:{self.oyuncu.enerji}/{self.oyuncu.maks_enerji} ---", Colors.CYAN)
            items = list(self.oyuncu.envanter.keys())
            for i, item in enumerate(items):
                color = next((c for k, c in color_map.items() if k in item), Colors.GREEN)
                info  = get_potion_info(item)
                print(f"{i+1}. {color}{item:25}{Colors.RESET} ({info['desc']}) (x{self.oyuncu.envanter[item]})")
            print("0. Geri Don")
            choice = input_colored("No: ")
            if choice == "0": break
            try:
                idx = int(choice) - 1
                if not (0 <= idx < len(items)): continue
                name = items[idx]
                if self.oyuncu.envanter.get(name, 0) <= 0:
                    cprint("O esyadan kalmadi.", Colors.RED); time.sleep(1); continue
                self.oyuncu.envanter[name] -= 1
                info = get_potion_info(name)
                if "Can İksiri" in name:
                    self.oyuncu.iyiles(info["val"])
                elif "Mana İksiri" in name:
                    self.oyuncu.mana_yenile(info["val"])
                elif "Enerji İksiri" in name:
                    self.oyuncu.enerji_yenile(info["val"])
                elif name == "Taze Başlangıç":
                    self.oyuncu.can = self.oyuncu.maks_can
                    self.oyuncu.mana = self.oyuncu.maks_mana
                    self.oyuncu.enerji = self.oyuncu.maks_enerji
                    cprint("Tum barlar fullendi!", Colors.GREEN)
                elif "Dayanıklılık İksiri" in name:
                    self.oyuncu.kalkan += info["val"]
                    cprint(f"+{info['val']} Kalkan eklendi!", Colors.WHITE)
                time.sleep(1)
            except (ValueError, IndexError, KeyError):
                pass

    def equipment_menu(self):
        while True:
            clear_screen()
            cprint("\n--- EKIPMAN YONETIMI ---", Colors.CYAN)
            print("GIYILI EKIPMANLAR:")
            for slot, item in self.oyuncu.ekipman.items():
                desc = f"{item.get_colored_name()} {item.get_stats_str()}" if item else "Bos"
                print(f"  {slot.upper()}: {desc}")
            print("\nCANTADAKI EKIPMANLAR:")
            if not self.oyuncu.ekipman_envanteri:
                print("  (Bos)")
            else:
                for i, item in enumerate(self.oyuncu.ekipman_envanteri):
                    print(f"  {i+1}. {item.get_colored_name()} {item.get_stats_str()} ({item.item_type})")
            print("\n1. Esya Giy\n2. Esya Cikar\n0. Geri Don")
            c = input_colored("Secim: ")
            if c == "0": break
            elif c == "1":
                if not self.oyuncu.ekipman_envanteri:
                    cprint("Giyilecek esya yok!", Colors.RED); time.sleep(1); continue
                try:
                    idx = int(input_colored("Hangi esya (No): ")) - 1
                    if 0 <= idx < len(self.oyuncu.ekipman_envanteri):
                        self.oyuncu.esya_kuşan(self.oyuncu.ekipman_envanteri.pop(idx))
                        time.sleep(1)
                except (ValueError, IndexError):
                    pass
            elif c == "2":
                print("1. Silah\n2. Zirh\n3. Aksesuar")
                slot_map = {"1": "silah", "2": "zirh", "3": "aksesuar"}
                sc = input_colored("Hangi slot (1-3): ")
                if sc in slot_map:
                    self.oyuncu.esya_cıkar(slot_map[sc])
                    time.sleep(1)


if __name__ == "__main__":
    game = Game()
    game.start()
