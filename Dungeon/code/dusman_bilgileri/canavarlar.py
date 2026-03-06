from dusman_bilgileri.enemy import Enemy
import random

class Skeleton(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Iskelet", 
            can=44 + (seviye * 5), 
            saldiri=13 + (seviye * 3), 
            savunma=6, 
            hiz=10, 
            tp_odulu=10, 
            altin_odulu=5
        )

class Goblin(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Goblin", 
            can=31 + (seviye * 4), 
            saldiri=19 + (seviye * 3), 
            savunma=3, 
            hiz=19, 
            tp_odulu=12, 
            altin_odulu=8
        )

class Zombie(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Zombi", 
            can=63 + (seviye * 7), 
            saldiri=10 + (seviye * 3), 
            savunma=10, 
            hiz=4, 
            tp_odulu=15, 
            altin_odulu=6
        )

class Wolf(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Vahsi Kurt", 
            can=50 + (seviye * 5), 
            saldiri=23 + (seviye * 4), 
            savunma=4, 
            hiz=18, 
            tp_odulu=18, 
            altin_odulu=7
        )

class Golem(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Golem", 
            can=125 + (seviye * 12), 
            saldiri=13 + (seviye * 4), 
            savunma=6 + (seviye * 3), 
            hiz=3, 
            tp_odulu=40, 
            altin_odulu=50
        )

class Worm(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Yeralti Solucani", 
            can=38 + (seviye * 5), 
            saldiri=15 + (seviye * 3), 
            savunma=6, 
            hiz=15, 
            tp_odulu=25, 
            altin_odulu=12
        )

class Scorpion(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Dev Akrep", 
            can=75 + (seviye * 6), 
            saldiri=19 + (seviye * 3), 
            savunma=13, 
            hiz=13, 
            tp_odulu=30, 
            altin_odulu=18
        )

class AtesRuhu(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Ateş Ruhu", 
            can=25 + (seviye * 3), 
            saldiri=23 + (seviye * 3), 
            savunma=2, 
            hiz=31, 
            tp_odulu=25, 
            altin_odulu=15
        )

class BuzRuhu(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Buz Ruhu", 
            can=25 + (seviye * 3), 
            saldiri=15 + (seviye * 3), 
            savunma=3, 
            hiz=28, 
            tp_odulu=25, 
            altin_odulu=15
        )

class Basilisk(Enemy):
    def __init__(self, seviye):
        super().__init__(
            ad="Basilisk", 
            can=113 + (seviye * 12), 
            saldiri=13 + (seviye * 2), 
            savunma=6, 
            hiz=10, 
            tp_odulu=40, 
            altin_odulu=30
        )

class Slime(Enemy):
    def __init__(self, seviye, tür="Düz"):
        self.tür = tür
        
        can = 50 + (seviye * 6)
        saldiri = 10 + (seviye * 2)
        hiz = 15
        altin = 10
        tp = 20
        
        if tür == "Ateş":
            saldiri += 6
            can += 6
        elif tür == "Su":
            hiz += 10
        elif tür == "Zehir":
            saldiri -= 3
            can += 13
            
        super().__init__(
            ad=f"{tür} Slime", 
            can=can, 
            saldiri=saldiri, 
            savunma=3, 
            hiz=hiz, 
            tp_odulu=tp, 
            altin_odulu=altin
        )

def rastgele_slime_getir(seviye):
    t = random.choice(["Düz", "Ateş", "Su", "Zehir"])
    return Slime(seviye, t)
