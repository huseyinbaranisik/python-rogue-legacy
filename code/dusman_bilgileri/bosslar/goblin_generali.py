from dusman_bilgileri.bosslar.boss import Boss
from utils import Colors, cprint

class GoblinGenerali(Boss):
    def __init__(self, seviye):
        super().__init__(
            ad="Goblin Generali Afir",
            can=400 + (seviye * 15),
            saldiri=30 + (seviye * 3),
            savunma=25 + (seviye * 2),
            hiz=8,
            tp_odulu=800,
            altin_odulu=400
        )
        self.can_calma = 0.25  # Hasarın %25'ini can olarak çeker
        self.adrenalin = 0
        self.maks_adrenalin = 100

    def ozel_mekanik(self, oyuncu):
        """Her tur başında ekstra zırh ve öfke kazanır."""
        self.savunma += 3
        # Her tur 20 öfke kazanır
        self.adrenalin = min(self.maks_adrenalin, self.adrenalin + 20)
        
        cprint(f"Afir zirhini guclendirdi! (Zirh: {self.savunma})", Colors.YELLOW)
        
        if self.adrenalin >= self.maks_adrenalin:
            cprint("!!! AFIR KUDURDU! GOZLERI KAN CANAGINA DONDU !!!", Colors.RED)
            # Bir sonraki saldırı için atağı geçici olarak %50 artar
            self.saldiri = int(self.saldiri * 1.5)
            self.adrenalin = 0
        
        cprint("Afir devasa balyozunu savuruyor!", Colors.RED)
        if not oyuncu.durumlar["sersemleme"] and oyuncu.hayatta_mi():
             pass
