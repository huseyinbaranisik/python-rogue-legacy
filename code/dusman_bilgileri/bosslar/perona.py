from dusman_bilgileri.bosslar.boss import Boss
from utils import Colors, cprint
import random
import time

class HirsizlarKiralicesi(Boss):
    def __init__(self, seviye):
        super().__init__(
            ad="Hirsizlar Kiralicesi Perona",
            can=1500 + (seviye * 30),
            saldiri=80 + (seviye * 6),
            savunma=40 + (seviye * 2),
            hiz=40,
            tp_odulu=5000,
            altin_odulu=10000
        )
        self.her_seyi_caldi_mi = False

    def ozel_mekanik(self, oyuncu):
        """TÜM HER ŞEYİ ÇALMA!"""
        if not self.her_seyi_caldi_mi:
            cprint(f"\n!!! {self.ad.upper()} KAHKAHALAR ATARAK UZERINE ATILDI !!!", Colors.PURPLE)
            cprint("!!! 'NE VAR NE YOK HEPSI BENIM!' DİYE BAGIRIYOR !!!", Colors.RED)
            
            # Altınları çal
            calinan_altin = oyuncu.altin
            oyuncu.altin = 0
            
            # İksirleri çal
            calinan_iksirler = list(oyuncu.envanter.keys())
            oyuncu.envanter = {}
            
            # Giyili eşyaları çal
            calinan_esya_sayisi = 0
            for slot in ["silah", "zirh", "aksesuar"]:
                if oyuncu.ekipman[slot] is not None:
                    oyuncu.ekipman[slot] = None
                    calinan_esya_sayisi += 1
            
            # Envanterdeki ekipmanları da çal
            enc_env_sayisi = len(oyuncu.ekipman_envanteri)
            oyuncu.ekipman_envanteri = []
            
            # Statları güncelle
            oyuncu.istatistikleri_hesapla()
            
            cprint(f">>> {calinan_altin} Altin calindi!", Colors.YELLOW)
            cprint(f">>> Tüm iksirlerin ({len(calinan_iksirler)} cesit) calindi!", Colors.RED)
            cprint(f">>> Tüm ekipmanlarin ({calinan_esya_sayisi} giyili, {enc_env_sayisi} cantada) calindi!", Colors.PURPLE)
            cprint(">>> ARTIK HİÇBİR ŞEYİN YOK. SADECE YETENEKLERİN KALDI! <<<", Colors.CYAN)
            
            self.her_seyi_caldi_mi = True
            time.sleep(2)
        else:
            phrases = [
                "Cok zavalli gorunuyorsun...",
                "Belki seni oldurmem, kole yaparım!",
                "Bu ekipmanlar bana daha cok yakisiyor.",
                "Hala savasiyor musun? Inanılmaz!"
            ]
            cprint(f"{self.ad}: '{random.choice(phrases)}'", Colors.PURPLE)
