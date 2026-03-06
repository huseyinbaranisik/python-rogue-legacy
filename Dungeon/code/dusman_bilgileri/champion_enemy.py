from dusman_bilgileri.enemy import Enemy

class ChampionEnemy(Enemy):
    def __init__(self, temel_dusman):
        """Normal bir dusmani Sampiyon versiyona ceviren sinif."""
        self.__dict__ = temel_dusman.__dict__.copy()
        self.ad = f"SAMPIYON {temel_dusman.ad}"
        
        # 2 kat daha guclu
        self.can = int(self.can * 2.0)
        self.maks_can = self.can
        self.saldiri = int(self.saldiri * 2.0)
        self.savunma = int(self.savunma * 2.0)
        
        # 3 kat daha fazla TP
        self.tp_odulu = int(self.tp_odulu * 3.0)
        self.altin_odulu = int(self.altin_odulu * 2.5) 
