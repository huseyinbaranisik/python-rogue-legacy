from esya_bilgileri.item import Item

# HAYDUT SILAHLARI: HANCER (Dagger)
def get_haydut_weapons():
    weapons = []
    
    # Common
    weapons.append(Item("Pasli Hancer", "common", "weapon", {"attack": 5, "speed": 1}, "Eski ve paslanmış."))
    weapons.append(Item("Mutfak Bicagi", "common", "weapon", {"attack": 4, "speed": 2}, "Savas icin degil."))
    weapons.append(Item("Kirik Cam", "common", "weapon", {"attack": 6, "speed": 1}, "Keskin parca."))
    
    # Rare
    weapons.append(Item("Keskin Bicak", "rare", "weapon", {"attack": 12, "speed": 2}, "Ucu zehirli."))
    weapons.append(Item("Avci Hanceri", "rare", "weapon", {"attack": 10, "speed": 3}, "Ormana uygun."))
    weapons.append(Item("Kivrik Kama", "rare", "weapon", {"attack": 15, "speed": 1}, "Ozel tasarim."))
    
    # Mystic
    weapons.append(Item("Kan Emici", "mystic", "weapon", {"attack": 22, "speed": 3}, "Düşmanın kanıyla beslenir."))
    weapons.append(Item("Golge Bicagi", "mystic", "weapon", {"attack": 18, "speed": 5}, "Golge gibi."))
    weapons.append(Item("Ruh Calan", "mystic", "weapon", {"attack": 20, "mana": 10}, "Ruhlari alir."))
    
    # Legendary
    weapons.append(Item("Gece Bicagi", "legendary", "weapon", {"attack": 35, "speed": 10}, "Karanlıkta görünmez olur."))
    weapons.append(Item("Suikastcinin Gozyasi", "legendary", "weapon", {"attack": 40, "energy": 20}, "Son darbe."))
    weapons.append(Item("Tehdit Kararli", "legendary", "weapon", {"attack": 45, "speed": 8}, "Nereden geldi?"))
    
    # Godlike
    weapons.append(Item("Loki'nin Hançeri", "godlike", "weapon", {"attack": 80, "speed": 15}, "Tanrıların bile kaçamayacağı bir tuzak."))
    weapons.append(Item("Hermes'in Hanceri", "godlike", "weapon", {"attack": 60, "speed": 30}, "Inanilmaz hiz."))
    weapons.append(Item("Azrail'in Tirpani", "godlike", "weapon", {"attack": 100, "hp": 100}, "Can alici."))
    
    return weapons

# HAYDUT ZIRHLARI: PELERIN (Cloak)
def get_haydut_armors():
    armors = []
    
    # Common
    armors.append(Item("Yırtık Pelerin", "common", "armor", {"speed": 1}, "Rüzgarda savrulur."))
    armors.append(Item("Kahverengi Pelerin", "common", "armor", {"defense": 1, "speed": 1}, "Basit kamuflaj."))
    armors.append(Item("Kapusonlu Ust", "common", "armor", {"defense": 2, "hp": 5}, "Yuzunu gizler."))
    
    # Rare
    armors.append(Item("Gezgin Pelerini", "rare", "armor", {"speed": 3, "defense": 2}, "Uzak diyarlardan."))
    armors.append(Item("Deri Ceket", "rare", "armor", {"defense": 5, "hp": 5}, "Saglam deri."))
    armors.append(Item("Avci Kiyafet", "rare", "armor", {"defense": 4, "speed": 5}, "Hizli hareket."))
    
    # Mystic
    armors.append(Item("Golge Pelerini", "mystic", "armor", {"speed": 10, "defense": 3}, "Gölgelerde kaybolmanı sağlar."))
    armors.append(Item("Gece Kiyafet", "mystic", "armor", {"defense": 8, "hp": 15}, "Gece kadar siyah."))
    armors.append(Item("Sis Pelerini", "mystic", "armor", {"speed": 12, "defense": 2}, "Sisten yapilmis."))
    
    # Legendary
    armors.append(Item("Hayalet Pelerini", "legendary", "armor", {"speed": 15, "defense": 5}, "Fiziksel saldırılar içinden geçer."))
    armors.append(Item("Ruzgar Yuruyusu", "legendary", "armor", {"speed": 20, "defense": 8}, "Ruzgar gibi."))
    armors.append(Item("Hiclik Ortusu", "legendary", "armor", {"defense": 15, "mana": 20}, "Buyusuzluk."))
    
    # Godlike
    armors.append(Item("Tanrisal Pelerin", "godlike", "armor", {"speed": 25, "defense": 20}, "Tanrisi tarafindan kutsanmis."))
    armors.append(Item("Gorunmezlik Pelerini", "godlike", "armor", {"speed": 40, "defense": 10}, "Tamamen gorunmezlik."))
    armors.append(Item("Kaos Ortusu", "godlike", "armor", {"defense": 40, "hp": 100}, "Kaosu yansit."))
    
    return armors
