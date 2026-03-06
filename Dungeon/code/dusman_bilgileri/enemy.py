from entity import Entity

class Enemy(Entity):
    ISTATISTIK_CARPANI = 1.50
    
    def __init__(self, ad, can, saldiri, savunma, hiz, tp_odulu, altin_odulu):
        m = self.ISTATISTIK_CARPANI
        super().__init__(
            ad=ad, 
            can=int(can * m), maks_can=int(can * m), 
            mana=0, maks_mana=0, 
            enerji=0, maks_enerji=0, 
            saldiri=int(saldiri * m), 
            savunma=int(savunma * m), 
            hiz=int(hiz * m)
        )
        self.tp_odulu = tp_odulu
        self.altin_odulu = altin_odulu
        self.patron_mu = False
