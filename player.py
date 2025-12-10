
import random

class Player:
    # creates a new player
    def __init__(self, xp_growth = 1.12, critical_chance = 0.25):
        # calls the reset function to create a default player
        self.reset()
        # sets the xp growth rate and critical chance
        self.xp_growth = xp_growth
        self.critical_chance = critical_chance
    
    # This function is called twice, one in init and when player dies and chooses to restart the tower
    # either way, this function resets all stats to default values
    def reset(self):
        # max health prevents over-heals
        self.max_health = 100
        # current health tracks damage taken and if 0 or negative, player death
        self.current_health = 100
        # tracks current level
        self.level = 1
        # tracks current xp
        self.xp = 0
        # sets max xp so that if current xp is equal to or greater than the max, player levels up
        self.max_xp = 80
        # base max to do some wonky calculations
        self.base_max_xp = self.max_xp
        # sets current default equipment and damage multiplier
        self.equipment = {"Wooden Sword":1}
        # String to track current equipment and is used to find the value of the equipment (damage multiplier)
        self.currently_equipped = "Wooden Sword"
        # sets damage to base of 10 and is multiplied by current equipment the first time
        self.base_damage = 10
        # final damage calculation based on equipment
        self.attack_damage = self.base_damage * self.equipment[self.currently_equipped]

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
        return self.base_damage
    
    def get_attack_damage(self): # POST EQUIPMENT DAMAGE
        self.attack_damage = round(self.get_damage() * self.equipment[self.get_currently_equipped()])
        return self.attack_damage
    
    def get_equipment(self): # EQUIPMENT DICT
        return self.equipment
    
    def get_currently_equipped(self): # CURRENT EQUIPMENT
        return self.currently_equipped
    
    def get_critical_chance(self): # CRITICAL CHANCE
        return self.critical_chance
    
    # setter functions
    # This function lets the player level up when called
    def level_up(self):
        # increases level
        self.level += 1
        # lets the user know they leveled up
        print(f"LEVEL UP! You are now level {self.get_level()}!")
        # Increase max health and damage on level up
        self.max_health = round(self.get_max_health() * 1.15) # ADJUST VALUE FOR BALANCING
        # Increase base damage growth per level by 13%
        self.set_damage(round(self.get_damage() * 1.13)) # ADJUST VALUE FOR BALANCING
    
    # sets the damage
    def set_damage(self, damage):
        self.base_damage = damage
    
    # sets the attack damage
    def set_attack_damage(self, damage):
        self.attack_damage = damage

    # sets the equipment dictionary
    def set_equipment(self, equipment):
        self.equipment = equipment
    
    # increases the max xp
    def raise_max_xp(self):
        # Recalculate max_xp using exponential growth from base_max_xp. The base max xp is multiplied by the xp growth rate to the power of the player's level - 1
        self.max_xp = round(self.base_max_xp * (self.xp_growth ** (self.level - 1)))

    # Increases the current xp
    def gain_experience(self, xp_gained):
        # Allow multiple level-ups from a single XP gain
        self.xp += xp_gained
        while self.xp >= self.max_xp:
            # subtracts the max xp from the current xp
            self.xp -= self.max_xp
            # levels up the player
            self.level_up()
            # raises the max xp
            self.raise_max_xp()
    
    # sets health
    def set_current_health(self, health):
        self.current_health = health
    
    # function to load save, is called in main to load stats from file
    def load_save(self, max_health, current_health, max_damage, level, xp, max_xp, equipment, currently_equipped):
        self.max_health = max_health
        self.current_health = current_health
        self.base_damage = max_damage
        self.level = level
        self.xp = xp
        self.max_xp = max_xp
        self.equipment = equipment
        self.currently_equipped = currently_equipped

    # player functions
    # player's attack function
    def attack(self, other):
        # the damage is random from max damage - 2 to max damage (e.g., 4-6, 10-12, 100-102, etc.)
        damage = random.randint(self.get_attack_damage()-2,self.get_attack_damage())
        # rolls the critical chance roll from a float from 0 - 1
        critical_roll = random.uniform(0,1)
        # sets is critical to false (for text display reasons)
        is_critical = False
        # if the critical chance of the player is greater than or equal to the critical rolled, critical is true
        # example, critical roll is 0.64 but the player chance is 0.25, this means the crit failed
        # if roll is 0.15, then the crit succeed
        if critical_roll <= self.get_critical_chance():
            # critical damage is increased by 50%
            damage = round(damage * 1.5)
            # sets is critical to true
            is_critical = True
        # calls the other's take damage method (found in the enemy.py)
        other.take_damage(damage)
        # If the crit succeed, it will display CRITICAL HIT at the end of the print statement
        crit_text = "CRITICAL HIT!" if is_critical == True else ""
        # Lets the player know how much damage they did
        print(f"You have attacked {other.get_type()} for {damage} damage! {crit_text}")
    
    # takes damage (used in the enemy's attack method)
    def take_damage(self, damage):
        # reduces the player health by how much damage was given
        self.set_current_health(round(self.get_current_health() - damage))
    
    # lets the player heal themselves for 50 points
    def heal(self):
        # healing is set to 50 throughout the game
        heal_amount = 50
        # this bit of code prevents overhealing and sets health accordingly
        if (heal_amount + self.get_current_health() > self.get_max_health()):
            self.set_current_health(self.get_max_health())
        else:
            self.current_health += heal_amount
    
    # adds a new equipment to the equipment dictionary and increases the player damage
    def equip(self, equipment_name, multiplier):
        # adds equipment to dictionary
        self.equipment[equipment_name] = multiplier
        self.currently_equipped = equipment_name

    # string magic method to display player's stats to the player
    def __str__(self):
        return f"PLAYER | HP {self.get_current_health()}/{self.get_max_health()} | LEVEL {self.get_level()} | XP {self.get_xp()}/{self.get_max_xp()} | EQUIPPED: {self.get_currently_equipped().upper()}"
    
    # repr magic method for saving purposes
    def __repr__(self):
        return f"{self.get_max_health()},{self.get_current_health()},{self.get_damage()},{self.get_level()},{self.get_xp()},{self.get_max_xp()},{self.get_equipment()},{self.get_currently_equipped()}"