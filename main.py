from enemy import Enemy
from player import Player

player = Player()
enemy_list = [Enemy(type = "Zombie"), Enemy(type = "Skeleton")]

while True:
    try:
        # checks if all enemies are alive or not
        enemies_alive = True
        living_counter = 0
        for enemy in enemy_list:
            if enemy.get_health() > 0:
                living_counter += 1
        if living_counter == 0:
            enemies_alive = False

        if enemies_alive:
            
            # Print out the enemy list
            selection_number = 1
            for enemy in enemy_list:
                print(f"[{selection_number}] {enemy}")
                selection_number += 1
            print()


            attack_or_heal_choice = int(input("[1] Heal | [2] Attack Enemy: "))

            if attack_or_heal_choice == 1:
                player.heal()
            elif attack_or_heal_choice == 2:
                choice = int(input("Which enemy would you like to attack? "))
                selected_enemy = enemy_list[choice - 1]

                if selected_enemy.get_health() > 0:
                    player.attack(selected_enemy)
                else:
                    print("This enemy is dead!")
            else:
                raise ValueError
            print()

        else:
            print("All enemies are dead. You Win!")
            break
    except ValueError:
        print("Please enter 1 or 2 to either heal yourself or attack the enemy.")
    except Exception as e:
        print(f"An error occured: {e}")

