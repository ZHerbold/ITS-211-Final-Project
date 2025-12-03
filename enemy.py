class Enemy:
    def __init__(self, type = "Undead", health = 50, damage = 5, level = 1):
        self.type = type
        self.health = health
        self.damage = damage
        self.level = level

    # getter functions
    def get_type(self):
        return self.type

    def get_health(self):
        return self.health
    
    def get_damage(self):
        return self.damage
    
    def get_level(self):
        return self.level
    
    # setter functions
    def set_type(self, type):
        self.type = type

    def set_health(self, health):
        self.health = health

    def set_damage(self, damage):
        self.damage = damage
    
    def set_level(self, level):
        self.level = level

    # enemy functions
    def take_damage(self, damage_taken):
        health = self.get_health()
        health = health - damage_taken
        self.set_health(health)
    
    def attack(self, other):
        other.take_damage(self.get_damage())
        
    def __str__(self):
        if self.get_health() > 0:
            return f"{self.get_type()} : Level {self.get_level()} has {self.get_health()} health points left."
        else:
            return f"{self.get_type()} : Level {self.get_level()} is DEAD"

