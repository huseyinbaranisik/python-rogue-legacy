from dusman_bilgileri.bosslar.boss import Boss
from utils import Colors, cprint
import random

class EjderPrens(Boss):
    def __init__(self, seviye):
        super().__init__(
            ad="Ejder Prens Naafiri",
            can=1000 + (seviye * 25),
            saldiri=60 + (seviye * 4), 
            savunma=80 + (seviye * 5),
            hiz=20,
            tp_odulu=2500,
            altin_odulu=3000
        )

    def ozel_mekanik(self, oyuncu):
        """Pasif yanma hasarı ve pulların direnci."""
        if oyuncu.hayatta_mi():
            # Pasif Yakma Hasarı (Her tur kaçınılmaz)
            yanma_hasari = 25 + (oyuncu.seviye * 2)
            cprint(f"!!! EJDERHANIN SICAKLIGI SENI YAKIYOR: -{yanma_hasari} HP !!!", Colors.RED)
            oyuncu.gercek_hasar_al(yanma_hasari)
            
            # Alev nefesi
            if random.random() < 0.4:
                cprint(f"{self.ad} alev nefesini puskurur!", Colors.RED)
                oyuncu.kanama_uygula(yukler=2, sure=3) # Yanma niyetine kanama kullanıyoruz
                cprint(f"{oyuncu.ad} ağır yanıklar içinde!", Colors.YELLOW)
