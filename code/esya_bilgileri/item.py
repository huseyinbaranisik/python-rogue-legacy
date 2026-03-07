from utils import Colors, get_rainbow_text

class Item:
    def __init__(self, name, rarity, item_type, stats=None, description=""):
        self.name = name
        self.rarity = rarity # common, rare, mystic, legendary, godlike
        self.item_type = item_type # weapon, armor, accessory
        self.stats = stats if stats else {}
        self.description = description

    def get_colored_name(self):
        """Eswanin nadirligine gore renkli adini dondurur."""
        if self.rarity == "common":
            return f"{Colors.GREY}{self.name}{Colors.RESET}"
        elif self.rarity == "rare":
            return f"{Colors.CYAN}{self.name}{Colors.RESET}"
        elif self.rarity == "mystic":
            return f"{Colors.PURPLE}{self.name}{Colors.RESET}"
        elif self.rarity == "legendary":
            return f"{Colors.YELLOW}{self.name}{Colors.RESET}"
        elif self.rarity == "godlike":
            return get_rainbow_text(self.name)
        else:
            return self.name

    def get_stats_str(self):
        """Eşyanın özelliklerini formatlı bir dize olarak döndürür."""
        if not self.stats:
            return ""
        
        stat_map = {
            "hp": "Can",
            "max_hp": "Can",
            "mana": "Mana",
            "max_mana": "Mana",
            "energy": "Enerji",
            "max_energy": "Enerji",
            "attack": "Hasar",
            "defense": "Savunma",
            "speed": "Hız"
        }
        
        parts = []
        for key, val in self.stats.items():
            stat_name = stat_map.get(key, key.capitalize())
            sign = "+" if val >= 0 else ""
            parts.append(f"{sign}{val} {stat_name}")
            
        return "(" + ", ".join(parts) + ")"

    def __str__(self):
        return f"{self.get_colored_name()} {self.get_stats_str()}"
