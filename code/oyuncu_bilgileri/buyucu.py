from oyuncu_bilgileri.player import Player

class Buyucu(Player):
    def __init__(self, ad):
        super().__init__(
            ad=ad,
            rol_adi="Buyucu",
            can=70, 
            mana=150,
            enerji=50,
            saldiri=22, 
            savunma=2, 
            hiz=11,
            yetenekler=["Asa Vurusu", "Alev Topu", "Buz Oku", "Asker Cagirma", "METEOR"]
        )
        # BUYUCU OZEL: Hizli Mana Yenileme
        self.tur_basina_mana_yenileme = 10 

    def seviye_artıslarını_getir(self):
        """Büyücü: Yüksek Hasar ve Mana, düşük savunma."""
        return {
            "hp": 20, "mana": 30, "energy": 5,
            "attack": 12, "defense": 1, "speed": 1
        }
