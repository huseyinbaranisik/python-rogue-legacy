"""
champion_enemy.py — Rastgele karşılaşmalarda şampiyon düzeyindeki canavarları üretir.
"""
from dusman_bilgileri.enemy import Enemy

# ----------------------------------------------------------------------------------------------------
# ŞAMPİYON DÜŞMAN SINIFI (Zorlu ama ödülü yüksek rakipler)
# ----------------------------------------------------------------------------------------------------
class ChampionEnemy(Enemy):
    def __init__(self, temel_dusman):
        """
        Normal olarak üretilmiş bir düşmanı alıp, statlarını aşırı güçlendirerek (örneğin can ve saldırısını ikiye katlayarak) 
        şampiyon (elit) statüsüne çeken sarmalayıcı (wrapper) fonksiyon.
        """
        # Standart düşmanın tüm özelliklerini alır
        self.__dict__ = temel_dusman.__dict__.copy()
        
        # Etiketi günceller
        self.ad = f"SAMPIYON {temel_dusman.ad}"
        
        # Savaş meydanındaki zorluğu artırmak için statlarını iyileştirir (x2 Kat)
        self.can = int(self.can * 2.0)
        self.maks_can = self.can
        self.saldiri = int(self.saldiri * 2.0)
        self.savunma = int(self.savunma * 2.0)
        
        # Meydan okumayı başaranlar için tecrübe puanı ve altını artırır
        self.tp_odulu = int(self.tp_odulu * 3.0)
        self.altin_odulu = int(self.altin_odulu * 2.5) 
