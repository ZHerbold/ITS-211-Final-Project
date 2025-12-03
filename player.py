class Player:
    def __init__(self, max_health = 100, current_health = 100, damage = 10, level = 1, xp = 0, equipment = []):
        self.max_health = max_health
        self.current_health = current_health
        self.damage = damage
        self.level = level
        self.xp = xp
        self.equipment = equipment
    
    # getter functions
    def get_max_health(self):
        return self.max_health
    
    def get_current_health(self):
        return self.current_health
    
    def get_xp(self):
        return self.xp
    
    def get_level(self):
        return self.level
    
    def get_damage(self):
        return self.damage
    
    def get_equipment(self):
        return self.equipment
    
    # setter functions
    def take_damage(self, damage):
        self.current_health -= damage

    def set_damage(self, weapon_damage):
        self.damage = weapon_damage
    
    def level_up(self):
        self.level += 1
        self.max_health = round(self.get_max_health() * 1.1)
    
    def gain_experience(self, xp_gained):
        self.xp += xp_gained
    
    def set_current_health(self, health):
        self.health = health
    # player functions
    def attack(self, other):
        other.take_damage(self.get_damage())
    
    def take_damage(self, damage_taken):
        health = self.get_current_health()
        health = health - damage_taken
        self.set_current_health(health)
    
    def heal(self):
        heal_amount = 50
        if (heal_amount + self.get_current_health() > self.get_max_health()):
            self.set_current_health(self.get_max_health())
        self.current_health