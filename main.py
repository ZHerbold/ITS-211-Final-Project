# Imports all classes and libraries
from enemy import Enemy
from player import Player
from floor import Floor
from customerrors import *
import time
import random

# function to create a tower (basically a list that stores floor objects)
def create_tower():
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
    # returns the revelant info
    return tower, tower_mob_list, current_floor_index

# function to load the tower info from file
def load_tower_save(list):
    # unprocessed info is stored
    raw_info = list
    # empty list
    processed_tower_list = []
    # loops through the raw info list
    for raw_floor_list in raw_info:
        # empty list
        processed_floor_list = []
        # splits the floor list into individual mobs with stats
        raw_mob_list = raw_floor_list.split("|")
        # for each mob string, split into usable info
        for mob in raw_mob_list:
            mob_info = mob.split(",")
            # this method usually leaves a emptyish string at the end which is ignored
            if len(mob_info) != 1:
                # creates a new enemy and adds to list
                processed_floor_list.append(Enemy(str(mob_info[0]), str(mob_info[1]),int(mob_info[2]),int(mob_info[3]),int(mob_info[4]),int(mob_info[5])))
        # appends the processed floor list to the processed tower list
        processed_tower_list.append(processed_floor_list)
    # returns the processed tower list for use
    return processed_tower_list

# saves the game info to file
def save_to_file():
    # SAVE THE TOWER INFO
    print("SAVING")
    # saves tower info with all the floor info and mob info
    savefile = open("towersave.txt", "w")
    # loops through each floor in the tower
    for floor_mob_list in tower_mob_list:
        # loops through each mob on the floor and saves the representation text with | at the end to be split when loading
        for mob in floor_mob_list:
            savefile.write(f"{repr(mob)}|")
        # new line = new floor
        savefile.write("\n")
    # closes file
    savefile.close()

    # SAVE THE PLAYER INFO AND CURRENT FLOOR
    savefile = open("playersave.txt", "w")
    # saves the player info and current floor number to playersave.txt
    savefile.write(f"{repr(player)},{current_floor_index}")
    # closes file
    savefile.close()
    # lets user know that file is saved
    print("SAVED\nQUITTING\nGOODBYE")

# Creates the player
player = Player()

# creates a new tower and stores the info
tower, tower_mob_list, current_floor_index = create_tower()

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

        # checks for empty file and exits loop without trying to load file
        if len(playersave) == 0 or len(towersave) == 0:
            raise EmptySaveFile
        # loads the player info into the player
        else:
            # splits the player save into list of stats
            playerinfo = playersave[0].split(",")
            # calls the load save function and feeds player info
            player.load_save(int(playerinfo[0]),int(playerinfo[1]),int(playerinfo[2]),int(playerinfo[3]),int(playerinfo[4]),int(playerinfo[5]),eval(playerinfo[6]),str(playerinfo[7]))
            # sets the floor index with saved floor index
            current_floor_index = int(playerinfo[8])

            # loads the tower save into list
            tower_mob_list = load_tower_save(towersave)
            # loops through each floor in tower and sets mob list in the floor object's list
            i = 0
            for floor in tower:
                floor.set_mob_list(tower_mob_list[i])
                i += 1
            break
    # Throws exception if there is no file found and exits loop
    except EmptySaveFile:
        print("Empty save file found, starting new game!")
        time.sleep(1)
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
        # this is the "current" floor monster list and prevents out of bounds error when loading a finished save
        if current_floor_index < 10:
            enemy_list = tower_mob_list[current_floor_index]
        else:
            enemy_list = tower_mob_list[9]
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
            if current_floor_index < 10:
                print(f"\n\nFLOOR {tower[current_floor_index].get_floor_number()}")
            else:
                print("GAME COMPLETED")
            print(player)
            print()
            # Print out the enemy list
            selection_number = 1
            for enemy in enemy_list:
                print(f"[{selection_number}] {enemy}")
                selection_number += 1
            print()

            # PLAYER TURN
            # asks player to choose what to do
            game_choice = input("[A] Attack Enemy | [B] Heal | [Q] Save and Quit: ").upper()
            # HEAL CHOICE
            if game_choice == "B":
                # Calls the heal function and lets player know how many points they healed for and their current health
                player.heal()
                print("The player has healed for 50 points!")
                print(f"The player now has {player.get_current_health()} / {player.get_max_health()}.")
                time.sleep(1)
            # ATTACK CHOICE
            elif game_choice == "A":
                # asks the player which mob they want to attack
                choice = int(input("Which enemy would you like to attack? "))
                # checks if the choice is valid and not negative
                if 0 <= choice and choice <= len(enemy_list):
                    # attacks the selected enemy
                    selected_enemy = enemy_list[choice - 1]
                    # checks if the enemy is still alive, and if so, attacks them
                    if selected_enemy.get_health() > 0:
                        player.attack(selected_enemy)
                        time.sleep(1)
                    # lets the player know if the enemy is already dead
                    else:
                        print("This enemy is dead!")
                        time.sleep(1)
                        raise DeadEnemyError
                # negative number or a number too big will throw this error
                else:
                    raise InvalidEnemyChoice
            # QUIT CHOICE
            elif game_choice == "Q":
                # saves the tower to file and quits
                save_to_file()
                break
            # raises error if no valid choice is made (The valid entries are "A", "B", and "Q")
            else:
                raise InvalidGameChoice
            
            print()
            time.sleep(1)

            # ENEMY TURN
            # loops through each enemy on this floor
            for enemy in enemy_list:
                # checks if the enemy is still alive
                if enemy.get_health() > 0:
                    # The cleric will heal every round and will heal any monsters on that floor if they are still alive
                    if enemy.get_combat_class() == "CLERIC":
                        # list comprehension for living monsters
                        list_of_valid_enemies = [mob for mob in enemy_list if mob.get_health() > 0]
                        # randomly chooses a valid monster to heal
                        heal_choice = random.choice(list_of_valid_enemies)
                        # heals the monster
                        enemy.heal(heal_choice)
                        time.sleep(1)
                    # the enemy attacks the player
                    enemy.attack(player)
                    time.sleep(1)
                    # lets the player know their current health every time they get attacked
                    print(f"You have {player.get_current_health()} health points left.")
                    time.sleep(1)
        # If the player is dead, lets them know
        elif player_alive == False:
            print("YOU DIED!")
            # asks them if they want to quit out (When the save is reloaded, the logic in the code will take them straight here)
            quit_choice = input("Quit? (y/n)")
            # if yes, saves to file and exit
            if quit_choice.lower() == "y":
                save_to_file()
                break
            # if no, asks them if they want to retry the floor (with full health) or restart the tower
            elif quit_choice.lower() == "n":
                restart_choice = input("[1] Retry floor or [2] restart? ")

                # RETRY FLOOR
                if restart_choice == "1":
                    # Sets all enemy health back to max
                    for enemy in enemy_list:
                        enemy.set_health(enemy.get_max_health())
                    # sets the player health back to max
                    player.set_current_health(player.get_max_health())
                    # lets user know which floor they are retrying
                    print(f"RETRYING FLOOR {tower[current_floor_index].get_floor_number()}")
                # RESET CHOICE
                elif restart_choice == "2":
                    # resets the player stats back to default
                    player.reset()
                    # creates a brand new tower
                    tower, tower_mob_list, current_floor_index = create_tower()
                # raise error if neither 1 or 2 is entered
                else:
                    raise RestartError
            # raise error if neither y or n is entered
            else:
                raise QuitError
        # If player is still alive and all enemies are dead
        else:
            # lets the user know they beat the floor
            print("All enemies are dead. You Cleared This Floor!")
            time.sleep(1)
            # grants the player experience based on the floor
            if current_floor_index < 10:
                player.gain_experience(tower[current_floor_index].give_xp())
            time.sleep(1)
            # increases the floor number
            current_floor_index = current_floor_index + 1
            # player gets the steel sword before the fifth floor
            if current_floor_index == 4:
                print("You have acquired the steel sword!")
                # equips the steel sword and increases current damage by 1.4
                player.equip("Steel Sword", 1.4)
                time.sleep(1)
            # player gets the dragon slaying sword before floor 10
            if current_floor_index == 9:
                print("You have acquired the dragon slaying sword!")
                # equips the dragon slaying sword and increases current damage by 1.75
                player.equip("Dragon Slaying Sword", 1.75)
                time.sleep(1)
            # Sets max floor to 10
            if current_floor_index < 10:
                # lets the player know what floor they are moving to now
                print("MOVING TO THE NEXT FLOOR!\nFLOOR", current_floor_index + 1)
                time.sleep(1)
            # this will only run on "floor 11", which doesnt exist so tells the player they win
            else:
                print("YOU WIN!!!!!")
                time.sleep(1)
                game_restart = input("Do you want to restart the game? (y/n):").lower()
                if game_restart == "y":
                    # resets the player stats back to default
                    player.reset()
                    # creates a brand new tower
                    tower, tower_mob_list, current_floor_index = create_tower()
                elif game_restart == "n":
                    # saves to file and quit
                    current_floor_index = 10
                    save_to_file()
                    break
                else:
                    raise QuitError
    # ERRORS
    except ValueError: # PLAYER DID NOT PICK A VALID ENEMY (TYPED A STRING)
        print("Please enter a number to attack any of the enemy (e.g., to attack [1] Skeleton, type 1 and press enter).")
        time.sleep(1)
    except InvalidEnemyChoice: # PLAYER DID NOT PICK A VALID ENEMY (TYPED A NEGATIVE NUMBER OR OUT OF BOUNDS NUMBER)
        # player picked a number that is higher than current amount of enemies
        if choice > len(enemy_list):
            print(f"There are only {len(enemy_list)} enemies. Please select one of them.")
            time.sleep(1)
        # player entered a negative number or 0
        elif choice <= 0:
            print("Please enter a positive number.")
            time.sleep(1)
    except InvalidGameChoice: # PLAYER DID NOT PICK A VALID GAME CHOICE (ENTERED ANYTHING OTHER THAN "A", "B", or "Q")
        print("Please enter 'A' or 'B' to either attack the enemy or heal yourself or 'Q' to save and quit.")
        time.sleep(1)
    except DeadEnemyError:
        print("Select a living enemy!")
        time.sleep(1)
    except QuitError: # PLAYER DID NOT ENTER Y OR N
        print("Please enter either 'y' or 'n' in order to quit or restart/retry.")
        time.sleep(1)
    except RestartError: # PLAYER DID NOT ENTER 1 OR 2
        print("Please enter either 1 or 2 to retry the floor or restart the tower.")
    except Exception as e: # ANY OTHER ERRORS I DID NOT CATCH
        print(f"An error occured: {e}")
        time.sleep(1)
        break

