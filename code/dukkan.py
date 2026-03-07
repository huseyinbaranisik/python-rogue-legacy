"""
dukkan.py — Tüccar, eşya düşürme ve fiyatlandırma sistemi
"""
import random
import time
import copy

from utils import Colors, cprint, input_colored, wait_with_dots

QUALITY_LEVELS = ["Temel", "Basit", "Orta Kalite", "Kaliteli", "Üstün",
                  "Görkemli", "Efsanevi", "Ruhani", "İlahi", "Kadim"]

DROP_CHANCE   = 0.25
RARITY_WEIGHTS = {"godlike": 0.01, "legendary": 0.05, "mystic": 0.20, "rare": 0.50, "common": 1.0}
BOSS_RARITY_WEIGHTS = {"godlike": 0.10, "legendary": 0.30, "mystic": 0.60, "rare": 1.0}
RARITY_PRICES  = {"common": 100, "rare": 250, "mystic": 600, "legendary": 1500, "godlike": 3000}


class DukkanMixin:

    # -----------------------------------------------------------------------
    # YARDIMCI HESAPLAMALAR
    # -----------------------------------------------------------------------
    def _roll_rarity(self, weights):
        roll = random.random()
        for rarity, threshold in sorted(weights.items(), key=lambda x: x[1]):
            if roll < threshold:
                return rarity
        return "common"

    def scale_item_to_level(self, item):
        new = copy.deepcopy(item)
        mult = 1.0 + (self.oyuncu.seviye * 0.1)
        for stat, val in new.stats.items():
            if isinstance(val, (int, float)) and val > 0:
                new.stats[stat] = int(val * mult)
        return new

    def get_item_price(self, item):
        base  = RARITY_PRICES.get(item.rarity, 100)
        lvmul = 1.0 + (self.oyuncu.seviye * 0.05)
        return int(base * lvmul)

    # -----------------------------------------------------------------------
    # EŞYA DÜŞÜRME
    # -----------------------------------------------------------------------
    def drop_item(self):
        if random.random() > DROP_CHANCE:
            return
        rarity = self._roll_rarity(RARITY_WEIGHTS)
        pool = [i for i in self.tum_esyalar if i.rarity == rarity] or \
               [i for i in self.tum_esyalar if i.rarity == "common"]
        if not pool:
            return
        item = self.scale_item_to_level(random.choice(pool))
        cprint("*" * 37, Colors.YELLOW)
        cprint(f"!!! GANIMET BULDUN: {item.get_colored_name()} !!!", Colors.GREEN)
        cprint(f"!!! {item.get_stats_str()} !!!", Colors.CYAN)
        cprint("*" * 37, Colors.YELLOW)
        self.oyuncu.ekipman_envanteri.append(item)
        wait_with_dots(count=3)

    def drop_boss_item(self, boss=None):
        from dusman_bilgileri.bosslar.ejder_prens import EjderPrens
        from dusman_bilgileri.bosslar.perona import HirsizlarKiralicesi

        if isinstance(boss, EjderPrens):
            cprint("\n*** EJDER PRENSIN GANIMETI SENINDIR! ***", Colors.YELLOW)
            pool = [i for i in self.tum_esyalar if i.rarity == "godlike" and i.item_type == "accessory"] \
                or [i for i in self.tum_esyalar if i.rarity == "godlike"]
            if pool:
                dropped = random.choice(pool)
                cprint(f"!!! {dropped.get_colored_name()} Kazandin! !!!", Colors.GREEN)
                self.oyuncu.ekipman_envanteri.append(dropped)
            return

        if isinstance(boss, HirsizlarKiralicesi):
            cprint("\n*** PERONA'NIN GIZLI HAZINESINI BULDUN! ***", Colors.PURPLE)
            pool = [i for i in self.tum_esyalar if i.rarity == "godlike"]
            for _ in range(2):
                if pool:
                    dropped = random.choice(pool)
                    cprint(f"!!! {dropped.get_colored_name()} Kazandin! !!!", Colors.GREEN)
                    self.oyuncu.ekipman_envanteri.append(dropped)
            return

        rarity = self._roll_rarity(BOSS_RARITY_WEIGHTS)
        pool = [i for i in self.tum_esyalar if i.rarity == rarity] or \
               [i for i in self.tum_esyalar if i.rarity == "common"]
        if pool:
            dropped = random.choice(pool)
            cprint(f"\n!!! BOSS ODULU: {dropped.get_colored_name()} !!!", Colors.YELLOW)
            self.oyuncu.ekipman_envanteri.append(dropped)

    # -----------------------------------------------------------------------
    # TÜCCAR ETKİNLİĞİ
    # -----------------------------------------------------------------------
    def merchant_event(self):
        cprint("\n--- SEYYAR GOBLIN DUKKAN ---", Colors.YELLOW)
        slots = ["weapon", "armor", "accessory"]
        items_by_slot = {s: [i for i in self.tum_esyalar if i.item_type == s] for s in slots}

        # Her slot için ağırlıklı rastgele seç
        shop_items = []
        for slot in slots:
            pool = items_by_slot.get(slot, [])
            if not pool:
                continue
            scored = []
            half_gold = self.oyuncu.altin * 0.5
            for base in pool:
                scaled = self.scale_item_to_level(base)
                price  = self.get_item_price(scaled)
                score  = 1.0
                if self.oyuncu.altin >= 1000:
                    score = 0.2 if price < half_gold else 10.0 / (1.0 + abs(price - self.oyuncu.altin) / 500)
                scored.append((scaled, price, score))
            if scored:
                items_only, prices_only, weights = zip(*scored)
                idx = random.choices(range(len(items_only)), weights=weights, k=1)[0]
                shop_items.append({"item": items_only[idx], "price": prices_only[idx],
                                   "type": slot, "sold": False})

        while True:
            import os; os.system("cls" if os.name == "nt" else "clear")
            cprint(f"Altin: {self.oyuncu.altin}", Colors.YELLOW)

            q_idx  = min(len(QUALITY_LEVELS) - 1, self.oyuncu.kat // 10)
            q_name = QUALITY_LEVELS[q_idx]
            mult   = q_idx + 1
            hp_name, hp_heal, hp_price = f"{q_name} Can İksiri", 50*mult, 30*mult
            mp_name, mp_price = f"{q_name} Mana İksiri", 25*mult
            ep_name, ep_price = f"{q_name} Enerji İksiri", 25*mult
            dp_name, dp_price = f"{q_name} Dayanıklılık İksiri", 250*mult
            full_price = 500 + (self.oyuncu.kat * 10)

            cprint("\n=== IKSIRLER ===", Colors.CYAN)
            cprint(f"1. {hp_name} ({hp_heal} HP) - {hp_price} Altin", Colors.RED)
            cprint(f"2. {mp_name} (40 MP) - {mp_price} Altin", Colors.BLUE)
            cprint(f"3. {ep_name} (40 EP) - {ep_price} Altin", Colors.YELLOW)
            cprint(f"4. Taze Başlangıç (Full Bar) - {full_price} Altin", Colors.GREEN)
            cprint(f"5. {dp_name} (50 Kalkan) - {dp_price} Altin", Colors.WHITE)

            if shop_items:
                cprint("\n=== EKIPMANLAR ===", Colors.PURPLE)
                for idx, si in enumerate(shop_items):
                    if si["sold"]:
                        cprint(f"{idx+6}. [SATILDI]", Colors.GREY)
                    else:
                        cprint(f"{idx+6}. {si['item'].get_colored_name()} {si['item'].get_stats_str()} - {si['price']} Altin",
                               Colors.WHITE)
                        if si["item"].description:
                            cprint(f"   {si['item'].description}", Colors.GREY)

            sell_idx = len(shop_items) + 6
            print(f"\n{sell_idx}. ESYA SAT")
            print("0. Ayril")
            c = input_colored("Secim: ")

            potion_map = {
                "1": (hp_name,  hp_price),
                "2": (mp_name,  mp_price),
                "3": (ep_name,  ep_price),
                "4": ("Taze Başlangıç", full_price),
                "5": (dp_name,  dp_price),
            }
            if c in potion_map:
                name, price = potion_map[c]
                if self.oyuncu.altin >= price:
                    self.oyuncu.altin -= price
                    self.oyuncu.envanter[name] = self.oyuncu.envanter.get(name, 0) + 1
                    cprint(f"{name} aldin.", Colors.GREEN)
                else:
                    cprint("Paran yetersiz.", Colors.RED)
                time.sleep(1)
            elif c == "0":
                break
            elif c == str(sell_idx):
                self.sell_items_menu()
            elif c.isdigit():
                ci = int(c)
                if 6 <= ci < 6 + len(shop_items):
                    si = shop_items[ci - 6]
                    if si["sold"]:
                        cprint("Bu esya zaten satildi!", Colors.RED)
                    elif self.oyuncu.altin >= si["price"]:
                        self.oyuncu.altin -= si["price"]
                        self.oyuncu.ekipman_envanteri.append(si["item"])
                        cprint(f"{si['item'].get_colored_name()} satin aldin!", Colors.GREEN)
                        si["sold"] = True
                    else:
                        cprint("Paran yetersiz.", Colors.RED)
                    time.sleep(1)

    def sell_items_menu(self):
        while True:
            import os; os.system("cls" if os.name == "nt" else "clear")
            cprint("\n--- ESYA SATIS ---", Colors.YELLOW)
            cprint(f"Altin: {self.oyuncu.altin}", Colors.YELLOW)
            if not self.oyuncu.ekipman_envanteri:
                cprint("\nCantanda satilacak ekipman yok!", Colors.RED)
                time.sleep(1); break
            for i, item in enumerate(self.oyuncu.ekipman_envanteri):
                price = int(self.get_item_price(item) * 0.66)
                print(f"{i+1}. {item.get_colored_name()} {item.get_stats_str()} -> {price} Altin")
            print("\n0. Geri Don")
            c = input_colored("Satilacak Esya (No): ")
            if c == "0": break
            try:
                idx = int(c) - 1
                if 0 <= idx < len(self.oyuncu.ekipman_envanteri):
                    item  = self.oyuncu.ekipman_envanteri.pop(idx)
                    price = int(self.get_item_price(item) * 0.66)
                    self.oyuncu.altin += price
                    cprint(f"{item.get_colored_name()} satildi! +{price} Altin.", Colors.GREEN)
                    time.sleep(1)
            except (ValueError, IndexError):
                pass
