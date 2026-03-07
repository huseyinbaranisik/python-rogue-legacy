from oyuncu_bilgileri.player import Player
from utils import Colors, cprint

class Tank(Player):
    def __init__(self, ad):
        super().__init__(
            ad=ad,
            rol_adi="Tank",
            can=160, 
            mana=40,
            enerji=80,
            saldiri=8, 
            savunma=30, 
            hiz=5,
            yetenekler=["Kalkan Vurusu", "Yer Sarsintisi", "Metanet", "Siper Al", "YIKILMAZ KALE"]
        )
    
    def hasar_yansit(self, gelen_hasar):
        """Temel %20 + her 25 zirh icin +%1 yansitma. Buff varsa temel %60 olur."""
        bonus_yansitma = self.savunma // 25 * 0.01
        temel_yansitma = 0.60 if self.durumlar["yansitma_turlari"] > 0 else 0.20
        toplam_yansitma_orani = temel_yansitma + bonus_yansitma
        yansitilan = int(gelen_hasar * toplam_yansitma_orani)
        if yansitilan > 0:
            cprint(f">>> {self.ad} KALKAN YANSITMASI (%{int(toplam_yansitma_orani*100)}): {yansitilan} hasar geri döndü! <<<", Colors.CYAN)
        return yansitilan

    def seviye_artıslarını_getir(self):
        """Tank: Yüksek Can ve Zırh, düşük hasar ve mana."""
        return {
            "hp": 50, "mana": 3, "energy": 3,
            "attack": 3, "defense": 8, "speed": 1
        }
