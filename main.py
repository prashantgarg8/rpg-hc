import random
import time
import os
from typing import List, Dict

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:

    class Dummy:

        def __getattr__(self, x):
            return ""

    Fore = Dummy()
    Style = Dummy()

logo = rf"""
{Fore.CYAN}
 _    _            _     _____ _       _     _             
| |  | |          | |   /  __ \ |     | |   | |            
| |__| | __ _  ___| | _ | /  \/ | ___ | |__ | |__   ___ _ __ 
|  __  |/ _` |/ __| |/ / | |   | |/ _ \| '_ \| '_ \ / _ \ '__|
| |  | | (_| | (__|   <  | \__/\ | (_) | |_) | |_) |  __/ |   
|_|  |_|\__,_|\___|_|\_\  \____/_|\___/|_.__/|_.__/ \___|_|   
{Style.RESET_ALL}
"""


class Player:

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.lvlupcp = 50
        self.hp = self.max_hp = role['hp']
        self.attack = list(role['attack'])
        self.coins = 0
        self.inventory = []
        self.tools = role['tools'][:]
        self.skills = []
        self.achivesments = set()
        self.location = "Coworking Space"
        self.rests_left = 3

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.lvlupcp:
            self.exp -= self.lvlupcp
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack[0] += 2
            self.attack[1] += 2
            self.lvlupcp = int(self.lvlupcp * 1.4)
            print(
                f"{Fore.YELLOW}Whoa! You hit level {self.level}. Time to flex!{Style.RESET_ALL}"
            )
            self.unlock_skill()

    def unlock_skill(self):
        skill_options = ["Debug Surge", "Stack Overflow", "Pizza Heal"]
        for s in skill_options:
            if s not in self.skills:
                self.skills.append(s)
                print(f"{Fore.MAGENTA}Unlocked skill: {s}!{Style.RESET_ALL}")
                break

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(
            f"{Fore.GREEN}Healed for {amount}! HP is now {self.hp}/{self.max_hp}.{Style.RESET_ALL}"
        )


class Enemy:

    def __init__(self, info: Dict):
        self.name = info['name']
        self.max_hp = self.hp = info['hp']
        self.attack = list(info['attack'])
        self.exp = info['exp']
        self.coins = info.get('coins', random.randint(10, 25))
        self.is_boss = info.get('is_boss', False)

    def decide_move(self, player):
        return 'attack'


dev_roles = {
    'Frontend Dev': {
        'hp': 95,
        'attack': (7, 17),
        "tools": ["Laptop", "Wi-Fi", "CSS Flexbox"]
    },
    'Backend Dev': {
        'hp': 110,
        'attack': (9, 19),
        "tools": ["Laptop", "APIs", "SQL"]
    },
    'Fullstack': {
        'hp': 100,
        'attack': (8, 18),
        "tools": ["Laptop", "Git", "Debug Goggles"]
    },
    'Hardware Hacker': {
        'hp': 105,
        'attack': (6, 21),
        "tools": ["Soldering Iron", "Breadboard"]
    }
}


def choose_class() -> Dict:
    print("\nChoose your class:")
    for i, (cls, stats) in enumerate(catagories.items(), 1):
        print(
            f"{i}) {cls} - HP: {stats['hp']} | ATK: {stats['attack']} | Tools: {', '.join(stats['tools'])}"
        )
    while True:
        choice = input("> ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(catagories):
                return list(catagories.values())[idx - 1]
        except:
            pass
        print("Invalid. Enter a number to pick your class.")


ENEMY_TEMPLATES = [{
    "name": "Segmentation Fault",
    "hp": 45,
    "attack": (8, 15),
    "exp": 12
}, {
    "name": "Merge Conflict",
    "hp": 55,
    "attack": (12, 22),
    "exp": 18
}, {
    "name": "JavaScript Bug",
    "hp": 65,
    "attack": (13, 23),
    "exp": 24
}, {
    "name": "Stack Overflow Demon",
    "hp": 80,
    "attack": (16, 25),
    "exp": 31
}, {
    "name": "Null Pointer Ninja",
    "hp": 90,
    "attack": (19, 29),
    "exp": 42
}, {
    "name": "Regex Goblin",
    "hp": 100,
    "attack": (17, 32),
    "exp": 55
}, {
    "name": "Legacy Code Dragon",
    "hp": 160,
    "attack": (22, 38),
    "exp": 100,
    "is_boss": True,
    "coins": 90
}]


def make_enemy(level):
    if level % 5 == 0:
        return Enemy([e for e in ENEMY_TEMPLATES if e.get("is_boss")][0])
    options = [e for e in ENEMY_TEMPLATES if not e.get("is_boss")]
    template = random.choice(options)
    scale = 1 + 0.08 * (level - 1)
    info = template.copy()
    info['hp'] = int(info['hp'] * scale)
    info['attack'] = (int(info['attack'][0] * scale),
                      int(info['attack'][1] * scale))
    info['exp'] = int(info['exp'] * scale)
    info['coins'] = int(template.get('coins', random.randint(10, 25)) * scale)
    return Enemy(info)


def attack(attacker, defender):
    dmg = random.randint(*attacker.attack)
    crit = random.random() < 0.10
    if crit:
        dmg = int(dmg * 1.5)
        print(
            f"{Fore.YELLOW}{attacker.name} lands a CRITICAL hit!{Style.RESET_ALL}"
        )
    defender.hp = max(0, defender.hp - dmg)
    print(
        f"{attacker.name} hits {defender.name} for {dmg} damage! ({defender.hp}/{defender.max_hp} HP left)"
    )


def fights(player: Player):
    enemy = make_enemy(player.level)
    print(f"\n {enemy.name} jumps out at you! (HP: {enemy.hp})")
    if enemy.is_boss:
        print(f"{Fore.RED}BOSS FIGHT! This won't be easy...{Style.RESET_ALL}")
    while enemy.hp > 0 and player.hp > 0:
        print(
            f"\n{Fore.CYAN}Your HP: {player.hp}/{player.max_hp} | {enemy.name}'s HP: {enemy.hp}/{enemy.max_hp}{Style.RESET_ALL}"
        )
        print("1) Attack   2) Use Item   3) Skill   4) Attempt Escape")
        move = input("> ").strip()
        if move == "1":
            attack(player, enemy)
        elif move == "2":
            print("Your inventory:", ", ".join([i for i in player.inventory])
                  or "Empty")
            continue
        elif move == "3":
            print("Skills:", ", ".join(player.skills) or "None yet.")
            continue
        elif move == "4":
            if enemy.is_boss:
                print(
                    f"{Fore.RED}You can't escape a boss fight!{Style.RESET_ALL}"
                )
            elif random.random() < 0.3:
                print(
                    f"{Fore.GREEN}You slipped away safely...{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Couldn't escape!{Style.RESET_ALL}")
        else:
            print("Choose a valid move.")
            continue
        if enemy.hp > 0:
            if enemy.decide_move(player) == "attack":
                attack(enemy, player)
    if player.hp <= 0:
        print(
            f"{Fore.LIGHTRED_EX}\nYou burned out. Start hydrating and coding again soon!{Style.RESET_ALL}"
        )
        return False
    print(
        f"{Fore.GREEN} You debugged {enemy.name}! +{enemy.exp} EXP, +{enemy.coins} coins!{Style.RESET_ALL}"
    )
    player.gain_exp(enemy.exp)
    player.coins += enemy.coins
    return True


def mmenu(player: Player):
    while True:
        print("\n--- Main Menu ---")
        print("1) Take On a Challenge")
        print("2) View Stats")
        print("3) Rest (Restore Energy)")
        print("4) Quit")
        choice = input("> ").strip()
        if choice == "1":
            success = fights(player)
            if not success:
                break
        elif choice == "2":
            print(f"\nName: {player.name}")
            print(
                f" Class: {list(catagories.keys())[list(catagories.values()).index(player.role)]}"
            )
            print(f" HP: {player.hp}/{player.max_hp}")
            print(f" Attack Power: {player.attack}")
            print(f" Level: {player.level}")
            print(f" EXP: {player.exp}/{player.lvlupcp}")
            print(f" Coins: {player.coins}")
            print(f" Tools: {', '.join(player.tools)}")
            print(f" Inventory: {', '.join(player.inventory) or 'Empty'}")
            print(f" Skills: {', '.join(player.skills) or 'None yet.'}")
        elif choice == "3":
            if player.rests_left > 0:
                player.heal(player.max_hp)
                player.rests_left -= 1
                print(
                    f"{Fore.BLUE}You feel refreshed! Rest uses left: {player.rests_left}{Style.RESET_ALL}"
                )
            else:
                print(
                    f"{Fore.RED}No rests left—push through!{Style.RESET_ALL}")
        elif choice == "4":
            print(
                f"{Fore.CYAN}Thanks for playing Hack Clubber RPG!{Style.RESET_ALL}"
            )
            break
        else:
            print("?? Invalid choice.")


def start():
    print(logo)
    print("Welcome to Hack Clubber RPG!\n")
    name = input("Your Hack Club name: ").strip() or "Hack Clubber"
    pclass = choose_class()
    player = Player(name, pclass)
    mmenu(player)


ITEMS = {
    "Coffee": {
        "type": "heal",
        "power": 40,
        "cost": 15,
        "desc": "Restores 40HP instantly."
    },
    "Energy Drink": {
        "type": "heal",
        "power": 80,
        "cost": 32,
        "desc": "Restores 80HP but stuns next turn."
    },
    "Debug Kit": {
        "type": "buff",
        "power": 6,
        "duration": 3,
        "cost": 30,
        "desc": "Boost ATK by 6 for 3 turns."
    },
    "Rubber Duck": {
        "type": "special",
        "cost": 25,
        "desc": "Resets one enemy action."
    },
    "Snack Bar": {
        "type": "heal",
        "power": 20,
        "cost": 8,
        "desc": "Minor HP recovery."
    },
}


def shop(player):
    print(f"\n{Fore.LIGHTYELLOW_EX}== Code Supply Shop =={Style.RESET_ALL}")
    while True:
        print("Coins:", player.coins)
        for i, (iname, data) in enumerate(ITEMS.items(), 1):
            print(f"{i}. {iname} ({data['cost']}g): {data.get('desc','')}")
        print("X. Leave Shop")
        choice = input("Buy what? > ").strip().upper()
        if choice == "X":
            break
        try:
            idx = int(choice)
            if 1 <= idx <= len(ITEMS):
                item = list(ITEMS.keys())[idx - 1]
                if player.coins >= ITEMS[item]['cost']:
                    player.coins -= ITEMS[item]['cost']
                    player.inventory.append(item)
                    print(f"{Fore.GREEN}Purchased {item}!{Style.RESET_ALL}")
                else:
                    print("Not enough coins.")
            else:
                print("Pick a valid item number.")
        except ValueError:
            print("Enter item number or X.")


def use_item(player, in_fights=False, target=None):
    if not player.inventory:
        print("Inventory empty!")
        return False
    print("Inventory:", ", ".join(player.inventory))
    item = input("Use what? ").strip()
    if item not in player.inventory:
        print("Not in inventory.")
        return False

    info = ITEMS.get(item)
    if not info:
        print("Unknown item.")
        return False
    if info["type"] == "heal":
        player.heal(info["power"])
    elif info["type"] == "buff":
        if in_fights and target:
            target.attack[0] += info["power"]
            target.attack[1] += info["power"]
            print(
                f"Attack power increased by {info['power']} for {info['duration']} turns!"
            )
            target.buff_turns = info['duration']
        else:
            print("Can only use in fights!")
    elif info["type"] == "special":
        if in_fights and target:
            target.skipped_turn = True
            print("The enemy looks confused... turn skipped!")
        else:
            print("Can only use in fights!")

    player.inventory.remove(item)
    return True


location = [
    "Coworking Space", "Hackathon", "Basement Lab", "Rooftop Garden",
    "Mars Hacker Colony"
]
levntS = {
    "Hackathon": [
        "A free pizza break! Restore 30HP.", "Win mini-hack: gain 25 coins.",
        "Lose in bug bash: -10 hp."
    ],
    "Basement Lab": [
        "Find a mysterious old gadget (get Debug Kit).",
        "Trip over loose cable: -5 hp.", "Find snack bar under the desk."
    ],
    "Rooftop Garden": [
        "Breathe in fresh air: +10 hp.", "Meet a wise mentor: +25 exp.",
        "Laptop battery dies: must rest."
    ],
    "Mars Hacker Colony": [
        "Low gravity helps focus, +10 atk for next challenge.",
        "Solar flare! Lose a rest.", "Martian finds your bug: gain rare item."
    ]
}


def travel(player):
    print("\nlocation:")
    for i, loc in enumerate(location, 1):
        print(f"{i}) {loc}")
    print("X) Stay put")
    choice = input("Go where? > ").strip().upper()
    if choice == "X":
        return
    try:
        idx = int(choice)
        if 1 <= idx <= len(location):
            new_loc = location[idx - 1]
            player.location = new_loc
            rand_event(player, new_loc)
        else:
            print("Invalid location.")
    except ValueError:
        print("Type number or X.")


def rand_event(player, location):
    if location in levntS and random.random() < 0.6:
        event = random.choice(levntS[location])
        print(f"{Fore.LIGHTMAGENTA_EX}Event: {event}{Style.RESET_ALL}")
        if "Restore" in event:
            hp = int([s for s in event.split() if s.isdigit()][0])
            player.heal(hp)
        elif "gain" in event and "coin" in event:
            coins = int([s for s in event.split() if s.isdigit()][0])
            player.coins += coins
            print(f"Gained {coins} coins!")
        elif "-hp" in event or "-" in event:
            dmg = int([
                s for s in event.replace("-", " -").split()
                if s.lstrip("-").isdigit()
            ][0])
            player.hp = max(0, player.hp + dmg)
            print(f"Ouch! HP now {player.hp}")
        elif "exp" in event:
            exp = int([s for s in event.split() if s.isdigit()][0])
            player.gain_exp(exp)
        elif "Debug Kit" in event:
            player.inventory.append("Debug Kit")
            print("Found a Debug Kit!")
        elif "snack bar" in event:
            player.inventory.append("Snack Bar")
            print("Yum! Got a Snack Bar.")
        elif "rare item" in event:
            player.inventory.append("Rubber Duck")
            print("You got... a Rubber Duck?!")


achivesments = [("First Challenge", "Win your first fights."),
                ("Coffee Overdose", "Use 5 Coffee items in one run."),
                ("Mars Adventure", "Travel to Mars Hacker Colony."),
                ("Boss Buster", "Defeat a boss."),
                ("Overachiever", "Reach level 5.")]


def check_achivesments(player, context=None):
    unlocked = set(player.achivesments)
    if player.level >= 5:
        unlocked.add("Overachiever")
    if player.location == "Mars Hacker Colony":
        unlocked.add("Mars Adventure")
    if any(item == "Coffee" for item in
           player.inventory) and player.inventory.count("Coffee") >= 5:
        unlocked.add("Coffee Overdose")
    if context == "win_fights" and player.level == 1:
        unlocked.add("First Challenge")
    if context == "boss" and player.level >= 2:
        unlocked.add("Boss Buster")
    for ach, _ in achivesments:
        if ach in unlocked and ach not in player.achivesments:
            print(
                f"{Fore.YELLOW}Achievement unlocked: {ach}!{Style.RESET_ALL}")
            player.achivesments.add(ach)


def achivess_show(player):
    print("\nachivesments unlocked:")
    for ach, desc in achivesments:
        got = ach in player.achivesments
        mark = "[X]" if got else "[ ]"
        print(f"{mark} {ach}: {desc}")


def fights(player: Player):
    enemy = make_enemy(player.level)
    print(f"\n {enemy.name} appears! (HP: {enemy.hp})")
    if enemy.is_boss:
        print(f"{Fore.RED}BOSS FIGHT!{Style.RESET_ALL}")

    buff = 0

    while enemy.hp > 0 and player.hp > 0:
        print(
            f"\n{Fore.CYAN}Your HP: {player.hp}/{player.max_hp} | {enemy.name}'s HP: {enemy.hp}/{enemy.max_hp}{Style.RESET_ALL}"
        )

        print("1) Attack   2) Use Item   3) Skill   4) Attempt Escape")
        move = input("> ").strip()
        if move == "1":
            attack(player, enemy)
        elif move == "2":
            use_item(player, in_fights=True, target=player)
            continue
        elif move == "3":
            if player.skills:
                print("Skills:", ", ".join(player.skills))
                print("Not implemented yet (coming soon!)")
            else:
                print("You have no skills yet.")
            continue
        elif move == "4":
            if enemy.is_boss:
                print(f"{Fore.RED}Can't escape this time!{Style.RESET_ALL}")
            elif random.random() < 0.25:
                print(
                    f"{Fore.GREEN}You slipped away successfully!{Style.RESET_ALL}"
                )
                return True
            else:
                print(f"{Fore.RED}Couldn't escape!{Style.RESET_ALL}")
        else:
            print("Choose a valid move.")
            continue

        if enemy.hp > 0:
            en_move = random.choices(population=["attack", "heal", "special"],
                                     weights=[0.7, 0.15, 0.15],
                                     k=1)[0]
            if en_move == "attack":
                attack(enemy, player)
            elif en_move == "heal":
                heal_amt = min(25, enemy.max_hp - enemy.hp)
                enemy.hp += heal_amt
                print(
                    f"{Fore.BLUE}{enemy.name} repairs itself for {heal_amt}!{Style.RESET_ALL}"
                )

            else:
                if random.random() < 0.5:
                    print(
                        f"{enemy.name} tries to confuse your code! Lose your next attack turn."
                    )
                else:
                    print(f"{enemy.name} lags—no effect this turn.")

            if hasattr(player, 'buff_turns') and player.buff_turns > 0:
                player.buff_turns -= 1
                if player.buff_turns == 0:
                    player.attack[0] -= 6
                    player.attack[1] -= 6
                    print("Your debug buff faded.")

    if player.hp <= 0:
        print(f"{Fore.LIGHTRED_EX}\nYou burned out...{Style.RESET_ALL}")
        return False
    print(
        f"{Fore.GREEN} Debugged {enemy.name}! +{enemy.exp} EXP, +{enemy.coins} coins!{Style.RESET_ALL}"
    )

    player.gain_exp(enemy.exp)
    player.coins += enemy.coins
    check_achivesments(player,
                       context="boss" if enemy.is_boss else "win_fights")
    return True


def mmenu(player: Player):
    while True:
        print("\n--- Main Menu ---")
        print("1) Take On a Challenge")
        print("2) View Stats")
        print("3) Rest (Restore Energy)")
        print("4) Shop")
        print("5) Travel")
        print("6) achivesments")
        print("7) Quit")
        choice = input("> ").strip()
        if choice == "1":
            success = fights(player)
            if not success:
                break
        elif choice == "2":
            print(f"\n Name: {player.name}")
            print(f" Class: {player.role}")
            print(f" HP: {player.hp}/{player.max_hp}")
            print(f" Attack Power: {player.attack}")
            print(f" Level: {player.level}")
            print(f" EXP: {player.exp}/{player.lvlupcp}")
            print(f" Coins: {player.coins}")
            print(f" Tools: {', '.join(player.tools)}")
            print(f" Inventory: {', '.join(player.inventory) or 'Empty'}")

            print(f" Skills: {', '.join(player.skills) or 'None yet.'}")
        elif choice == "3":
            if player.rests_left > 0:
                player.heal(player.max_hp)
                player.rests_left -= 1
                print(
                    f"{Fore.BLUE}You feel refreshed! Rests left: {player.rests_left}{Style.RESET_ALL}"
                )
                rand_event(player, player.location)
            else:
                print(f"{Fore.RED}No rests left!{Style.RESET_ALL}")
        elif choice == "4":
            shop(player)
        elif choice == "5":
            travel(player)
        elif choice == "6":
            achivess_show(player)
        elif choice == "7":
            print(
                f"{Fore.CYAN} Thanks for playing Hack Clubber RPG!{Style.RESET_ALL}"
            )
            break
        else:

            print("?? Invalid choice.")


if __name__ == "__main__":

    start()
