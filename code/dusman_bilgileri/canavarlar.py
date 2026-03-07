"""
canavarlar.py — Oyundaki tüm normal düşmanların isimlerinin, statülerinin ve seviyeye göre güçlenme formüllerinin tanımlandığı dosya.
"""
from dusman_bilgileri.enemy import Enemy
import random

# ----------------------------------------------------------------------------------------------------
# CANAVAR SINIFLARI 
# Her bir canavar sınıfı, kendi yapısına uygun temel statü (can, saldırı, hız, zırh vb.) özelliklerine ve artış çarpanlarına sahiptir.
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------

class Skeleton(Enemy):
    """Ortalama cana sahip, ancak savunması düşük, standart bir yakın dövüş düşmanıdır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Iskelet", 
            can=60 + (seviye * 5), 
            saldiri=15 + (seviye * 3), 
            savunma=6, 
            hiz=15, 
            tp_odulu=15, 
            altin_odulu=25
        )

# ----------------------------------------------------------------------------------------------------

class Goblin(Enemy):
    """Hızlı hareket eden, yüksek saldırı gücüne sahip fakat çok kırılgan (düşük can ve zırh) bir varlıktır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Goblin", 
            can=75 + (seviye * 4), 
            saldiri=20 + (seviye * 3), 
            savunma=3, 
            hiz=20, 
            tp_odulu=15, 
            altin_odulu=20
        )

# ----------------------------------------------------------------------------------------------------

class Zombie(Enemy):
    """Çok yavaş hareket eden ancak can değeri son derece yüksek olan inatçı bir ölümsüzdür."""
    def __init__(self, seviye):
        super().__init__(
            ad="Zombi", 
            can=100 + (seviye * 7), 
            saldiri=15 + (seviye * 3), 
            savunma=10, 
            hiz=4, 
            tp_odulu=20, 
            altin_odulu=25
        )

# ----------------------------------------------------------------------------------------------------

class Wolf(Enemy):
    """Oyuncuya kanama (zamanla tura bağlı hasar) etkisi verebilen, hızlı çevik bir yırtıcıdır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Vahşi Kurt", 
            can=110 + (seviye * 5), 
            saldiri=30 + (seviye * 5), 
            savunma=10, 
            hiz=20, 
            tp_odulu=25, 
            altin_odulu=50
        )

# ----------------------------------------------------------------------------------------------------

class Golem(Enemy):
    """Son derece yüksek zırh ve can değerleri ile tam bir duvardır. Öldürmesi uzun sürer ancak inanılmaz yavaştır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Golem", 
            can=250 + (seviye * 12), 
            saldiri=20 + (seviye * 4), 
            savunma=20 + (seviye * 3), 
            hiz=2, 
            tp_odulu=40, 
            altin_odulu=75
        )

# ----------------------------------------------------------------------------------------------------

class Worm(Enemy):
    """Bir tur içerisinde defalarca ve ard arda saldırabilen (Çoklu vuruş mekaniğine sahip) tehlikeli bir canavardır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Yer Altı Solucanı", 
            can=75 + (seviye * 5), 
            saldiri=20 + (seviye * 3), 
            savunma=10, 
            hiz=15, 
            tp_odulu=25, 
            altin_odulu=15
        )

# ----------------------------------------------------------------------------------------------------

class Scorpion(Enemy):
    """Yüksek ihtimalle rakibi zehirleyen (zamanla hasar ve statü zayıflaması bırakan) çöl canavarıdır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Dev Akrep", 
            can=100 + (seviye * 6), 
            saldiri=25 + (seviye * 3), 
            savunma=13, 
            hiz=13, 
            tp_odulu=30, 
            altin_odulu=18
        )

# ----------------------------------------------------------------------------------------------------

class AtesRuhu(Enemy):
    """Aşırı hızlıdır ve vuruşları yakma etkisi (statüye bağlı yakıcı hasar) bırakır. Canı düşüktür."""
    def __init__(self, seviye):
        super().__init__(
            ad="Ateş Ruhu", 
            can=100 + (seviye * 3), 
            saldiri=25 + (seviye * 3), 
            savunma=5, 
            hiz=20, 
            tp_odulu=25, 
            altin_odulu=15
        )

# ----------------------------------------------------------------------------------------------------

class BuzRuhu(Enemy):
    """Çok yüksek bir hıza sahiptir. Rakibini dondurarak (sırasını atlamasını veya yavaşlamasını sağlayarak) zorlar."""
    def __init__(self, seviye):
        super().__init__(
            ad="Buz Ruhu", 
            can=100 + (seviye * 3), 
            saldiri=20 + (seviye * 3), 
            savunma=5, 
            hiz=20, 
            tp_odulu=25, 
            altin_odulu=15
        )

# ----------------------------------------------------------------------------------------------------

class Basilisk(Enemy):
    """Dayanıklı ve çok yüksek miktarda ölümcül zehir kalıntısı (savaş boyu kalıcı hasar) saçan korkutucu bir canavardır."""
    def __init__(self, seviye):
        super().__init__(
            ad="Basilisk", 
            can=150 + (seviye * 12), 
            saldiri=20 + (seviye * 2), 
            savunma=10, 
            hiz=15, 
            tp_odulu=40, 
            altin_odulu=30
        )

# ----------------------------------------------------------------------------------------------------

class Slime(Enemy):
    """Farklı element (Ateş, Su, Zehir) varyasyonlarına sahip olabilen değişken ve sinsi bir yaratıktır."""
    def __init__(self, seviye, tür="Düz"):
        self.tür = tür
        
        can = 100 + (seviye * 6)
        saldiri = 20 + (seviye * 2)
        hiz = 15
        altin = 20
        tp = 25
        
        if tür == "Ateş":
            saldiri += 6 + (seviye * 2)
            can += 6 + (seviye * 2)
        elif tür == "Su":
            hiz += 10 + (seviye * 2)
        elif tür == "Zehir":
            saldiri -= 3 + (seviye * 2)
            can += 13 + (seviye * 2)    
            
        super().__init__(
            ad=f"{tür} Slime", 
            can=can, 
            saldiri=saldiri, 
            savunma=3, 
            hiz=hiz, 
            tp_odulu=tp, 
            altin_odulu=altin
        )

# ----------------------------------------------------------------------------------------------------

def rastgele_slime_getir(seviye):
    t = random.choice(["Düz", "Ateş", "Su", "Zehir"])
    return Slime(seviye, t)
