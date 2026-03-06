import random
from esya_bilgileri.item import Item

def get_accessories():
    accessories = []
    
    # Common Accessories
    accessories.append(Item("Bakir Yuzuk", "common", "accessory", {"mana": 10}, "Biraz enerji verir."))
    accessories.append(Item("Deri Bileklik", "common", "accessory", {"hp": 15}, "Şansı artırır."))
    accessories.append(Item("Demir Yuzuk", "common", "accessory", {"defense": 1}, "Basit demir."))
    accessories.append(Item("Tahta Kolye", "common", "accessory", {"mana": 5}, "Koylu kolyesi."))
    accessories.append(Item("Ip Bileklik", "common", "accessory", {"speed": 1}, "Hizlandirir."))
    accessories.append(Item("Eski Madalyon", "common", "accessory", {"defense": 2}, "Eski bir hatira."))
    
    # Rare Accessories
    accessories.append(Item("Alev Yuzugu", "rare", "accessory", {"attack": 5}, "Sıcak hissettirir."))
    accessories.append(Item("Buz Kolyesi", "rare", "accessory", {"defense": 5}, "Soğuk bir dokunuş."))
    accessories.append(Item("Gumus Yuzuk", "rare", "accessory", {"defense": 3, "hp": 10}, "Saf gumus."))
    accessories.append(Item("Altin Yuzuk", "rare", "accessory", {"hp": 30}, "Zenginlik belirtisi."))
    accessories.append(Item("Zumrut Kupe", "rare", "accessory", {"speed": 2}, "Sans getirir."))
    accessories.append(Item("Yakut Bileklik", "rare", "accessory", {"attack": 4}, "Savasci kani."))
    
    # Mystic Accessories
    accessories.append(Item("Zehirli Yuzuk", "mystic", "accessory", {"attack": 10, "speed": 2}, "Zehir saçar."))
    accessories.append(Item("Hiz Bilekligi", "mystic", "accessory", {"speed": 8}, "Daha hızlı hareket et."))
    accessories.append(Item("Guc Yuzugu", "mystic", "accessory", {"attack": 15}, "Saf guc."))
    accessories.append(Item("Buyucu Kolyesi", "mystic", "accessory", {"attack": 12, "mana": 20}, "Buyuculer icin."))
    accessories.append(Item("Sifa Tilsimi", "mystic", "accessory", {"hp": 70}, "Can yeniler."))
    accessories.append(Item("Vampir Yuzugu", "mystic", "accessory", {"attack": 8, "hp": 20}, "Kan icer."))
    accessories.append(Item("Koruma Muskasi", "mystic", "accessory", {"defense": 10}, "Kotulukten korur."))
    
    # Legendary Accessories
    accessories.append(Item("Kralin Yuzugu", "legendary", "accessory", {"hp": 50, "attack": 10, "defense": 10}, "Krallara layık."))
    accessories.append(Item("Olumun Dokunusu", "legendary", "accessory", {"attack": 30, "speed": 5}, "Her vuruşta hayat çalar."))
    accessories.append(Item("Ejderha Gozu", "legendary", "accessory", {"attack": 35}, "Ejderha buyusu."))
    accessories.append(Item("Anka Tuyu", "legendary", "accessory", {"hp": 150}, "Yeniden dogus."))
    accessories.append(Item("Bilgelik Taci", "legendary", "accessory", {"mana": 100}, "Sonsuz bilgi."))
    accessories.append(Item("Savas Lordu Madalyonu", "legendary", "accessory", {"attack": 25, "defense": 15}, "Sorumluluk."))
    accessories.append(Item("Element Yuzugu", "legendary", "accessory", {"defense": 25}, "Elementlere hukmet."))
    
    # Godlike Accessories
    accessories.append(Item("Zamanin Kum Saati", "godlike", "accessory", {"speed": 40}, "Zamanı büker."))
    accessories.append(Item("Her Seyin Gozu", "godlike", "accessory", {"attack": 100}, "Hiçbir şey kaçmaz."))
    accessories.append(Item("Kaderin Ipi", "godlike", "accessory", {"hp": 500, "mana": 500}, "Kader parmaklarinin ucunda."))
    accessories.append(Item("Ruh Tasi", "godlike", "accessory", {"attack": 30, "hp": 500}, "Ruhlari hapseder."))
    accessories.append(Item("Tanrilarin Lutfu", "godlike", "accessory", {"hp": 300, "attack": 30, "defense": 30}, "Olu degil, olumsuz."))
    accessories.append(Item("Kaosun Cekirdegi", "godlike", "accessory", {"attack": 120}, "Saf kaos."))
    accessories.append(Item("Yasam Pinari", "godlike", "accessory", {"hp": 1500}, "Tukenemez yasam."))
    
    return accessories

def generate_random_accessory():
    base_acc = random.choice(get_accessories())
    return base_acc
