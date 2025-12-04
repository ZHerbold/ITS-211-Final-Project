
import random

class Player:
    def __init__(self, max_health = 100, current_health = 100, max_damage = 10, level = 1, xp = 0, max_xp = 80, equipment = None, xp_growth = 1.12):
        self.max_health = max_health
        self.current_health = current_health
        self.damage = max_damage
        self.level = level
        self.xp = xp
        self.base_max_xp = max_xp
        self.xp_growth = xp_growth
        self.max_xp = max_xp
        self.equipment = [] if equipment is None else equipment
    
    # getter functions
    def get_max_health(self): # MAX HEALTH
        return self.max_health
    
    def get_current_health(self): # CURRENT HEALTH
        return self.current_health
    
    def get_xp(self): # XP
        return self.xp
    
    def get_max_xp(self): # XP THRESHOLD
        return self.max_xp
    
    def get_level(self): # LEVEL
        return self.level
    
    def get_damage(self): # DAMAGE
        return self.damage
    
    def get_equipment(self): # EQUIPMENT
        return self.equipment
    
    # setter functions
    def level_up(self):
        self.level += 1
        # Increase max health and damage on level up
        self.max_health = round(self.get_max_health() * 1.15)
        # Increase damage growth per level to 20%
        self.damage = round(self.get_damage() * 1.20)
    
    def raise_max_xp(self):
        # Recalculate max_xp using exponential growth from base_max_xp
        self.max_xp = round(self.base_max_xp * (self.xp_growth ** (self.level - 1)))

    def gain_experience(self, xp_gained):
        # Allow multiple level-ups from a single XP gain
        self.xp += xp_gained
        leveled = False
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level_up()
            self.raise_max_xp()
            leveled = True
        return leveled
    
    def set_current_health(self, health):
        self.current_health = health
    
    def load_save(self, max_health, current_health, max_damage, level, xp, max_xp, equipment):
        self.max_health = max_health
        self.current_health = current_health
        self.damage = max_damage
        self.level = level
        self.xp = xp
        self.max_xp = max_xp
        self.equipment = equipment

    # player functions
    def attack(self, other):
        damage = random.randint(self.get_damage()-2,self.get_damage())
        other.take_damage(damage)
        print(f"You have attacked {other.get_type()} for {damage} damage!")
    
    def take_damage(self, damage):
        self.set_current_health(round(self.get_current_health() - damage))
    
    def heal(self):
        heal_amount = 50
        if (heal_amount + self.get_current_health() > self.get_max_health()):
            self.set_current_health(self.get_max_health())
        else:
            self.current_health += heal_amount

    def __str__(self):
        return f"PLAYER | HP {self.get_current_health()}/{self.get_max_health()} | LEVEL {self.get_level()} | XP {self.get_xp()}/{self.get_max_xp()}"
    
    def __repr__(self):
        return f"{self.get_max_health()},{self.get_current_health()},{self.get_damage()},{self.get_level()},{self.get_xp()},{self.get_max_xp()},{self.get_equipment()}"