from classes.game import Person, bColors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create black magic
fire = Spell("Fire", 25, 600, "Black")
thunder = Spell("Thunder", 25, 600, "Black")
blizzard = Spell("Thunder", 25, 600, "Black")
meteor = Spell("Meteor", 40, 1200, "Black")
quake = Spell("Quake", 14, 140, "Black")

# Create white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Create some Items
poition = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
granade = Item("Granade", "attack", "Deals 500 dmg", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": poition, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": granade, "quantity": 5}]

# Instantiate Players
player1 = Person("Eduardo :", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Esteban :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot   :", 3089, 174, 288, 34, player_spells, player_items)

# Instantiate enemies
enemy3 = Person("Enemy3  :", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = Person("Enemy1  :", 18200, 65, 45, 25, enemy_spells, [])
enemy2 = Person("Enemy2  :", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bColors.FAIL + bColors.BOLD + "AN ENEMY ATTACKS!" + bColors.ENDC)

while running:
    print("=============================")
    print("NAME                   HP                                        MP          ")
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()
    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attack "+enemies[enemy].name.replace(" ", "")+" for", dmg, "points of damage to " + enemies[enemy].name.replace(" ", ""))
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + "has died")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic:")) - 1
            if magic_choice == -1:
                continue
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bColors.FAIL + "\nNot enough MP\n" + bColors.ENDC)
                continue
            player.reduce_mp(spell.cost)
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bColors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP" + bColors.ENDC)
            elif spell.type == "Black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bColors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to "+enemies[enemy].name.replace(" ", "")+ bColors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died")
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player_items[item_choice]["quantity"] == 0:
                print(bColors.FAIL + "\n" + "None left..." + bColors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bColors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP", bColors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bColors.OKGREEN + "\n" + item.name + " fully restores HP & MP " + bColors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bColors.FAIL + "\n" + item.name + " deals ", str(item.prop), "points of damage" + bColors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died")
                    del enemies[enemy]
    # Check if the battle is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    # Check if players won
    if defeated_enemies == 2:
        print(bColors.OKGREEN + "You win!" + bColors.ENDC)
        running = False
    # Check if enemies won
    elif defeated_players == 2:
        print(bColors.FAIL + "Your enemies have defeated you!" + bColors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        # Choose attack
        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            target = random.randrange(0, 2)
            players[target].take_damage(enemy_dmg)
            print(bColors.WARNING + enemy.name.replace(" ", "") + " attacks "+player.name.replace(" ", "")+"for", enemy_dmg, bColors.ENDC)
            print("----------------------------")
        # Choose magic
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            print(enemy.name+" chose ", spell, " for ", magic_dmg)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bColors.OKBLUE + "\n" + spell.name + "heals "+enemy.name+" for", str(magic_dmg), "HP" + bColors.ENDC)
            elif spell.type == "Black":
                target = random.randrange(0, 2)
                players[target].take_damage(magic_dmg)
                print(bColors.OKBLUE + "\n"+enemy.name.replace(" ", "")+"'s " + spell.name + " deals", str(magic_dmg), "points of damage to "+players[target].name.replace(" ", "")+ bColors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + "has died")
                    del players[target]
