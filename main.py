import random
import pickle

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.health = 100
        self.max_health = 100
        self.attack_power = 20
        self.inventory = {"Health Potion": 3}
        self.gold = 0
        self.house = [[" "] * 5 for _ in range(5)]

    def attack(self):
        return random.randint(1, self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.attack_power += 5

    def show_inventory(self):
        print("\nInventory:")
        for item, quantity in self.inventory.items():
            print(f"{item} x{quantity}")

    def show_house(self):
        print("\nHouse:")
        for row in self.house:
            print(" | ".join(row))

    def save(self):
        with open(f"{self.name}_savefile.pkl", "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(name):
        with open(f"{name}_savefile.pkl", "rb") as file:
            return pickle.load(file)

# Monster class
class Monster:
    def __init__(self, name, health, attack_power, gold):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.gold = gold

    def attack(self):
        return random.randint(1, self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

# Shop class
class Shop:
    def __init__(self):
        self.items = {
            "Health Potion": {"price": 20, "effect": 20},
            "Super Sword": {"price": 50, "effect": 10},
            "Mega Shield": {"price": 40, "effect": 15}
        }

    def show_items(self):
        print("\nShop Items:")
        for item, details in self.items.items():
            print(f"{item}: {details['price']} gold")

    def buy_item(self, player, item_name):
        if item_name in self.items:
            item_details = self.items[item_name]
            item_price = item_details["price"]
            if item_price <= player.gold:
                player.gold -= item_price
                player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
                print(f"\nYou purchased {item_name} for {item_price} gold.")
            else:
                print("You don't have enough gold to buy that item.")
        else:
            print("Invalid item.")

# Game logic
def game():
    print("Welcome to the Adventure Game!")
    player_name = input("Enter your name: ")
    try:
        player = Player.load(player_name)
        print(f"Welcome back, {player.name}!")
    except FileNotFoundError:
        player = Player(player_name)
        print(f"Welcome, {player.name}!")

    shop = Shop()

    while True:
        print("\n[1] Fight monsters")
        print("[2] Visit hub")
        print("[3] Save and Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nYou are now in the monster arena!")
            while True:
                monster_name = random.choice(["Goblin", "Orc", "Troll", "Dragon"])
                monster_health = random.randint(50, 100)
                monster_attack = random.randint(10, 20)
                monster_gold = random.randint(5, 15)
                monster = Monster(monster_name, monster_health, monster_attack, monster_gold)

                print(f"\nA wild {monster.name} appears!\n")

                while True:
                    print(f"{player.name} (Level {player.level}) HP: {player.health}/{player.max_health}")
                    print(f"{monster.name} HP: {monster.health}")
                    print(f"Gold: {player.gold}\n")

                    action = input("What do you want to do? [1] Attack, [2] Heal, [3] Use Item, [4] Run: ")

                    if action == "1":
                        player_damage = player.attack()
                        monster.take_damage(player_damage)
                        print(f"\nYou attack the {monster.name} for {player_damage} damage!")

                        if monster.health <= 0:
                            print(f"\nYou defeated the {monster.name}!")
                            player.level_up()
                            player.gold += monster.gold
                            loot = random.choice(["Table", "Chair", "Painting", "Rug"])
                            player.house[random.randint(0, 4)][random.randint(0, 4)] = loot
                            print(f"You gained a {loot} as loot!")
                            break

                        monster_damage = monster.attack()
                        player.take_damage(monster_damage)
                        print(f"The {monster.name} attacks you for {monster_damage} damage!")

                        if player.health <= 0:
                            print("You were defeated. Game over!")
                            player.save()
                            return

                    elif action == "2":
                        player.heal(20)
                        print("\nYou heal yourself for 20 HP.")

                        monster_damage = monster.attack()
                        player.take_damage(monster_damage)
                        print(f"The {monster.name} attacks you for {monster_damage} damage!")

                        if player.health <= 0:
                            print("You were defeated. Game over!")
                            player.save()
                            return

                    elif action == "3":
                        player.show_inventory()
                        item_name = input("Enter the item name to use (or 'q' to go back): ")
                        if item_name.lower() == "q":
                            continue
                        if item_name in player.inventory:
                            if item_name == "Health Potion":
                                player.heal(20)
                                print("\nYou used a Health Potion and healed yourself for 20 HP.")
                                player.inventory[item_name] -= 1
                                if player.inventory[item_name] == 0:
                                    del player.inventory[item_name]
                            else:
                                print("You can't use that item in battle.")
                        else:
                            print("Invalid item.")

                        monster_damage = monster.attack()
                        player.take_damage(monster_damage)
                        print(f"The {monster.name} attacks you for {monster_damage} damage!")

                        if player.health <= 0:
                            print("You were defeated. Game over!")
                            player.save()
                            return

                    elif action == "4":
                        print(f"You ran away from the {monster.name}.")
                        break

                    else:
                        print("Invalid action. Please try again.")

                if player.health <= 0:
                    break

                choice = input("\nDo you want to keep fighting? [Y/N]: ")
                if choice.lower() == "n":
                    break

        elif choice == "2":
            while True:
                print("\nWelcome to the hub!")
                print("[1] Check inventory")
                print("[2] Visit shop")
                print("[3] Visit home")
                print("[4] Return to fighting")
                hub_choice = input("Enter your choice: ")

                if hub_choice == "1":
                    player.show_inventory()

                elif hub_choice == "2":
                    shop.show_items()
                    item_name = input("Enter the item name to buy (or 'q' to go back): ")
                    if item_name.lower() == "q":
                        continue
                    shop.buy_item(player, item_name)

                elif hub_choice == "3":
                    player.show_house()

                elif hub_choice == "4":
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            player.save()
            print("Game saved. Thank you for playing!")
            return

        else:
            print("Invalid choice. Please try again.")

game()
