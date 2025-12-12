import random
from enemy import Enemy

class Floor:
    # This class spawns enemies and controls their difficulty and gives players xp on floor completion
    def __init__(self, floor_number = None, mob_list = None):
        self.floor_number = 0 if floor_number is None else floor_number
        # Avoid using a mutable default argument so each Floor gets its own list
        self.mob_list = [] if mob_list is None else mob_list
    
    # GET FUNCTIONS
    def get_floor_number(self): # FLOOR NUMBER
        return self.floor_number
    
    # sets the floor's xp value and increases it per floor
    def give_xp(self): # CALCULATES XP PER FLOOR
        # Calculate XP without modifying state; use base value of 20
        base_xp = 20
        # For floors above 1 scale XP more aggressively so players level by floor 2
        if self.floor_number <= 1:
            calculated_xp = base_xp
        elif self.floor_number == 10:
            calculated_xp = 0 # NO XP given on last floor
        else:
            multiplier = 1.5
            calculated_xp = round(self.floor_number * multiplier * base_xp)
        return calculated_xp
    
    def get_mob_list(self): # MOB LIST
        return self.mob_list
    
    # SET FUNCTIONS
    def set_mob_list(self,list):
        self.mob_list = list
    
    # Sets mob list
    def spawn_mobs(self):
        # the amount of mobs spawned and their difficulty must follow the floor number
        # Floor 1-3 will have 2 enemies, 4-6 will have 3, and 7-9 will have 4, and floor 10 is a boss floor
        difficulty = self.floor_number
        mob_level = (difficulty+1)//2
        # Increase mob health scaling slightly (but less than player's damage growth)
        mob_health = (difficulty * 1.5) + 25 # ADJUST VALUE FOR BALANCING
        # Reduce mob damage scaling so multiple enemies are less lethal
        mob_damage = (difficulty * 0.9) + 3 # ADJUST VALUE FOR BALANCING
        # mob count will increases by 1 every 3 floor
        mob_amount = ((difficulty+2)//3)
        
        # for floor 1-9 create random mobs and add to list
        if self.get_floor_number() < 10:
            # loops based on mob amount
            for i in range(mob_amount+1):
                # creates a new enemy object with random class, type, and calculated health/max health, damage, and level
                enemy = Enemy(random.choice(Enemy.COMBAT_CLASSES), random.choice(Enemy.ENEMY_TYPES), round(mob_health), round(mob_health), round(mob_damage), mob_level)
                # stores the enemy's combat class
                enemy_combat_class = enemy.get_combat_class()
                # stores the enemy's health
                enemy_health = enemy.get_health()
                # match case to adjust health and damge based on class
                match enemy_combat_class:
                    # FIGHTER CLASS, Massively increased health and slightly increased damage (TANK ARCHETYPE)
                    case "FIGHTER":
                        enemy_health *= 1.5
                        enemy.set_damage(round(enemy.get_damage() * 1.1))
                    # MAGE CLASS, Moderately reduce health and massively increase damge (RANGED ARCHETYPE)
                    case "MAGE":
                        enemy_health *= 0.7
                        enemy.set_damage(round(enemy.get_damage() * 1.5))
                    # ROGUE CLASS, Slightly reduced health and moderately increase damage (ASSASSIN ARCHETYPE)
                    case "ROGUE":
                        enemy_health *= 0.9
                        enemy.set_damage(round(enemy.get_damage() * 1.3))
                    # CLERIC CLASS, Slightly/Moderately reduced health and massively reduced damage (HEALER ARCHETYPE)
                    case "CLERIC":
                        enemy_health *= 0.8
                        enemy.set_damage(round(enemy.get_damage()* 0.4))
                # sets health and max health based on the adjustments made
                enemy.set_health(round(enemy_health))
                enemy.set_max_health(enemy.get_health())
                # adds enemy to the floor's mob list
                self.mob_list.append(enemy)
        # if floor number is 10 (last floor), summons a boss monster
        elif self.get_floor_number() == 10:
            enemy = Enemy("BOSS","BOSS: Dragon", 600, 600, 25, 10) # ADJUST VALUE FOR BALANCING
            # adds boss to floor's list of enemy
            self.mob_list.append(enemy)
    
    # sets xp granted
    def set_xp_given(self, xp_granted):
        self.xp_granted = xp_granted
    
    # prints the floor info
    def __str__(self):
        return f"This is floor {self.get_floor_number()}. The enemies on this floor are {self.get_mob_list()}"