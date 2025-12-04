import random
class Enemy:
    # Enemy variables
    ENEMY_TYPES = ["Zombie", "Skeleton", "Slime", "Mimic", "Ghost", "Living Armor", "Goblin", "Orc", "Golem"]
    
    def __init__(self, type = "Unknown Monster", health = -1, damage = -1, level = -1):
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
        damage = random.randint(self.get_damage()-2,self.get_damage())
        other.take_damage(damage)
        print(f"Level {self.get_level()} {self.get_type()} has attacked the level {other.get_level()} player for {damage} health points!")
        
    def __str__(self):
        if self.get_health() > 0:
            return f"Level {self.get_level()} {self.get_type()} has {self.get_health()} health points left."
        else:
            return f"Level {self.get_level()} {self.get_type()} is DEAD"
    
    def __repr__(self):
        return f"{self.get_type()},{self.get_health()},{self.get_damage()},{self.get_level()}"