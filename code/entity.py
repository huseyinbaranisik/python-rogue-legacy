import random
from utils import Colors, cprint


class Entity:
    """Oyundaki her canlının temel yapı taşı. (Oyuncu veya Düşman)"""

    def __init__(self, ad, can, maks_can, mana, maks_mana, enerji, maks_enerji,
                 saldiri, savunma, hiz):
        self.ad          = ad
        self.can         = can
        self.maks_can    = maks_can
        self.mana        = mana
        self.maks_mana   = maks_mana
        self.enerji      = enerji
        self.maks_enerji = maks_enerji
        self.saldiri     = saldiri
        self.savunma     = savunma
        self.hiz         = hiz
        self.temel_hiz   = hiz
        self.kalkan      = 0

        self.durumlar = {
            "zehir": 0, "yanma": 0, "donma": 0, "yavaslama": 0,
            "kanama_yukleri": 0, "kanama_turlari": 0,
            "sersemleme": False, "sersemleme_kullanildi": False,
            "savunma_artisi_turlari": 0, "hasar_azaltma": 0,
            "yansitma_turlari": 0, "yenilenme_turlari": 0,
            "hiz_carpani_turlari": 0, "kacinma_siniri_gecersiz": 0,
        }
        self.degistiriciler = {
            "zehir_hasari": 0, "kanama_hasari": 0, "sersemletme_sansi": 0,
        }

    def hayatta_mi(self):
        return self.can > 0

    # ----------------------------------------------------------------------------------------------------
    # STATÜ VE DURUM EFEKTLERİ UYGULAMA METOTLARI
    # Bu metotlar, karakterin veya düşmanın üzerinde geçici yan etkiler (Örn: zehir, yanma, donma) bırakır.
    # ----------------------------------------------------------------------------------------------------
    def zehir_uygula(self, sure, ekstra_hasar=0):
        self.durumlar["zehir"] = max(self.durumlar["zehir"], sure)
        cprint(f"> {self.ad} ZEHIRLENDI! ({sure} tur)", Colors.GREEN)

    def yakma_uygula(self, sure):
        self.durumlar["yanma"] = max(self.durumlar["yanma"], sure)
        cprint(f"> {self.ad} YANIYOR! ({sure} tur)", Colors.RED)

    def dondurma_uygula(self, sure):
        self.durumlar["donma"]     = max(self.durumlar["donma"], sure)
        self.durumlar["yavaslama"] = 0
        cprint(f"> {self.ad} DONDU! Hiz %50 azaldi! ({sure} tur)", Colors.CYAN)

    def yavaslatma_uygula(self, sure):
        if self.durumlar["donma"] <= 0:
            self.durumlar["yavaslama"] = max(self.durumlar["yavaslama"], sure)
            cprint(f"> {self.ad} YAVASLADI! Hiz %30 azaldi! ({sure} tur)", Colors.WHITE)

    def kanama_uygula(self, yukler=1, sure=2):
        self.durumlar["kanama_yukleri"] += yukler
        self.durumlar["kanama_turlari"] = max(self.durumlar["kanama_turlari"], sure)
        cprint(f"> {self.ad} KANIYOR! (Yuk: {self.durumlar['kanama_yukleri']})", Colors.RED)

    def sersemlet_uygula(self):
        if not self.durumlar["sersemleme"]:
            self.durumlar["sersemleme"]           = True
            self.durumlar["sersemleme_kullanildi"] = False
            cprint(f"> {self.ad} SERSEMLEDI!", Colors.PURPLE)

    # ----------------------------------------------------------------------------------------------------
    # TUR SONU BİLGİSAYAR (MOTOR) HESAPLAMALARI
    # ----------------------------------------------------------------------------------------------------
    def durum_efektlerini_isle(self):
        """
        Savaşta her tur bittikten sonra çağrılır. 
        Karakterin üzerinde kalan zehir, yanma gibi statülerin süresini 1 tur azaltır ve 
        eğer etki hala aktifse kalıcı gerçek hasar olarak canından eksiltir.
        """
        d = self.durumlar

        # Hız güncelleme
        yeni_hiz = self.temel_hiz
        if d["donma"] > 0:       yeni_hiz = int(yeni_hiz * 0.5)
        elif d["yavaslama"] > 0: yeni_hiz = int(yeni_hiz * 0.7)
        self.hiz = yeni_hiz

        # Efektlerin savaş sırasında sonsuza dek sürmemesi için tur sayaçlarını birer birer düşürür
        for key in ["zehir", "yanma", "donma", "yavaslama",
                    "kanama_turlari", "yenilenme_turlari",
                    "savunma_artisi_turlari", "yansitma_turlari"]:
            if d[key] > 0:
                d[key] -= 1

        # Süresi henüz bitmemiş olan aktif kötücül etkilerin (zehir, yanma, kanama) hasarlarını can barından düşer
        if d["zehir"] > 0:
            hasar = int(self.maks_can * 0.02) + 5
            self.gercek_hasar_al(hasar)
            cprint(f"> ZEHIR: {self.ad} -{hasar} CAN", Colors.GREEN)

        if d["yanma"] > 0:
            hasar = int(self.maks_can * 0.03) + 10
            self.gercek_hasar_al(hasar)
            cprint(f"> YANMA: {self.ad} -{hasar} CAN", Colors.RED)

        if d["kanama_turlari"] > 0:
            hasar = 5 * d["kanama_yukleri"]
            self.gercek_hasar_al(hasar)
            cprint(f"> KANAMA: {self.ad} -{hasar} CAN", Colors.RED)

        if d["yenilenme_turlari"] > 0:
            miktar = max(10, int((self.maks_can - self.can) * 0.25))
            self.iyiles(miktar)
            cprint(f"> YENILENME: {self.ad} +{miktar} CAN", Colors.GREEN)

        if d["kanama_turlari"] == 0:
            d["kanama_yukleri"] = 0

        if d.get("hiz_carpani_turlari", 0) > 0:
            d["hiz_carpani_turlari"] -= 1
            if d["hiz_carpani_turlari"] == 0:
                d["kacinma_siniri_gecersiz"] = 0

        d["hasar_azaltma"] = 0

    # ----------------------------------------------------------------------------------------------------
    # ANA CAN, ZIRH VE HASAR HESAPLAMA METOTLARI
    # Zırh direncine bağlı hasar kırılma, kalkan engellemesi veya saf (gerçek) hasar alma işlemleri buradadır.
    # ----------------------------------------------------------------------------------------------------
    def hasar_al(self, miktar):
        if miktar <= 0: return 0
        if self.durumlar["hasar_azaltma"] > 0:
            miktar *= (1.0 - self.durumlar["hasar_azaltma"])
        savunma = self.savunma
        if self.durumlar["savunma_artisi_turlari"] > 0:
            savunma *= 1.30
        gercek = max(0, int(miktar - savunma))
        if self.kalkan > 0:
            if self.kalkan >= gercek:
                self.kalkan -= gercek
                return 0
            gercek -= self.kalkan
            self.kalkan = 0
        self.can = max(0, self.can - gercek)
        return gercek

    def gercek_hasar_al(self, miktar):
        self.can = max(0, self.can - miktar)

    def iyiles(self, miktar):
        self.can = min(self.maks_can, self.can + miktar)
        cprint(f"+{miktar} CAN Iyilesildi", Colors.GREEN)

    def mana_yenile(self, miktar):
        self.mana = min(self.maks_mana, self.mana + miktar)

    def enerji_yenile(self, miktar):
        self.enerji = min(self.maks_enerji, self.enerji + miktar)
