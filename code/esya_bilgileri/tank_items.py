from esya_bilgileri.item import Item

# TANK SILAHLARI: KALKAN (Shield)
def get_tank_weapons():
    weapons = []
    
    # Common
    weapons.append(Item("Tahta Kalkan", "common", "weapon", {"defense": 5}, "Basit ama iş görür."))
    weapons.append(Item("Tencere Kapagi", "common", "weapon", {"defense": 2, "hp": 1}, "Garip ama ise yariyor."))
    weapons.append(Item("Catlak Kalkan", "common", "weapon", {"defense": 4}, "Yarisi kirik."))
    
    # Rare
    weapons.append(Item("Demir Kalkan", "rare", "weapon", {"defense": 10}, "Sağlam demirden."))
    weapons.append(Item("Asker Kalkani", "rare", "weapon", {"defense": 8, "hp": 5}, "Standart ordu ekipmani."))
    weapons.append(Item("Yuvarlak Kalkan", "rare", "weapon", {"defense": 9, "speed": 1}, "Hizlica kaldirilabilir."))
    
    # Mystic
    weapons.append(Item("Dikenli Kalkan", "mystic", "weapon", {"defense": 15, "attack": 2}, "Saldıranlara zarar verir."))
    weapons.append(Item("Kule Kalkan", "mystic", "weapon", {"defense": 20, "speed": -2}, "Devasa bir kule gibi."))
    weapons.append(Item("Ayna Kalkan", "mystic", "weapon", {"defense": 12, "hp": 10}, "Buyu yansitmak icin."))
    
    # Legendary
    weapons.append(Item("Ejder Pulu Kalkan", "legendary", "weapon", {"defense": 30, "hp": 30}, "Ejderha ateşine dayanır."))
    weapons.append(Item("Kutsal Kalkan", "legendary", "weapon", {"defense": 35, "hp": 50}, "Ilahi koruma."))
    weapons.append(Item("Aegis", "legendary", "weapon", {"defense": 40, "mana": 20}, "Tanricalarin kalkani."))
    
    # Godlike
    weapons.append(Item("Titan Duvari", "godlike", "weapon", {"defense": 60, "hp": 100}, "Hiçbir şey onu delemez."))
    weapons.append(Item("Atlas'in Yuku", "godlike", "weapon", {"defense": 80, "attack": 10}, "Dunyayi tasiyabilir."))
    weapons.append(Item("Olympos Kapisi", "godlike", "weapon", {"defense": 100, "hp": 200}, "Tanrilarin gecidi."))
    
    return weapons

# TANK ZIRHLARI: AGIR ZIRH (Heavy Armor)
def get_tank_armors():
    armors = []
    
    # Common
    armors.append(Item("Bakir Zirh", "common", "armor", {"defense": 8}, "Biraz ağır."))
    armors.append(Item("Pasli Plaka", "common", "armor", {"defense": 7, "speed": -1}, "Zamanla eskismis."))
    armors.append(Item("Teneke Zirh", "common", "armor", {"defense": 6}, "Metal parcasi."))
    
    # Rare
    armors.append(Item("Celik Zirh", "rare", "armor", {"defense": 15}, "Savaşçılar için ideal."))
    armors.append(Item("Lejyoner Zirhi", "rare", "armor", {"defense": 16, "hp": 10}, "Eski imparatorluktan."))
    armors.append(Item("Sehir Muhafizi Zirhi", "rare", "armor", {"defense": 14, "hp": 5}, "Standart koruma."))
    
    # Mystic
    armors.append(Item("Volkanik Zirh", "mystic", "armor", {"defense": 25, "hp": 30}, "Sıcak ve dayanıklı."))
    armors.append(Item("Buzul Zirh", "mystic", "armor", {"defense": 24, "mana": 10}, "Soguga karsi."))
    armors.append(Item("Obsidyen Zirh", "mystic", "armor", {"defense": 28, "speed": -3}, "Agir ama kirilmaz."))
    
    # Legendary
    armors.append(Item("Granit Zirh", "legendary", "armor", {"defense": 50, "hp": 100}, "Taştan daha sert."))
    armors.append(Item("Ademantiyum Zirh", "legendary", "armor", {"defense": 60, "energy": 20}, "Bilinen en sert metal."))
    armors.append(Item("Kutsal Plaka", "legendary", "armor", {"defense": 55, "hp": 80}, "Kutsanmis."))
    
    # Godlike
    armors.append(Item("Olimpos Kalesi", "godlike", "armor", {"defense": 100, "hp": 250}, "Yürüyen bir kale."))
    armors.append(Item("Gaia'nin Kucagi", "godlike", "armor", {"defense": 90, "hp": 300}, "Toprak ana korur."))
    armors.append(Item("Olumsuzluk Zirhi", "godlike", "armor", {"defense": 120, "attack": 20}, "Olumu reddet."))
    
    return armors
