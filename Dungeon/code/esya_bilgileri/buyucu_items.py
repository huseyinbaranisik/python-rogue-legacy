from esya_bilgileri.item import Item

# BUYUCU SILAHLARI: ASA (Staff)
def get_buyucu_weapons():
    weapons = []
    
    # Common
    weapons.append(Item("Tahta Asa", "common", "weapon", {"attack": 8}, "Sıradan bir ağaç dalı."))
    weapons.append(Item("Cirak Asasi", "common", "weapon", {"attack": 6, "mana": 10}, "Baslangic asasi."))
    weapons.append(Item("Egri Dal", "common", "weapon", {"attack": 7, "energy": 5}, "Yasli bir agactan."))
    
    # Rare
    weapons.append(Item("Kristal Asa", "rare", "weapon", {"attack": 15, "mana": 15}, "Enerji ile parlayan bir asa."))
    weapons.append(Item("Yakut Asa", "rare", "weapon", {"attack": 18, "hp": 5}, "Ates buyusunu guclendirir."))
    weapons.append(Item("Bilge Asasi", "rare", "weapon", {"attack": 12, "mana": 20}, "Eski bir bilgenin."))
    
    # Mystic
    weapons.append(Item("Alev Asasi", "mystic", "weapon", {"attack": 25, "hp": 10}, "Ucundaki alev hiç sönmez."))
    weapons.append(Item("Buz Asasi", "mystic", "weapon", {"attack": 22, "energy": 20}, "Daglardan gelen soguk."))
    weapons.append(Item("Yildirim Asasi", "mystic", "weapon", {"attack": 30, "speed": 2}, "Simsekler cakar."))
    
    # Legendary
    weapons.append(Item("Hiclik Asasi", "legendary", "weapon", {"attack": 40, "mana": 50}, "Gerçekliğin dokusunu büker."))
    weapons.append(Item("Zaman Asasi", "legendary", "weapon", {"attack": 35, "speed": 5}, "Zamani manipule eder."))
    weapons.append(Item("Arkana Asasi", "legendary", "weapon", {"attack": 50, "mana": 30}, "Saf buyu gucu."))
    
    # Godlike
    weapons.append(Item("Zeus'un Yildirimi", "godlike", "weapon", {"attack": 80, "speed": 10}, "Tanrısal güçle dolu."))
    weapons.append(Item("Merlin'in Asasi", "godlike", "weapon", {"attack": 70, "mana": 200}, "Efsanevi buyucunun mirasi."))
    weapons.append(Item("Kozmik Asa", "godlike", "weapon", {"attack": 100, "energy": 50}, "Evrenin enerjisini yonet."))
    
    return weapons

# BUYUCU ZIRHLARI: CUPPE (Robe)
def get_buyucu_armors():
    armors = []
    
    # Common
    armors.append(Item("Keten Cuppe", "common", "armor", {"defense": 2}, "Basit bir kumaş."))
    armors.append(Item("Yirtik Cuppe", "common", "armor", {"defense": 1, "hp": 5}, "Cok kullanilmis."))
    armors.append(Item("Cirak Cuppesi", "common", "armor", {"defense": 3, "mana": 10}, "Ogrenciler icin."))
    
    # Rare
    armors.append(Item("Ipek Cuppe", "rare", "armor", {"defense": 4, "mana": 15}, "Hafif ve rahat."))
    armors.append(Item("Kadife Cuppe", "rare", "armor", {"defense": 5, "hp": 10}, "Luks gorunumlu."))
    armors.append(Item("Rahip Cuppesi", "rare", "armor", {"defense": 6, "energy": 10}, "Tapinak rahiplerinin."))
    
    # Mystic
    armors.append(Item("Yildiz Isigi Cuppesi", "mystic", "armor", {"defense": 8, "mana": 30}, "Gece kadar karanlık."))
    armors.append(Item("Ay Isigi Cuppesi", "mystic", "armor", {"defense": 10, "energy": 20}, "Ay isigi ile parlar."))
    armors.append(Item("Gunes Cuppesi", "mystic", "armor", {"defense": 9, "hp": 20}, "Gunesin sicakligi."))
    
    # Legendary
    armors.append(Item("Safir Cuppe", "legendary", "armor", {"defense": 15, "mana": 60}, "Büyüsel enerji yayar."))
    armors.append(Item("Zumrut Cuppe", "legendary", "armor", {"defense": 18, "hp": 50}, "Doga ile uyumlu."))
    armors.append(Item("Element Cuppesi", "legendary", "armor", {"defense": 20, "energy": 40}, "Elementlere hukmeder."))
    
    # Godlike
    armors.append(Item("Sonsuzluk Cuppesi", "godlike", "armor", {"defense": 30, "mana": 200}, "Zamanın ötesinden bir dokuma."))
    armors.append(Item("Galaksi Ortusu", "godlike", "armor", {"defense": 25, "speed": 10}, "Uzayin derinlikleri."))
    armors.append(Item("Tanrisal Dokuma", "godlike", "armor", {"defense": 40, "hp": 200}, "Tanrilarin elinden cikma."))
    
    return armors
