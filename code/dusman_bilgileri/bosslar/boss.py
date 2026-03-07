from dusman_bilgileri.enemy import Enemy
from utils import Colors, cprint

class Boss(Enemy):
    ISTATISTIK_CARPANI = 1.0
    def __init__(self, ad, can, saldiri, savunma, hiz, tp_odulu, altin_odulu):
        super().__init__(ad, can, saldiri, savunma, hiz, tp_odulu, altin_odulu)
        self.patron_mu = True

    def bos_giris(self):
        """Boss savasi oncesi havali bir giris mesaji."""
        cprint("\n" + "#" * 50, Colors.RED)
        cprint(f"!!! BOSS SAVASI BASLIYOR: {self.ad} !!!", Colors.RED)
        cprint("#" * 50 + "\n", Colors.RED)

    def ozel_mekanik(self, oyuncu):
        """Her bossun overwrite edecegi ozel mekanik."""
        pass
