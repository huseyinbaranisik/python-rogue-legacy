from utils import Colors, cprint, print_slow, print_rainbow_slow, Sound
from entity import Entity


class Player(Entity):
    def __init__(self, ad, rol_adi, can, mana, enerji, saldiri, savunma, hiz, yetenekler):
        super().__init__(ad=ad,
                         can=can, maks_can=can,
                         mana=mana, maks_mana=mana,
                         enerji=enerji, maks_enerji=enerji,
                         saldiri=saldiri, savunma=savunma, hiz=hiz)
        self.rol              = rol_adi
        self.yetenekler       = yetenekler
        self.yetenek_carpanlari = [1.0] * 5
        self.altin            = 0
        self.tecrube          = 0
        self.seviye           = 1
        self.kat              = 1
        self.yetenek_puanlari = 0
        self.envanter         = {"Temel Can İksiri": 3, "Temel Mana İksiri": 2, "Temel Enerji İksiri": 2}
        self.ekipman          = {"silah": None, "zirh": None, "aksesuar": None}
        self.ekipman_envanteri = []
        self.cagrilan         = None
        self.temel_istatistikler = {
            "maks_can": can, "maks_mana": mana, "maks_enerji": enerji,
            "saldiri": saldiri, "savunma": savunma, "hiz": hiz,
        }

    def _exp_bar(self, width=20):
        """EXP barı: yeşilden sarıya RPG tarzı."""
        gerekli = self.seviye * 25
        doluluk = min(1.0, self.tecrube / gerekli)
        dolu = int(doluluk * width)
        bos  = width - dolu
        # Yeşil doluluk, sarı kalan hedef, gri boş
        bar = (
            f"{Colors.GREEN}{'█' * dolu}{Colors.RESET}"
            f"{Colors.GREY}{'░' * bos}{Colors.RESET}"
        )
        return f"[{bar}] {self.tecrube}/{gerekli}"

    def istatistikleri_goster(self):
        cprint(f"\n--- {self.ad} | {self.rol} | Seviye {self.seviye} ---", Colors.CYAN)
        cprint(f"CAN: {self.can}/{self.maks_can}", Colors.RED,    end="  |  ")
        cprint(f"MANA: {self.mana}/{self.maks_mana}", Colors.BLUE, end="  |  ")
        cprint(f"ENERJI: {self.enerji}/{self.maks_enerji}", Colors.YELLOW)
        cprint(f"SALDIRI: {self.saldiri}  |  SAVUNMA: {self.savunma}  |  HIZ: {self.hiz}", Colors.WHITE)
        cprint(f"ALTIN: {self.altin}  |  KAT: {self.kat}", Colors.YELLOW)
        # EXP Bar
        print(f"{Colors.YELLOW} EXP {Colors.RESET}{self._exp_bar()}  "
              f"{Colors.PURPLE}Yetenek Puanı: {self.yetenek_puanlari}{Colors.RESET}")
        s = self.ekipman["silah"].get_colored_name()    if self.ekipman["silah"]    else "Yok"
        z = self.ekipman["zirh"].get_colored_name()     if self.ekipman["zirh"]     else "Yok"
        a = self.ekipman["aksesuar"].get_colored_name() if self.ekipman["aksesuar"] else "Yok"
        cprint(f"\nSilah: {s} | Zirh: {z} | Aksesuar: {a}", Colors.GREY)
        cprint("-" * 50, Colors.CYAN)

    def _normalize_slot(self, item_type):
        return {"weapon": "silah", "armor": "zirh", "accessory": "aksesuar"}.get(item_type, item_type)

    def esya_kuşan(self, esya):
        slot = self._normalize_slot(esya.item_type)
        if self.ekipman[slot]:
            self.esya_cıkar(slot)
        self.ekipman[slot] = esya
        cprint(f"{esya.get_colored_name()} kusanildi!", Colors.GREEN)
        self.istatistikleri_hesapla()

    def esya_cıkar(self, slot):
        if self.ekipman[slot]:
            esya = self.ekipman[slot]
            self.ekipman_envanteri.append(esya)
            self.ekipman[slot] = None
            cprint(f"{esya.get_colored_name()} cikarildi.", Colors.GREY)
        self.istatistikleri_hesapla()

    def istatistikleri_hesapla(self):
        # Temel statları sıfırla
        t = self.temel_istatistikler
        self.maks_can  = t["maks_can"]
        self.maks_mana = t["maks_mana"]
        self.maks_enerji = t["maks_enerji"]
        self.saldiri   = t["saldiri"]
        self.savunma   = t["savunma"]
        self.hiz       = t["hiz"]
        self.degistiriciler = {"zehir_hasari": 0, "kanama_hasari": 0, "sersemletme_sansi": 0}

        # Stat -> alan eşleme
        stat_map = {
            "hp":        ("maks_can",    None),
            "mana":      ("maks_mana",   None),
            "energy":    ("maks_enerji", None),
            "attack":    ("saldiri",     None),
            "defense":   ("savunma",     None),
            "speed":     ("hiz",         None),
            "poison_dmg":  (None, "zehir_hasari"),
            "bleed_dmg":   (None, "kanama_hasari"),
            "stun_chance": (None, "sersemletme_sansi"),
        }
        for esya in self.ekipman.values():
            if esya:
                for stat, val in esya.stats.items():
                    if stat in stat_map:
                        attr, mod = stat_map[stat]
                        if attr:   setattr(self, attr, getattr(self, attr) + val)
                        elif mod:  self.degistiriciler[mod] += val

        self.temel_hiz = self.hiz
        self.can = min(self.can, self.maks_can)

    def seviye_atla(self):
        self.seviye        += 1
        self.yetenek_puanlari += 1
        incs = self.seviye_artıslarını_getir()
        for key, field in [("hp","maks_can"),("mana","maks_mana"),("energy","maks_enerji"),
                            ("attack","saldiri"),("defense","savunma"),("speed","hiz")]:
            self.temel_istatistikler[field] += incs[key]
        self.istatistikleri_hesapla()
        self.can = self.maks_can; self.mana = self.maks_mana; self.enerji = self.maks_enerji

        # --- Sarı level-up animasyonu ---
        Sound.level_up()
        import time; time.sleep(0.2)
        cprint(f"\n★★★ TEBRIKLER! {self.seviye}. SEVIYEYE ULASTIN! ★★★", Colors.YELLOW, slow=True)
        cprint(
            f"+{incs['hp']} CAN  +{incs['mana']} MANA  +{incs['energy']} ENERJI  "
            f"+{incs['attack']} ATK  +{incs['defense']} DEF  +{incs['speed']} HIZ",
            Colors.YELLOW, slow=True
        )
        cprint("★ +1 YETENEK PUANI KAZANDIN! ★", Colors.YELLOW, slow=True)
        cprint("Tazelendiğini hissettin.", Colors.GREEN, slow=True)
        time.sleep(0.5)

    def seviye_artıslarını_getir(self):
        return {"hp": 30, "mana": 10, "energy": 5, "attack": 6, "defense": 3, "speed": 1}

    def istatistik_arttır(self, stat_adi):
        if self.yetenek_puanlari <= 0:
            cprint("Yeterli yetenek puanin yok!", Colors.RED); return False
        arttir = {
            "max_hp":     ("maks_can",    25),
            "max_mana":   ("maks_mana",   15),
            "max_energy": ("maks_enerji", 10),
            "attack":     ("saldiri",      5),
            "defense":    ("savunma",      3),
            "speed":      ("hiz",          2),
        }
        if stat_adi not in arttir: return False
        field, amount = arttir[stat_adi]
        self.temel_istatistikler[field] += amount
        self.yetenek_puanlari -= 1
        self.istatistikleri_hesapla()
        cprint(f"{stat_adi.upper()} gelistirildi! (Kalan Puan: {self.yetenek_puanlari})", Colors.GREEN)
        return True
