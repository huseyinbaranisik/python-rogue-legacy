from dusman_bilgileri.bosslar.boss import Boss
from utils import Colors, cprint

class Void(Boss):
    def __init__(self, seviye):
        super().__init__(
            ad="VOID: The Ending",
            can=2500 + (seviye * 50),
            saldiri=120 + (seviye * 8), 
            savunma=80 + (seviye * 5),
            hiz=50,
            tp_odulu=15000,
            altin_odulu=5000
        )
        self.patron_mu = True

    def bos_giris(self):
        super().bos_giris()
        cprint("\n.....", Colors.GREY)
        cprint("H I C L I K", Colors.PURPLE)
        cprint("S O N   S A V A S", Colors.RED)
        cprint("\nVOID seni bekliyor...", Colors.GREY)

    def ozel_mekanik(self, oyuncu):
        """Her turda güçlü saldırı ve kendini iyileştirme"""
        import random
        
        if oyuncu.hayatta_mi():
            # %60 şans ile güçlü karanlık saldırı
            if random.random() < 0.60:
                cprint(f"{self.ad} karanlık enerjisini serbest bırakıyor!", Colors.PURPLE)
                karanlik_hasari = random.randint(80, 150)
                oyuncu.gercek_hasar_al(karanlik_hasari)
                cprint(f"Karanlık enerji {oyuncu.ad}'e {karanlik_hasari} hasar verdi!", Colors.RED)
            
            # %40 şans ile kendini iyileştirme
            if random.random() < 0.40:
                iyilesme = random.randint(100, 200)
                self.can = min(self.maks_can, self.can + iyilesme)
                cprint(f"{self.ad} hiçlikten güç çekiyor! (+{iyilesme} HP)", Colors.CYAN) 
