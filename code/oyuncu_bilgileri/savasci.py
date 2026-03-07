from oyuncu_bilgileri.player import Player
from utils import Colors, cprint

class Savasci(Player):
    def __init__(self, ad):
        super().__init__(
            ad=ad,
            rol_adi="Savasci",
            can=100, 
            mana=50,
            enerji=100,
            saldiri=15, 
            savunma=8, 
            hiz=10,
            yetenekler=["Yumruk", "Kilic Darbesi", "Ofke", "Hortlak Darbesi", "KAOS VURUSU"]
        )
        # ADRENALIN BAR (Turuncu)
        self.adrenalin = 0
        self.maks_adrenalin = 100
        self.adrenalin_saldiri_basi = 20
    
    def istatistikleri_goster(self):
        """Savaşçı için özel stat gösterimi (Adrenalin barı ile)"""
        cprint(f"\n--- {self.ad} | {self.rol} | Seviye {self.seviye} ---", Colors.CYAN)
        cprint(f"CAN: {self.can}/{self.maks_can}", Colors.RED, end="  |  ")
        cprint(f"MANA: {self.mana}/{self.maks_mana}", Colors.BLUE, end="  |  ")
        cprint(f"ENERJI: {self.enerji}/{self.maks_enerji}", Colors.YELLOW)
        
        # ADRENALIN BAR (TURUNCU)
        adr_color = "\033[38;5;208m"  # Turuncu renk
        cprint(f"ADRENALIN: {self.adrenalin}/{self.maks_adrenalin}", adr_color)
        
        cprint(f"SALDIRI: {self.saldiri}  |  SAVUNMA: {self.savunma}  |  HIZ: {self.hiz}", Colors.WHITE)
        cprint(f"ALTIN: {self.altin}  |  KAT: {self.kat}", Colors.YELLOW)
        cprint(f"YETENEK PUANI: {self.yetenek_puanlari}", Colors.GREEN)
        
        # Ekipmanları Göster
        s = self.ekipman['silah'].get_colored_name() if self.ekipman['silah'] else "Yok"
        z = self.ekipman['zirh'].get_colored_name() if self.ekipman['zirh'] else "Yok"
        ak = self.ekipman['aksesuar'].get_colored_name() if self.ekipman['aksesuar'] else "Yok"
        
        cprint(f"\nSilah: {s} | Zirh: {z} | Aksesuar: {ak}", Colors.GREY)
        cprint("-" * 50, Colors.CYAN)
    
    def adrenalin_kazan(self, miktar=20):
        """Adrenalin kazan, fazlasını cana dönüştür ve statları güncelle"""
        yeni_deger = self.adrenalin + miktar
        if yeni_deger > self.maks_adrenalin:
            fazlalik = yeni_deger - self.maks_adrenalin
            iyilesme_miktari = fazlalik // 2
            if iyilesme_miktari > 0:
                self.iyiles(iyilesme_miktari)
            self.adrenalin = self.maks_adrenalin
        else:
            self.adrenalin = yeni_deger

        if self.adrenalin >= self.maks_adrenalin:
            cprint(">>> ADRENALIN DOLU! KRITIK VURUŞ HAZIR! <<<", "\033[38;5;208m")
        self.istatistikleri_hesapla()

    def adrenalinsiz_saldiri_getir(self):
        """Hortlak Darbesi gibi yetenekler için bonusu çıkararak hasar döner."""
        bonus = self.adrenalin // 12
        return self.saldiri - bonus
    
    def adrenalin_saldirisi_kullan(self):
        """Adrenalin barı doluysa kritik vuruş yap ve statları sıfırla"""
        if self.adrenalin >= self.maks_adrenalin:
            self.adrenalin = 0
            self.istatistikleri_hesapla()
            return True
        return False

    def istatistikleri_hesapla(self):
        """Temel statları hesapla ve adrenalin bonusunu ekle"""
        super().istatistikleri_hesapla()
        # Her ~12.5 adrenalin için +1 Hasar, +1 Zırh ve +1 Hız (Maks 100/12 = 8)
        bonus = self.adrenalin // 12
        self.saldiri += bonus
        self.savunma += bonus
        self.hiz += bonus

    def seviye_artıslarını_getir(self):
        """Savaşçı: Dengeli gelişim, düşük mana artışı."""
        return {
            "hp": 30, "mana": 5, "energy": 10,
            "attack": 8, "defense": 4, "speed": 1
        }
