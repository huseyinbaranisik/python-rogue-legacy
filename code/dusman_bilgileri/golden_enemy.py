"""
golden_enemy.py — Karşılaşması nadir, ancak ödülü altın bakımından çok cömert olan canavarları üretir.
"""
from dusman_bilgileri.enemy import Enemy

# ----------------------------------------------------------------------------------------------------
# ALTIN DÜŞMAN SINIFI (Zenginleştirilmiş Rakip)
# ----------------------------------------------------------------------------------------------------
class GoldenEnemy(Enemy):
    def __init__(self, temel_dusman):
        """
        Normal olarak üretilmiş bir düşmanı alıp, özelliklerini altın varyasyona dönüştürür.
        Şampiyon düşmana kıyasla daha zayıftır, asıl esprisi çok yüksek altın kazandırmasıdır.
        """
        # Standart düşmanın değerlerini olduğu gibi alır
        self.__dict__ = temel_dusman.__dict__.copy()
        
        # İsmi belirginleşir (Örn: ALTIN Goblin)
        self.ad = f"ALTIN {temel_dusman.ad}"
        
        # Normal düşmandan biraz daha dayanıklı ve güçlüdür (x1.5 Kat)
        self.can = int(self.can * 1.5)
        self.maks_can = self.can
        self.saldiri = int(self.saldiri * 1.5)
        
        # Daha az TP (Tecrübe), ancak çok daha fazla altın verir (x4 Kat)
        self.tp_odulu = int(self.tp_odulu * 0.5) 
        self.altin_odulu = self.altin_odulu * 4
