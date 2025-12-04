# Imports all classes
from enemy import Enemy
from player import Player
from floor import Floor
from customerrors import *
import time

def load_tower_save(list):
    raw_info = list
    processed_tower_list = []
    for raw_floor_list in raw_info:
        processed_floor_list = []
        raw_mob_list = raw_floor_list.split("|")
        for mob in raw_mob_list:
            mob_info = mob.split(",")
            if len(mob_info) != 1:
                processed_floor_list.append(Enemy(str(mob_info[0]),int(mob_info[1]),int(mob_info[2]),int(mob_info[3])))
        processed_tower_list.append(processed_floor_list)
    return processed_tower_list
        
# Creates the player
player = Player()

# creates the "tower" with 10 floors
tower = [] # tower list to hold floors

# loop 10 times to make 10 floors
for i in range(10):
    # appends a floor to the list with the appropiate floor number
    tower.append(Floor(i+1))

# create a empty list to hold list of mobs in it
tower_mob_list = []

# loop through each floor object in the tower list and create enemies
for floor in tower:
    floor.spawn_mobs()
    # adds the list of mob to the master list of mobs
    tower_mob_list.append(floor.get_mob_list())

# sets the floor index to 0 (for list purposes). The "player-facing" floor number is 1, but 0 for indexing purposes
current_floor_index = 0

# loop to load a save file
while True:

    try:
        # save player info into memory
        savefile = open("playersave.txt", "r")
        playersave = savefile.readlines()
        savefile.close()

        # save tower info into memory
        towersave = []
        with open("towersave.txt", "r") as file:
            for line in file:
                towersave.append(line.strip())
        savefile.close()

        if len(playersave) == 0 or len(towersave) == 0:
            break
        else:
            playerinfo = playersave[0].split(",")
            player.load_save(int(playerinfo[0]),int(playerinfo[1]),int(playerinfo[2]),int(playerinfo[3]),int(playerinfo[4]),int(playerinfo[5]),eval(playerinfo[6]))
            current_floor_index = int(playerinfo[7])
            tower_mob_list = load_tower_save(towersave)
            i = 0
            for floor in tower:
                floor.set_mob_list(tower_mob_list[i])
                i += 1
            break
    
    except Exception as e:
        print("ERROR:",e)
        print("No save file found, starting new game!")
        time.sleep(1)
        break

# gameplay loop
while True:
    # try and except block to catch errors
    try:
        # this is the "current" floor monster list
        enemy_list = tower_mob_list[current_floor_index]
        # sets a couple of variables to check if the mobs and player are still alive
        enemies_alive = True
        player_alive = True
        living_counter = 0
        # loops through the list of enemies and check if their health is greater than zero
        for enemy in enemy_list:
            if enemy.get_health() > 0:
                living_counter += 1
        # if no enemy has health greater than zero, that means they're all dead
        if living_counter == 0:
            enemies_alive = False
        
        if player.get_current_health() <= 0:
            player_alive = False
        
        # if both the enemy and player are alive, game continues as normal
        if enemies_alive and player_alive:
            # Print out user info and floor number
            print(f"\n\nFLOOR {tower[current_floor_index].get_floor_number()}")
            time.sleep(1)
            print(player)
            time.sleep(1)
            print()
            # Print out the enemy list
            selection_number = 1
            for enemy in enemy_list:
                print(f"[{selection_number}] {enemy}")
                selection_number += 1
            print()
            time.sleep(1)

            # PLAYER TURN
            attack_or_heal_choice = input("[A] Attack Enemy | [B] Heal | [Q] Save and Quit: ").upper()
            if attack_or_heal_choice == "B":
                player.heal()
                print("The player has healed for 50 points!")
                print(f"The player now has {player.get_current_health()} / {player.get_max_health()}.")
                time.sleep(2)
            elif attack_or_heal_choice == "A":
                choice = int(input("Which enemy would you like to attack? "))
                if 0 <= choice and choice <= len(enemy_list):
                    selected_enemy = enemy_list[choice - 1]
                    if selected_enemy.get_health() > 0:
                        player.attack(selected_enemy)
                        time.sleep(1)
                    else:
                        print("This enemy is dead!")
                        time.sleep(1)
                else:
                    raise InvalidEnemyChoice
            elif attack_or_heal_choice == "Q":
                # SAVE THE TOWER INFO
                savefile = open("towersave.txt", "w")
                for floor_mob_list in tower_mob_list:
                    for mob in floor_mob_list:
                        savefile.write(f"{repr(mob)}|")
                    savefile.write("\n")
                savefile.close()

                # SAVE THE PLAYER INFO AND CURRENT FLOOR
                savefile = open("playersave.txt", "w")
                savefile.write(f"{repr(player)},{current_floor_index}")
                savefile.close()
                break
            else:
                raise InvalidGameChoice
            
            print()
            time.sleep(1)
            # ENEMY TURN
            for enemy in enemy_list:
                if enemy.get_health() > 0:
                    enemy.attack(player)
                    time.sleep(0.5)
                    print(f"You have {player.get_current_health()} health points left.")
        elif player_alive == False:
            print("YOU DIED!")
            break
        else:
            print("All enemies are dead. You Cleared This Floor!")
            time.sleep(1)
            if player.gain_experience(tower[current_floor_index].give_xp()):
                print(f"LEVEL UP! You are now level {player.get_level()}!")
            time.sleep(1)
            current_floor_index = current_floor_index + 1
            if current_floor_index < 10:
                print("MOVING TO THE NEXT FLOOR!\nFLOOR", current_floor_index + 1)
                time.sleep(1)
            else:
                print("YOU WIN!!!!!")
                break
    except ValueError:
        print("Please enter a number to attack any of the enemy (e.g., to attack [1] Skeleton, type 1 and press enter).")
        time.sleep(0.5)
    except InvalidEnemyChoice:
        if choice > len(enemy_list):
            print(f"There are only {len(enemy_list)} enemies. Please select one of them.")
            time.sleep(0.5)
        elif choice <= 0:
            print("Please enter a positive number.")
            time.sleep(0.5)
    except InvalidGameChoice:
        print("Please enter 'A' or 'B' to either attack the enemy or heal yourself or 'Q' to save and quit.")
        time.sleep(0.5)
    except Exception as e:
        print(f"An error occured: {e}")
        time.sleep(1)
        break

