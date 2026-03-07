"""
savas.py — Tüm savaş mekanikleri (battle_phase, boss_battle, player_select_action, turn_enemy vs.)
"""
import random
import time

from utils import Colors, cprint, input_colored, wait_with_dots, battle_print, Sound
from entity import Entity
from oyuncu_bilgileri.savasci import Savasci
from oyuncu_bilgileri.buyucu import Buyucu
from oyuncu_bilgileri.haydut import Haydut
from oyuncu_bilgileri.tank import Tank
from dusman_bilgileri.canavarlar import (
    Worm, Wolf, Scorpion, Zombie, AtesRuhu, BuzRuhu, Basilisk, Slime,
    Skeleton, Goblin, Golem, rastgele_slime_getir
)
from dusman_bilgileri.golden_enemy import GoldenEnemy
from dusman_bilgileri.champion_enemy import ChampionEnemy
from ui_helper import battle_ui

# Tüm düşmanların karşılaşma oranları ve temel güç çarpanları
CHAMPION_CHANCE    = 0.05   # Odaya giren düşmanın Şampiyon özellikli olma ihtimali (%5)
GOLDEN_CHANCE      = 0.20   # Odaya giren düşmanın Altın (nadir ödüller) özellikli olma ihtimali (%20)
ENEMY_POWER_RATIO  = 0.77   # Normal düşmanların oyuncuya kıyasla standart stat dengeleme çarpanı
BOSS_POWER_RATIO   = 0.90   # Bölüm sonu canavarlarının oyuncuya kıyasla standart stat dengeleme çarpanı

# ----------------------------------------------------------------------------------------------------
# İKSİR VE EŞYA ÖZELLİKLERİ YARDIMCI FONKSİYONLARI
# ----------------------------------------------------------------------------------------------------
QUALITY_LEVELS = ["Temel", "Basit", "Orta Kalite", "Kaliteli", "Üstün",
                  "Görkemli", "Efsanevi", "Ruhani", "İlahi", "Kadim"]

def get_potion_info(ad):
    """
    Parametre olarak alınan iksir adını inceler ve iyileştirme gücünü hesaplayarak döndürür.
    İksirin başındaki kalite seviyesi arttıkça, verdiği stat değeri (Can, Mana vb.) katlanarak artar.
    """
    mult = next((i + 1 for i, k in enumerate(QUALITY_LEVELS) if k in ad), 1)
    specs = {
        "Can İksiri":       (50, "CAN",    "yeniler"),
        "Mana İksiri":      (40, "MANA",   "yeniler"),
        "Enerji İksiri":    (40, "ENERJI", "yeniler"),
        "Dayanıklılık İksiri": (50, "Kalkan", "ekler"),
    }
    for ptype, (base, key, verb) in specs.items():
        if ptype in ad:
            val = base * mult
            return {"val": val, "desc": f"{val} {key} {verb}"}
    if "Taze Başlangıç" in ad:
        return {"val": 0, "desc": "Tüm barları fuller"}
    return {"val": 0, "desc": ""}


# ----------------------------------------------------------------------------------------------------
# SAVAŞ MEKANİKLERİ VE KONTROL SINIFI (SavasMixin)
# Bu sınıf Oyun motorunun ana sınıfına eklenerek, tüm saldırı, kaçınma, iksir içme ve tur sistemlerini yönetir.
# ----------------------------------------------------------------------------------------------------
class SavasMixin:

    # ----------------------------------------------------------------------------------------------------
    # OYUNCU HAMLE (YETENEK) SEÇİM VE EKRAN YÖNETİMİ
    # ----------------------------------------------------------------------------------------------------
    def player_select_action(self, enemy):
        """
        Savaş esnasında ekrana yetenekleri, maliyetlerini ve hasar çarpanlarını yazdırır.
        Oyuncunun klavyeden yaptığı seçime göre bir aksiyon verisi (dictionary) oluşturup geri döndürür.
        Oluşturulan bu aksiyon bir sonraki aşamada (player_execute_action) işleme alınır.
        """
        oyuncu = self.oyuncu
        # Sersemleme kontrolü
        if oyuncu.durumlar["sersemleme"]:
            if not oyuncu.durumlar.get("sersemleme_kullanildi", False):
                cprint("SERSEMLEDIN! Hareket edemiyorsun.", Colors.PURPLE)
                oyuncu.durumlar["sersemleme_kullanildi"] = True
                return {"type": "skip"}
            else:
                oyuncu.durumlar["sersemleme"] = False
                oyuncu.durumlar["sersemleme_kullanildi"] = False

        sk   = oyuncu.yetenekler
        mult = oyuncu.yetenek_carpanlari
        ulti_color = Colors.PURPLE if enemy.durumlar.get("sersemleme") else Colors.GREY

        # --- SAVASCI ---
        if isinstance(oyuncu, Savasci):
            if oyuncu.adrenalin >= oyuncu.maks_adrenalin:
                cprint(">>> ADRENALIN DOLU! Saldırın kritik vuracak! <<<", "\033[38;5;208m")
            print(f"1. {sk[0]} (x{mult[0]:.1f})")
            print(f"2. {sk[1]} {Colors.YELLOW}(15 EP){Colors.RESET} (x{mult[1]:.1f})")
            print(f"3. {sk[2]} {Colors.BLUE}(20 MP){Colors.RESET}+{Colors.YELLOW}(25 EP){Colors.RESET} (x{mult[2]:.1f})")
            print(f"4. {sk[3]} {Colors.RED}(%20 HP){Colors.RESET} (x{mult[3]:.1f})")
            print(f"5. {sk[4]} {ulti_color}(ULTI - 40 MP+EP){Colors.RESET} (x{mult[4]:.1f})")
            print("6. Iksir Ic")
            print("7. Kac")
            c = input_colored("Hamlen: ")
            if c == "1":
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "2":
                if oyuncu.enerji >= 15:
                    oyuncu.enerji -= 15
                    return {"type": "attack", "mult": 1.5 * mult[1], "stun": True, "skill_idx": 1}
                cprint("Yetersiz Enerji!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "3":
                if oyuncu.mana >= 20 and oyuncu.enerji >= 25:
                    oyuncu.mana -= 20; oyuncu.enerji -= 25
                    return {"type": "attack", "mult": 2.5 * mult[2], "stun": True, "skill_idx": 2}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "4":
                cost = int(oyuncu.maks_can * 0.20)
                if oyuncu.can > cost:
                    oyuncu.can -= cost
                    return {"type": "attack", "mult": 2.0 * mult[3], "stun": True, "bleed": 2, "skill_idx": 3}
                cprint(f"\n{Colors.RED}!!! YETERLI CANIN YOK !!!{Colors.RESET}", Colors.RED)
                cprint(f"Gereken Can: {cost} HP (%20)", Colors.WHITE); wait_with_dots(count=1)
                return "RETRY"
            elif c == "5":
                if not enemy.durumlar.get("sersemleme"):
                    cprint("ULTI SADECE STUNLU RAKIBE ATILIR!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 40 and oyuncu.enerji >= 40:
                    oyuncu.mana -= 40; oyuncu.enerji -= 40
                    return {"type": "ulti", "mult": 5.0 * mult[4], "skill_idx": 4, "fill_adrenaline": True}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "6": return self.select_potion()
            elif c == "7": return {"type": "escape"}
            return "RETRY"

        # --- BUYUCU ---
        elif isinstance(oyuncu, Buyucu):
            print(f"1. {sk[0]} (x{mult[0]:.1f})")
            print(f"2. {sk[1]} {Colors.BLUE}(25 MP){Colors.RESET} - Yakar (x{mult[1]:.1f})")
            print(f"3. {sk[2]} {Colors.BLUE}(30 MP){Colors.RESET}+{Colors.YELLOW}(15 EP){Colors.RESET} - Yavaşlatır (x{mult[2]:.1f})")
            print(f"4. {sk[3]} {Colors.GREY}(GELİŞTİRİLİYOR){Colors.RESET}")
            print(f"5. {sk[4]} {ulti_color}(ULTI - 80 MP+30 EP){Colors.RESET} (x{mult[4]:.1f})")
            print("6. Iksir Ic"); print("7. Kac")
            c = input_colored("Hamlen: ")
            if c == "1":
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "2":
                if oyuncu.mana >= 25:
                    oyuncu.mana -= 25
                    return {"type": "attack", "mult": 1.8 * mult[1], "stun": True, "burn": True, "skill_idx": 1}
                cprint("Yetersiz Mana!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "3":
                if oyuncu.mana >= 30 and oyuncu.enerji >= 15:
                    oyuncu.mana -= 30; oyuncu.enerji -= 15
                    return {"type": "attack", "mult": 2.2 * mult[2], "stun": True, "slow": True, "skill_idx": 2}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "4":
                cprint("Bu yetenek şu an geliştiriliyor!", Colors.YELLOW); time.sleep(1); return "RETRY"
            elif c == "5":
                if not enemy.durumlar.get("sersemleme"):
                    cprint("ULTI SADECE STUNLU RAKIBE ATILIR!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 80 and oyuncu.enerji >= 30:
                    oyuncu.mana -= 80; oyuncu.enerji -= 30
                    return {"type": "ulti", "mult": 5.0 * mult[4], "skill_idx": 4}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "6": return self.select_potion()
            elif c == "7": return {"type": "escape"}
            return "RETRY"

        # --- HAYDUT ---
        elif isinstance(oyuncu, Haydut):
            print(f"1. {sk[0]} - %15 Çift Vuruş (x{mult[0]:.1f})")
            print(f"2. {sk[1]} {Colors.YELLOW}(30 EP){Colors.RESET} - %50 3x Hasar+15 Kanama (x{mult[1]:.1f})")
            print(f"3. {sk[2]} {Colors.BLUE}(20 MP){Colors.RESET}+{Colors.YELLOW}(25 EP){Colors.RESET} - 10 Zehir 3 Tur (x{mult[2]:.1f})")
            print(f"4. {sk[3]} {Colors.BLUE}(60 MP){Colors.RESET} - Yaniltma")
            print(f"5. {sk[4]} {ulti_color}(ULTI - 50 MP+80 EP){Colors.RESET} (x{mult[4]:.1f})")
            print("6. Iksir Ic"); print("7. Kac")
            c = input_colored("Hamlen: ")
            if c == "1":
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "double_hit": 0.15, "bleed": 5, "skill_idx": 0}
            elif c == "2":
                if oyuncu.enerji >= 30:
                    oyuncu.enerji -= 30
                    return {"type": "attack", "mult": 1.5 * mult[1], "stun": True, "backstab": True, "skill_idx": 1}
                cprint("Yetersiz Enerji!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "double_hit": 0.15, "bleed": 5, "skill_idx": 0}
            elif c == "3":
                if oyuncu.mana >= 20 and oyuncu.enerji >= 25:
                    oyuncu.mana -= 20; oyuncu.enerji -= 25
                    return {"type": "attack", "mult": 0.67 * mult[2], "stun": True, "poison": 10, "skill_idx": 2}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "double_hit": 0.15, "bleed": 5, "skill_idx": 0}
            elif c == "4":
                if oyuncu.durumlar.get("hiz_carpani_turlari", 0) > 0:
                    cprint("Bu yetenek zaten aktif!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 60:
                    oyuncu.mana -= 60
                    return {"type": "buff", "speed_mult": 2, "dodge_cap": 0.75, "duration": 2, "skill_idx": 3}
                cprint("Yetersiz Mana!", Colors.RED); time.sleep(1); return "RETRY"
            elif c == "5":
                if not enemy.durumlar.get("sersemleme"):
                    cprint("ULTI SADECE STUNLU RAKIBE ATILIR!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 50 and oyuncu.enerji >= 80:
                    oyuncu.mana -= 50; oyuncu.enerji -= 80
                    return {"type": "ulti", "mult": 5.0 * mult[4], "skill_idx": 4}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "double_hit": 0.15, "bleed": 5, "skill_idx": 0}
            elif c == "6": return self.select_potion()
            elif c == "7": return {"type": "escape"}
            return "RETRY"

        # --- TANK ---
        elif isinstance(oyuncu, Tank):
            print(f"1. {sk[0]} (x{mult[0]:.1f})")
            print(f"2. {sk[1]} {Colors.YELLOW}(20 EP){Colors.RESET} (x{mult[1]:.1f})")
            print(f"3. {sk[2]} {Colors.BLUE}(80 MP){Colors.RESET} - 3 Tur %30 Zirh + %25 Eksik HP Yenileme")
            print(f"4. {sk[3]} {Colors.YELLOW}(40 EP){Colors.RESET} - %50 Hasar Azaltma + %60 Yansitma")
            print(f"5. {sk[4]} {ulti_color}(ULTI - 35 MP+60 EP){Colors.RESET} (x{mult[4]:.1f})")
            print("6. Iksir Ic"); print("7. Kac")
            c = input_colored("Hamlen: ")
            if c == "1":
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "extra_stun": 0.10, "skill_idx": 0}
            elif c == "2":
                if oyuncu.enerji >= 20:
                    oyuncu.enerji -= 20
                    return {"type": "attack", "mult": 1.5 * mult[1], "stun": True, "skill_idx": 1}
                cprint("Yetersiz Enerji!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "3":
                if oyuncu.durumlar.get("yenilenme_turlari", 0) > 0:
                    cprint("Metanet zaten aktif!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 80:
                    oyuncu.mana -= 80
                    return {"type": "buff", "target": "self", "defense_boost": 3, "regen": 3, "skill_idx": 2}
                cprint("Yetersiz Mana!", Colors.RED); wait_with_dots(count=1); return "RETRY"
            elif c == "4":
                if oyuncu.enerji >= 40:
                    oyuncu.enerji -= 40
                    return {"type": "buff", "target": "self", "damage_reduction": 0.5, "reflect_buff": 1, "skill_idx": 3}
                cprint("Yetersiz Enerji!", Colors.RED); wait_with_dots(count=1); return "RETRY"
            elif c == "5":
                if not enemy.durumlar.get("sersemleme"):
                    cprint("ULTI SADECE STUNLU RAKIBE ATILIR!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 35 and oyuncu.enerji >= 60:
                    oyuncu.mana -= 35; oyuncu.enerji -= 60
                    return {"type": "ulti", "mult": 5.0 * mult[4], "skill_idx": 4}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "6": return self.select_potion()
            elif c == "7": return {"type": "escape"}
            return "RETRY"

        # --- VARSAYILAN ---
        else:
            print(f"1. {sk[0]} (x{mult[0]:.1f})")
            print(f"2. {sk[1]} {Colors.YELLOW}(20 EP){Colors.RESET} (x{mult[1]:.1f})")
            print(f"3. {sk[2]} {Colors.BLUE}(30 MP){Colors.RESET}+{Colors.YELLOW}(30 EP){Colors.RESET} (x{mult[2]:.1f})")
            print(f"4. {sk[3]} {ulti_color}(ULTI - 50 MP+EP){Colors.RESET} (x{mult[3]:.1f})")
            print("5. Iksir Ic")
            c = input_colored("Hamlen: ")
            if c == "1":
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "2":
                if oyuncu.enerji >= 20:
                    oyuncu.enerji -= 20
                    return {"type": "attack", "mult": 1.5 * mult[1], "stun": True, "skill_idx": 1}
                cprint("Yetersiz Enerji!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "3":
                if oyuncu.mana >= 30 and oyuncu.enerji >= 30:
                    oyuncu.mana -= 30; oyuncu.enerji -= 30
                    return {"type": "attack", "mult": 2.5 * mult[2], "stun": True, "skill_idx": 2}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "4":
                if not enemy.durumlar.get("sersemleme"):
                    cprint("ULTI SADECE STUNLU RAKIBE ATILIR!", Colors.RED); time.sleep(1); return "RETRY"
                if oyuncu.mana >= 50 and oyuncu.enerji >= 50:
                    oyuncu.mana -= 50; oyuncu.enerji -= 50
                    return {"type": "ulti", "mult": 5.0 * mult[3], "skill_idx": 3}
                cprint("Yetersiz Kaynak!", Colors.RED); wait_with_dots(count=1)
                return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}
            elif c == "5":
                return self.select_potion()
            return {"type": "attack", "mult": 1.0 * mult[0], "stun": True, "skill_idx": 0}

    def select_potion(self):
        """Savaş sırasında iksir seçimi."""
        cprint("HANGI IKSIR?", Colors.CYAN)
        available = [n for n, c in self.oyuncu.envanter.items() if c > 0]
        if not available:
            cprint("Cantanda hic iksir yok!", Colors.RED); time.sleep(1); return "RETRY"
        for i, name in enumerate(available):
            print(f"{i+1}. {name} (x{self.oyuncu.envanter[name]})")
        print("0. Iptal")
        sub = input_colored("Secim: ")
        if sub == "0": return "RETRY"
        try:
            idx = int(sub) - 1
            if 0 <= idx < len(available):
                return {"type": "potion", "item": available[idx]}
        except (ValueError, IndexError):
            pass
        return "RETRY"

    def player_execute_potion(self, item_name):
        """
        Oyuncunun envanterinden seçili iksiri harcayarak, anında ilgili statlarını (Can, Mana, Enerji vb.) doldurur.
        Taze Başlangıç gibi çok nadir iksirlerin özel mekaniklerini de kontrol eder.
        """
        if self.oyuncu.envanter.get(item_name, 0) <= 0:
            cprint(f"Cantanda {item_name} yok!", Colors.RED); return
        self.oyuncu.envanter[item_name] -= 1
        info = get_potion_info(item_name)
        if "Can İksiri" in item_name:
            self.oyuncu.iyiles(info["val"])
            cprint(f"{Colors.GREEN}>> {item_name} ictin. +{info['val']} HP{Colors.RESET}")
        elif "Mana İksiri" in item_name:
            self.oyuncu.mana_yenile(info["val"])
            cprint(f"{Colors.BLUE}>> {item_name} ictin. +{info['val']} MP{Colors.RESET}")
        elif "Enerji İksiri" in item_name:
            self.oyuncu.enerji_yenile(info["val"])
            cprint(f"{Colors.YELLOW}>> {item_name} ictin. +{info['val']} EP{Colors.RESET}")
        elif item_name == "Taze Başlangıç":
            self.oyuncu.can = self.oyuncu.maks_can
            self.oyuncu.mana = self.oyuncu.maks_mana
            self.oyuncu.enerji = self.oyuncu.maks_enerji
            cprint(f"{Colors.GREEN}>> Taze Başlangıç ictin. Tum barlar fullendi!{Colors.RESET}")
        elif "Dayanıklılık İksiri" in item_name:
            self.oyuncu.kalkan += info["val"]
            cprint(f"{Colors.WHITE}>> {item_name} ictin. +{info['val']} Kalkan!{Colors.RESET}")

    def player_execute_action(self, enemy, action_data):
        """
        player_select_action fonksiyonundan gelen aksiyon verisini (action_data) işleyerek,
        hasar verme, ulti atma, buff (güçlendirme) kazanma veya minyon çağırma gibi işlemleri anında gerçekleştirir.
        """
        atype = action_data["type"]
        if atype == "skip":
            return
        if atype == "attack":
            fx = {"skill_idx": action_data.get("skill_idx", 0)}
            for k in ["double_hit", "backstab", "burn", "slow", "poison", "bleed", "extra_stun"]:
                if k in action_data:
                    fx[k] = action_data[k]
            self.perform_attack(self.oyuncu, enemy, action_data["mult"],
                                chance_stun=action_data.get("stun", False), **fx)
        elif atype == "ulti":
            sidx = action_data.get("skill_idx", 3)
            cprint(f"--- ULTI: {self.oyuncu.yetenekler[sidx]} ---", Colors.PURPLE)
            self.perform_attack(self.oyuncu, enemy, action_data["mult"],
                                chance_stun=False, skill_idx=sidx)
            if not enemy.hayatta_mi():
                cprint("MUKEMMEL BITIRIS!", Colors.GREEN)
                self.oyuncu.mana_yenile(25)
                self.oyuncu.enerji_yenile(25)
                self.oyuncu.altin += int(enemy.altin_odulu * 0.1)
        elif atype == "buff":
            sidx = action_data.get("skill_idx", 0)
            cprint(f"--- YETENEK: {self.oyuncu.yetenekler[sidx]} ---", Colors.CYAN)
            if "defense_boost" in action_data:
                self.oyuncu.durumlar["savunma_artisi_turlari"] = action_data["defense_boost"]
                cprint(f">>> {self.oyuncu.ad} zirhini guclendirdi! (3 Tur) <<<", Colors.GREEN)
            if "regen" in action_data:
                self.oyuncu.durumlar["yenilenme_turlari"] = action_data["regen"]
                cprint(f">>> {self.oyuncu.ad} yenilenmeye basladi! (3 Tur) <<<", Colors.GREEN)
            if "damage_reduction" in action_data:
                self.oyuncu.durumlar["hasar_azaltma"] = action_data["damage_reduction"]
                cprint(f">>> {self.oyuncu.ad} siper aldi! <<<", Colors.YELLOW)
            if "reflect_buff" in action_data:
                self.oyuncu.durumlar["yansitma_turlari"] = action_data["reflect_buff"]
                cprint(f">>> {self.oyuncu.ad} yansitma gucunu artirdi! <<<", Colors.CYAN)
            if "speed_mult" in action_data:
                self.oyuncu.durumlar["hiz_carpani_turlari"] = action_data["duration"]
                self.oyuncu.durumlar["kacinma_siniri_gecersiz"] = action_data["dodge_cap"]
                cprint(f">>> {self.oyuncu.ad} inanilmaz hizlandi! (Hiz x{action_data['speed_mult']}) <<<", Colors.CYAN)
        elif atype == "summon":
            self._create_summon()

    # ----------------------------------------------------------------------------------------------------
    # YAPAY ZEKA (DÜŞMAN) KARAR VE SALDIRI SİSTEMİ
    # ----------------------------------------------------------------------------------------------------
    def turn_enemy(self, enemy):
        """
        Düşmanın sırası geldiğinde hangi eylemi yapacağını belirler. Sersemlemişse turunu atlar. 
        Oyuncunun çağırdığı bir asker varsa önceliği ona verir. Sınıflarına (Örn: Kurt, Slime) göre özel efektler uygular.
        """
        if enemy.durumlar.get("sersemleme"):
            if not enemy.durumlar.get("sersemleme_kullanildi"):
                cprint(f"{enemy.ad} sersemledi, saldiramiyor!", Colors.PURPLE)
                enemy.durumlar["sersemleme_kullanildi"] = True
                return
            enemy.durumlar["sersemleme"] = False
            enemy.durumlar["sersemleme_kullanildi"] = False

        target = self.oyuncu
        if self.oyuncu.cagrilan and self.oyuncu.cagrilan.hayatta_mi():
            target = self.oyuncu.cagrilan
            cprint(f">>> {enemy.ad} ASKERINE SALDIRIYOR! <<<", Colors.YELLOW)

        if isinstance(enemy, Worm):
            hits = random.randint(1, 3)
            cprint(f"{enemy.ad} {hits} kez saldiriyor!", Colors.RED)
            for _ in range(hits):
                if not target.hayatta_mi(): break
                self.perform_attack(enemy, target, 0.6)
                if random.random() < 0.2 and target == self.oyuncu:
                    self.oyuncu.zehir_uygula(2, ekstra_hasar=0)
        elif isinstance(enemy, Wolf):
            self.perform_attack(enemy, target, 1.0)
            if target == self.oyuncu: self.oyuncu.kanama_uygula(yukler=2, sure=3)
        elif isinstance(enemy, Scorpion):
            self.perform_attack(enemy, target, 0.8)
            if random.random() < 0.6 and target == self.oyuncu: self.oyuncu.zehir_uygula(4)
        elif isinstance(enemy, Zombie):
            self.perform_attack(enemy, target, 1.0)
            if random.random() < 0.3 and target == self.oyuncu: self.oyuncu.zehir_uygula(3)
        elif isinstance(enemy, AtesRuhu):
            self.perform_attack(enemy, target, 1.2)
            if target == self.oyuncu: self.oyuncu.yakma_uygula(3)
        elif isinstance(enemy, BuzRuhu):
            self.perform_attack(enemy, target, 1.2)
            if target == self.oyuncu: self.oyuncu.dondurma_uygula(2)
        elif isinstance(enemy, Basilisk):
            self.perform_attack(enemy, target, 0.7)
            if target == self.oyuncu: self.oyuncu.zehir_uygula(5)
        elif isinstance(enemy, Slime):
            self.perform_attack(enemy, target, 0.8)
            if target == self.oyuncu:
                efekt = {"Ateş": lambda: self.oyuncu.yakma_uygula(2),
                         "Zehir": lambda: self.oyuncu.zehir_uygula(3),
                         "Düz":   lambda: self.oyuncu.yavaslatma_uygula(2),
                         "Su":    lambda: self.oyuncu.yavaslatma_uygula(1)}
                efekt.get(enemy.tür, lambda: None)()
        else:
            self.perform_attack(enemy, target, 1.0)

    # ----------------------------------------------------------------------------------------------------
    # ORTAK HASAR HESAPLAMA VE ÇATIŞMA MOTORU
    # ----------------------------------------------------------------------------------------------------
    def perform_attack(self, attacker, defender, multiplier, chance_stun=False, **fx):
        """
        Herhangi bir yetenek, saldırı veya büyü gerçekleştiğinde tüm hesaplamaların (Kaçınma, Zırh, Kritik vb.) 
        işlendiği ana merkez fonksiyondur. Statüler ve sınıflara özel hasar çarpanları burada devreye girer.
        """
        time.sleep(0.5)
        damage = int(attacker.saldiri * multiplier)

        # Savaşçı adrenalin sistemi
        if isinstance(attacker, Savasci) and attacker == self.oyuncu:
            if fx.get("skill_idx") == 3:
                damage = int(attacker.adrenalinsiz_saldiri_getir() * multiplier)
            if attacker.adrenalin_saldirisi_kullan():
                damage = int(damage * 1.5)
                cprint(">>> ADRENALIN KRITIK VURUŞ! 1.5x HASAR! <<<", "\033[38;5;208m")
            gain_map = {0: 5, 1: 10, 2: 20, 3: 50, 4: 100}
            attacker.adrenalin_kazan(gain_map.get(fx.get("skill_idx", 0), 5))

        # Haydut kritik sistemi
        if isinstance(attacker, Haydut) and attacker == self.oyuncu:
            if attacker.kritik_vurus_kontrol():
                damage = int(damage * attacker.kritik_carpani)
                cprint(">>> KRITIK VURUŞ! 1.5x HASAR! <<<", Colors.YELLOW)

        # Çift vuruş
        if fx.get("double_hit") and attacker == self.oyuncu:
            if random.random() < fx["double_hit"]:
                cprint(">>> ÇIFT VURUŞ! <<<", Colors.PURPLE)
                self._execute_single_attack(attacker, defender, damage, chance_stun, fx)
                if defender.hayatta_mi():
                    self._execute_single_attack(attacker, defender, damage, chance_stun, fx)
                return damage

        # Backstab
        if fx.get("backstab") and attacker == self.oyuncu:
            if random.random() < 0.50:
                damage = int(damage * 3)
                cprint(">>> SIRTINDAN BICAKLA! 3x HASAR! <<<", Colors.RED)
                defender.kanama_uygula(yukler=3, sure=3)
            else:
                cprint(">>> Sirtindan bicaklama basarisiz! Normal hasar. <<<", Colors.GREY)

        return self._execute_single_attack(attacker, defender, damage, chance_stun, fx)

    def _execute_single_attack(self, attacker, defender, damage, chance_stun, fx):
        # Kaçınma sistemi
        if defender.hiz > attacker.hiz:
            speed_diff = defender.hiz - attacker.hiz
            base_cap = 0.60 if hasattr(defender, "tür") else 0.30
            if defender.durumlar.get("kacinma_siniri_gecersiz", 0) > 0:
                base_cap = defender.durumlar["kacinma_siniri_gecersiz"]
            dodge = min(base_cap, speed_diff * 0.02)
            if random.random() < dodge:
                cprint(f"{Colors.CYAN}>> {defender.ad} %{int(dodge*100)} şansla sidirdi!{Colors.RESET}")
                return 0

        def_val = defender.savunma
        if defender.durumlar.get("savunma_artisi_turlari", 0) > 0:
            def_val *= 1.30

        if def_val >= damage:
            actual = max(1, int(damage * 0.20))
            color = Colors.GREEN if attacker == self.oyuncu else Colors.RED
            Sound.hit()
            battle_print(f"{attacker.ad} vurdu -> {defender.ad} ({actual} Hasar - Zirh Engelledi)", color)
            defender.gercek_hasar_al(actual)
        else:
            actual = defender.hasar_al(damage)
            color = Colors.GREEN if attacker == self.oyuncu else Colors.RED
            if attacker == self.oyuncu:
                Sound.attack()
            else:
                Sound.enemy_attack()
            battle_print(f"{attacker.ad} vurdu -> {defender.ad} ({actual} Hasar)", color)
            # Lifesteal (Boss)
            if hasattr(attacker, "lifesteal") and attacker.lifesteal > 0:
                heal = int(actual * attacker.lifesteal)
                attacker.can = min(attacker.maks_can, attacker.can + heal)
                battle_print(f"{attacker.ad} can caldi: +{heal} HP", Colors.RED)

        # Tank yansıtma
        if isinstance(defender, Tank) and defender == self.oyuncu:
            reflected = defender.hasar_yansit(actual)
            if reflected > 0:
                attacker.gercek_hasar_al(reflected)

        # Oyuncu özel efektler
        if attacker == self.oyuncu:
            if attacker.degistiriciler["zehir_hasari"] > 0:
                defender.zehir_uygula(3, ekstra_hasar=attacker.degistiriciler["zehir_hasari"])
            if attacker.degistiriciler["kanama_hasari"] > 0:
                defender.kanama_uygula(yukler=1, sure=3)
            total_stun = attacker.degistiriciler["sersemletme_sansi"] + (0.20 if chance_stun else 0)
            if fx.get("extra_stun"): total_stun += fx["extra_stun"]
            if random.random() < total_stun: defender.sersemlet_uygula()
            if fx.get("bleed"):  defender.kanama_uygula(yukler=fx["bleed"], sure=3)
            if fx.get("poison"): defender.zehir_uygula(sure=3, ekstra_hasar=fx["poison"])
            if fx.get("burn"):
                defender.yakma_uygula(3)
                cprint(">>> ALEV TOPU! Düşman yanıyor! <<<", Colors.RED)
            if fx.get("slow"):
                defender.dondurma_uygula(2)
                cprint(">>> BUZ OKU! Düşman dondu! <<<", Colors.CYAN)
        elif chance_stun and random.random() < 0.20:
            defender.sersemlet_uygula()

        return actual

    # ----------------------------------------------------------------------------------------------------
    # ANA SAVAŞ DÖNGÜSÜ (BATTLE LOOP)
    # ----------------------------------------------------------------------------------------------------
    def _run_battle_loop(self, enemy):
        """
        Savaş bitene (taraflardan biri ölene) kadar devam eden sonsuz döngü. 
        Oyuncu hızı ve düşman hızını karşılaştırıp (Hızlı olan ilk vurur) tur sırasını düzenler.
        """
        self.battle_log = []
        while self.oyuncu.hayatta_mi() and enemy.hayatta_mi():
            import os
            os.system("cls" if os.name == "nt" else "clear")
            battle_ui(self.oyuncu, enemy, self.battle_log)
            self.battle_log = []

            action_data = self.player_select_action(enemy)
            if action_data == "RETRY": continue

            if action_data["type"] == "escape":
                escape = max(0.1, min(0.95, 0.5 + (self.oyuncu.hiz - enemy.hiz) * 0.05))
                battle_print(f"\nKacmaya calisiyorsun... (Sans: %{int(escape*100)})", Colors.CYAN, delay=0.4)
                time.sleep(0.6)
                if random.random() < escape:
                    Sound.escape_success()
                    battle_print("BASARILI! Kactin!", Colors.GREEN, delay=0.3); time.sleep(1); return "escaped"
                crit = int(enemy.saldiri * 1.5)
                self.oyuncu.gercek_hasar_al(crit)
                energy_loss = int(self.oyuncu.maks_enerji * 0.20)
                self.oyuncu.enerji = max(0, self.oyuncu.enerji - energy_loss)
                Sound.enemy_attack()
                battle_print(f"KACAMADIN! -{crit} HP (Kritik) -{energy_loss} EP", Colors.RED, delay=0.3)
                time.sleep(1.5)
                self.turn_enemy(enemy); continue

            # Gereksiz ekran temizleme ve UI tekrarı kaldırıldı, mesajlar menünün altına eklenecek.



            if action_data["type"] == "potion":
                self.player_execute_potion(action_data["item"])
                time.sleep(1)
                if enemy.hayatta_mi():
                    if hasattr(enemy, "ozel_mekanik"):
                        enemy.ozel_mekanik(self.oyuncu)
                    self.turn_enemy(enemy)
            elif self.oyuncu.hiz >= enemy.hiz:
                cprint(f"{Colors.GREEN}>> SEN DAHA HIZLISIN!{Colors.RESET}")
                self.player_execute_action(enemy, action_data)
                if enemy.hayatta_mi():
                    if hasattr(enemy, "ozel_mekanik"):
                        enemy.ozel_mekanik(self.oyuncu)
                    self.turn_enemy(enemy)
            else:
                cprint(f"{Colors.RED}>> {enemy.ad} DAHA HIZLI!{Colors.RESET}")
                if hasattr(enemy, "ozel_mekanik"):
                    enemy.ozel_mekanik(self.oyuncu)
                self.turn_enemy(enemy)
                if self.oyuncu.hayatta_mi():
                    self.player_execute_action(enemy, action_data)

            self.oyuncu.durum_efektlerini_isle()
            if enemy.hayatta_mi(): enemy.durum_efektlerini_isle()
            self._apply_class_regen()

            # Asker saldırısı
            if self.oyuncu.cagrilan:
                if self.oyuncu.cagrilan.hayatta_mi():
                    dmg = self.oyuncu.cagrilan.saldiri
                    cprint(f">>> ASKER SALDIRIYOR: {enemy.ad} -{dmg} HP", Colors.CYAN)
                    enemy.hasar_al(dmg)
                    if random.random() < 0.10: enemy.sersemlet_uygula()
                else:
                    cprint(">>> Askerin yok edildi! <<<", Colors.RED)
                    self.oyuncu.cagrilan = None
            time.sleep(1.5) # Savaş akışını yavaşlatmak için artırıldı
        return "done"

    def _normalize_enemy_power(self, enemy, ratio=ENEMY_POWER_RATIO):
        """
        Düşmanların statlarını oyuncunun genel güç skoruna (Can, Saldırı, Savunma, Hız ağırlıklı bir formülle) göre oranlayarak düzenler.
        Böylece düşmanların kendi doğası (örneğin goblinler her zaman hızlı, golemler hep zırhlıdır) korunarak adil bir zorluk seviyesi yakalanır.
        """
        # Oyuncunun ağırlıklı 'toplam güç' skoru
        oyuncu_gucu = (
            self.oyuncu.maks_can * 0.30 +
            self.oyuncu.saldiri  * 0.40 +
            self.oyuncu.savunma  * 0.20 +
            self.oyuncu.hiz      * 0.10
        )
        # Düşmanın mevcut güç skoru
        dusman_gucu = (
            enemy.maks_can * 0.30 +
            enemy.saldiri  * 0.40 +
            enemy.savunma  * 0.20 +
            enemy.hiz      * 0.10
        )
        if dusman_gucu <= 0:
            return
        # Tek ölçek faktörü: kişilik oranları korunur!
        olcek = (oyuncu_gucu * ratio) / dusman_gucu
        enemy.maks_can = enemy.can = max(10, int(enemy.maks_can * olcek))
        enemy.saldiri  = max(1,  int(enemy.saldiri  * olcek))
        enemy.savunma  = max(0,  int(enemy.savunma  * olcek))
        enemy.hiz      = max(1,  int(enemy.hiz      * olcek))
        enemy.temel_hiz = enemy.hiz

    def _get_enemy_level(self):
        """Düşman seviyesini oyuncu seviyesine göre belirler. (Artık hep oyuncuyla aynı)"""
        return max(1, self.oyuncu.seviye)

    def battle_phase(self):
        """Normal düşman savaşı."""
        enemy_types = [Skeleton, Goblin, Zombie, Wolf, Golem, Worm, Scorpion,
                       AtesRuhu, BuzRuhu, Basilisk, Slime]
        enemy_type = random.choice(enemy_types)
        
        lvl = self._get_enemy_level()
        enemy = rastgele_slime_getir(lvl) if enemy_type == Slime else enemy_type(lvl)

        # Düşman gücünü, oyuncu ile arasındaki seviye farkına göre dinamik olarak hesaplıyor ve esnetiyoruz.
        level_diff = lvl - self.oyuncu.seviye
        adjusted_ratio = ENEMY_POWER_RATIO + (level_diff * 0.08)
        self._normalize_enemy_power(enemy, ratio=max(0.70, adjusted_ratio))

        # Ödülleri seviyeye göre ölçekle
        reward_mult = 1.0 + (lvl * 0.05)
        enemy.altin_odulu = max(5,  int(enemy.altin_odulu * reward_mult))
        enemy.tp_odulu    = max(10, int(enemy.tp_odulu    * reward_mult))

        roll = random.random()
        if roll < CHAMPION_CHANCE:
            enemy = ChampionEnemy(enemy)
            cprint(f"\n!!! {enemy.ad} KARSINDA !!!", Colors.PURPLE)
        elif roll < GOLDEN_CHANCE:
            enemy = GoldenEnemy(enemy)
            cprint(f"\n!!! {enemy.ad} KARSINDA !!!", Colors.YELLOW)
        else:
            cprint(f"\nSAVAS BASLADI: {enemy.ad}", Colors.RED)
        time.sleep(1)

        result = self._run_battle_loop(enemy)
        if result != "escaped":
            self.handle_battle_end(enemy)

    def boss_battle(self, boss_class):
        """Boss savaşı."""
        boss = boss_class(self.oyuncu.seviye)
        # Bosslar normal düşmanlardan daha yüksek güç çarpanlarıyla gelerek ektra dayanıklı yaratılır (uzun süren savaşlar hedeflenir).
        self._normalize_enemy_power(boss, ratio=BOSS_POWER_RATIO)
        bonus_hp = int(self.oyuncu.maks_can * 1.5)
        boss.maks_can += bonus_hp
        boss.can       = boss.maks_can
        Sound.boss_intro()
        boss.bos_giris()

        self._run_battle_loop(boss)
        self.handle_battle_end(boss)

    def handle_battle_end(self, enemy):
        import os
        os.system("cls" if os.name == "nt" else "clear")
        if self.oyuncu.hayatta_mi():
            gold_bonus = 1.0 + (self.oyuncu.seviye * 0.04)
            gold = int(enemy.altin_odulu * gold_bonus)
            battle_print(f"\nKAZANDIN: +{enemy.tp_odulu} XP, +{gold} Altin", Colors.GREEN, delay=0.3)
            self.oyuncu.tecrube += enemy.tp_odulu
            self.oyuncu.altin   += gold
            if hasattr(enemy, "patron_mu") and enemy.patron_mu:
                self.drop_boss_item(enemy)
            else:
                self.drop_item()
            
            # Tecrübe puanı (TP) sınırı geçerse ardışık seviye atlamaları kontrolü (TP fazlasının boşa gitmemesi için)
            while self.oyuncu.tecrube >= (self.oyuncu.seviye * 25):
                tecrube_gereksinimi = self.oyuncu.seviye * 25
                self.oyuncu.tecrube -= tecrube_gereksinimi
                self.oyuncu.seviye_atla()

        else:
            Sound.death()
            battle_print("\nOLDUN...", Colors.RED, delay=0.5)
        wait_with_dots()

    # ----------------------------------------------------------------------------------------------------
    # SINIF/UZMANLIK GÜÇLENDİRİCİ YARDIMCI FONKSİYONLAR
    # ----------------------------------------------------------------------------------------------------
    def _apply_class_regen(self):
        oyuncu = self.oyuncu
        if isinstance(oyuncu, Buyucu):
            regen = 5 if (oyuncu.cagrilan and oyuncu.cagrilan.hayatta_mi()) else 10
            oyuncu.mana_yenile(regen)
            oyuncu.enerji_yenile(5)
        elif isinstance(oyuncu, Haydut):
            oyuncu.mana_yenile(5)
            oyuncu.enerji_yenile(10)
        else:
            oyuncu.mana_yenile(5)
            oyuncu.enerji_yenile(5)

    def _create_summon(self):
        lv = self.oyuncu.seviye
        hp  = 160 + (lv - 1) * 50
        dfs = 8   + (lv - 1) * 4
        
        summon_name = "Golem" if isinstance(self.oyuncu, Buyucu) else "Sihirli Nöbetçi"
        
        self.oyuncu.cagrilan = Entity(
            ad=summon_name,
            can=hp, maks_can=hp,
            mana=0, maks_mana=0, enerji=0, maks_enerji=0,
            saldiri=max(1, int(self.oyuncu.saldiri / 2)),
            savunma=dfs,
            hiz=self.oyuncu.hiz
        )
        cprint(f">>> {self.oyuncu.ad} bir {summon_name.upper()} cagirdi! (HP:{hp} ZIRH:{dfs}) <<<", Colors.CYAN)
        cprint("Bu tur baska bir sey yapamadin.", Colors.GREY)
        time.sleep(1)
