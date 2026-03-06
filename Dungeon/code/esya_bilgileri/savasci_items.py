from esya_bilgileri.item import Item

# SAVASCI SILAHLARI: KILIC (Sword)
def get_savasci_weapons():
    weapons = []
    
    # Common
    weapons.append(Item("Demir Kilic", "common", "weapon", {"attack": 8}, "Savascilarin baslangic silahi."))
    weapons.append(Item("Eski Palas", "common", "weapon", {"attack": 7, "defense": 1}, "Biraz koruma saglayan pasli bir palas."))
    weapons.append(Item("Pasli Balta", "common", "weapon", {"attack": 9, "speed": -1}, "Agir ama keskin."))
    
    # Rare
    weapons.append(Item("Celik Kilic", "rare", "weapon", {"attack": 15}, "Keskin ve dayanikli."))
    weapons.append(Item("Sovalye Kilici", "rare", "weapon", {"attack": 16, "defense": 2}, "Genc sovalyeler icin."))
    weapons.append(Item("Savas Baltasi", "rare", "weapon", {"attack": 18, "speed": -2}, "Yikici guc."))
    
    # Mystic
    weapons.append(Item("Golge Kilici", "mystic", "weapon", {"attack": 25, "speed": 1}, "Karanlikta parildayan bir kilic."))
    weapons.append(Item("Ruh Kesen", "mystic", "weapon", {"attack": 28, "mana": 10}, "Dusmanin ruhundan beslenir."))
    weapons.append(Item("Kanli Balta", "mystic", "weapon", {"attack": 30, "hp": 5}, "Surekli kanama yaratir."))
    
    # Legendary
    weapons.append(Item("Ejderha Katili", "legendary", "weapon", {"attack": 45, "hp": 20}, "Ejderha pullarini bile kesebilecek guctell."))
    weapons.append(Item("Kralin Adaleti", "legendary", "weapon", {"attack": 42, "defense": 10}, "Krallara layik denge."))
    weapons.append(Item("Cennetin Gazabi", "legendary", "weapon", {"attack": 50, "speed": 5}, "Simsek kadar hizli."))
    
    # Godlike
    weapons.append(Item("Ares'in Gazabi", "godlike", "weapon", {"attack": 80, "defense": 10}, "Savas Tanrisinin lutfu."))
    weapons.append(Item("Odin'in Mizragi", "godlike", "weapon", {"attack": 90, "speed": 3}, "Asla iskalama."))
    weapons.append(Item("Hel'in Dokunusu", "godlike", "weapon", {"attack": 75, "hp": 50}, "Olumcul bir dokunus."))
    
    return weapons

# SAVASCI ZIRHLARI: ZIRH (Armor)
def get_savasci_armors():
    armors = []
    
    # Common
    armors.append(Item("Deri Zirh", "common", "armor", {"defense": 5}, "Basit bir kumaş."))
    armors.append(Item("Ahsap Plaka", "common", "armor", {"defense": 4, "hp": 5}, "Hafif ve dayanikli."))
    armors.append(Item("Yipranmis Zirh", "common", "armor", {"defense": 6, "speed": -1}, "Eski savaslardan kalma."))
    
    # Rare
    armors.append(Item("Zincir Zirh", "rare", "armor", {"defense": 10, "speed": 1}, "Hafif ama etkili."))
    armors.append(Item("Demir Plaka", "rare", "armor", {"defense": 12}, "Standart piyade zirhi."))
    armors.append(Item("Muhafiz Zirhi", "rare", "armor", {"defense": 11, "hp": 10}, "Sehir muhafizlari giyer."))
    
    # Mystic
    armors.append(Item("Sovalye Zirhi", "mystic", "armor", {"defense": 20, "hp": 15}, "Sovalye nisanlari ile suslu."))
    armors.append(Item("Kara Plaka", "mystic", "armor", {"defense": 22, "attack": 2}, "Saldirgan bir savunma."))
    armors.append(Item("Buyulu Zirh", "mystic", "armor", {"defense": 18, "mana": 10}, "Buyuye karsi direnc."))
    
    # Legendary
    armors.append(Item("Ejder Pulu Zirh", "legendary", "armor", {"defense": 35, "hp": 50}, "Atese dayanikli efsanevi zirh."))
    armors.append(Item("Anka Kusu Zirhi", "legendary", "armor", {"defense": 30, "hp": 100}, "Kulleri uzerinde tasir."))
    armors.append(Item("Titan Zirhi", "legendary", "armor", {"defense": 45, "speed": -2}, "Devlerin gucu."))
    
    # Godlike
    armors.append(Item("Olympos Zirhi", "godlike", "armor", {"defense": 60, "hp": 150}, "Tanrilarin savasta giydigi zirh."))
    armors.append(Item("Herkul'un Postu", "godlike", "armor", {"defense": 55, "attack": 20}, "Yenilmez bir guc."))
    armors.append(Item("Yggdrasil Kabugu", "godlike", "armor", {"defense": 70, "hp": 300}, "Dunya agacindan bir parca."))
    
    return armors
