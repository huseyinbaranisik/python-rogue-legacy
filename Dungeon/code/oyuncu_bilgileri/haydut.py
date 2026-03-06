from oyuncu_bilgileri.player import Player
import random

class Haydut(Player):
    def __init__(self, ad):
        super().__init__(
            ad=ad,
            rol_adi="Haydut",
            can=80, 
            mana=60,
            enerji=120,
            saldiri=18, 
            savunma=4, 
            hiz=20, # En Hizli
            yetenekler=["Hancer", "Sirtindan Bicakla", "Zehirli Bicak", "Yaniltma", "SUIKAST"]
        )
        # HAYDUT OZEL: Kritik Vurus
        self.kritik_sansi = 0.10  # %10 kritik şansı
        self.kritik_carpani = 1.5  # 1.5x hasar
        
        # HAYDUT OZEL: Yenileme
        self.tur_basina_mana_yenileme = 5
        self.tur_basina_enerji_yenileme = 10
    
    def kritik_vurus_kontrol(self):
        """Kritik vuruş kontrolü"""
        return random.random() < self.kritik_sansi

    def seviye_artıslarını_getir(self):
        """Haydut: Yüksek Hasar ve Hız, düşük savunma."""
        return {
            "hp": 20, "mana": 7, "energy": 15,
            "attack": 10, "defense": 1, "speed": 5
        }
