from dusman_bilgileri.enemy import Enemy

class GoldenEnemy(Enemy):
    def __init__(self, temel_dusman):
        """Normal bir dusmani Altin versiyona ceviren sinif."""
        self.__dict__ = temel_dusman.__dict__.copy()
        self.ad = f"ALTIN {temel_dusman.ad}"
        self.can = int(self.can * 1.5)
        self.maks_can = self.can
        self.saldiri = int(self.saldiri * 1.5)
        self.tp_odulu = int(self.tp_odulu * 0.5) 
        self.altin_odulu = self.altin_odulu * 4
