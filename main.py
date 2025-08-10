import random
import time
import os

hello = "hey"

logo = """

 _   _            _     ____ _       _     _               
| | | | __ _  ___| | __/ ___| |_   _| |__ | |__   ___ _ __ 
| |_| |/ _` |/ __| |/ / |   | | | | | '_ \| '_ \ / _ \ '__|
|  _  | (_| | (__|   <| |___| | |_| | |_) | |_) |  __/ |   
|_| |_|\__,_|\___|_|\_\\____|_|\__,_|_.__/|_.__/ \___|_|   

"""


class Player:

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.lvlupcp = 50
        self.max_hp = role['hp']
        self.hp = self.max_hp
        self.attack = list(role['attack'])
        self.coins = 0
        self.inventory = []
        self.tools = role['tools'][:]
        self.skills = []
        self.achivesments = set()
        self.location = "Coworking Space"
        self.rests_left = 3
        # messy flag
        self.buff_turns = 0

    def gain_exp(self, amount):
        self.exp = self.exp + amount
        # levelling loop
        while self.exp >= self.lvlupcp:
            self.exp = self.exp - self.lvlupcp
            self.level = self.level + 1
            self.max_hp = self.max_hp + 20
            self.hp = self.max_hp
            # increase both attack bounds
            self.attack[0] = self.attack[0] + 2
            self.attack[1] = self.attack[1] + 2
            self.lvlupcp = int(self.lvlupcp * 1.4)
            print("Whoa! You hit level " + str(self.level) + ". Time to flex!")
            self.unlock_skill()

    def unlock_skill(self):
        opts = ["Debug Surge", "Stack Overflow", "Pizza Heal"]
        for s in opts:
            if s not in self.skills:
                self.skills.append(s)
                print("Unlocked skill: " + s + "!")
                break

    def heal(self, amount):
        self.hp = self.hp + amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print("Healed for " + str(amount) + "! HP is now " + str(self.hp) +
              "/" + str(self.max_hp) + ".")


class Enemy:

    def __init__(self, info):
        self.name = info['name']
        self.max_hp = info['hp']
        self.hp = info['hp']
        self.attack = list(info['attack'])
        self.exp = info['exp']
        # coins sometimes passed else random
        if 'coins' in info:
            self.coins = info['coins']
        else:
            self.coins = random.randint(10, 25)
        self.is_boss = info.get('is_boss', False)
        self.skipped_turn = False
        self.buff_turns = 0

    def decide_move(self, player):
        # simple ai for enemy, beginner style
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


def choose_class():
    print("")
    print("Choose your class:")
    i = 1
    keys = list(dev_roles.keys())
    for k in keys:
        stats = dev_roles[k]
        print(
            str(i) + ") " + k + " - HP: " + str(stats['hp']) + " | ATK: " +
            str(stats['attack']) + " | Tools: " + ", ".join(stats['tools']))
        i = i + 1
    while True:
        choice = input("> ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(keys):
                # return the role dict
                return dev_roles[keys[idx - 1]]
        except:
            pass
        print("Invalid. Enter a number to pick your class.")


dusmans = [{
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
    # if boss level
    if level % 5 == 0:
        for e in dusmans:
            if e.get("is_boss"):
                return Enemy(e.copy())
    options = [e for e in dusmans if not e.get("is_boss")]
    template = random.choice(options)
    scale = 1 + 0.08 * (level - 1)
    info = template.copy()
    info['hp'] = int(info['hp'] * scale)
    info['attack'] = (int(info['attack'][0] * scale),
                      int(info['attack'][1] * scale))
    info['exp'] = int(info['exp'] * scale)
    info['coins'] = int(template.get('coins', random.randint(10, 25)) * scale)
    return Enemy(info)


def attack(a, d):
    # a attacker, d defender
    dmg = random.randint(a.attack[0], a.attack[1])
    crit = random.random() < 0.10
    if crit:
        dmg = int(dmg * 1.5)
        print(a.name + " lands a CRITICAL hit!")
    d.hp = d.hp - dmg
    if d.hp < 0:
        d.hp = 0
    print(a.name + " hits " + d.name + " for " + str(dmg) + " damage! (" +
          str(d.hp) + "/" + str(d.max_hp) + " HP left)")


items = {
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
    }
}


def shop(player):
    print("")
    print("== Code Supply Shop ==")
    while True:
        print("Coins: " + str(player.coins))
        j = 1
        keys = list(items.keys())
        for name in keys:
            data = items[name]
            print(
                str(j) + ". " + name + " (" + str(data['cost']) + "g): " +
                data.get('desc', ''))
            j = j + 1
        print("X. Leave Shop")
        choice = input("Buy what? > ").strip().upper()
        if choice == "X":
            break
        try:
            idx = int(choice)
            if 1 <= idx <= len(keys):
                item = keys[idx - 1]
                if player.coins >= items[item]['cost']:
                    player.coins = player.coins - items[item]['cost']
                    player.inventory.append(item)
                    print("Purchased " + item + "!")
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
    print("Inventory: " + ", ".join(player.inventory))
    item = input("Use what? ").strip()
    if item not in player.inventory:
        print("Not in inventory.")
        return False
    info = items.get(item)
    if not info:
        print("Unknown item.")
        return False
    t = info["type"]
    if t == "heal":
        player.heal(info["power"])
    elif t == "buff":
        if in_fights and target:
            target.attack[0] = target.attack[0] + info["power"]
            target.attack[1] = target.attack[1] + info["power"]
            target.buff_turns = info['duration']
            print("Attack power increased by " + str(info['power']) + " for " +
                  str(info['duration']) + " turns!")
        else:
            print("Can only use in fights!")
    elif t == "special":
        if in_fights and target:
            target.skipped_turn = True
            print("The enemy looks confused... turn skipped!")
        else:
            print("Can only use in fights!")
    # remove item
    try:
        player.inventory.remove(item)
    except:
        pass
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


def rand_event(player, locationn):
    if locationn in levntS and random.random() < 0.6:
        event = random.choice(levntS[locationn])
        print("Event: " + event)
        if "Restore" in event or "Restore" in event:
            # get number from string
            nums = [int(s) for s in event.split() if s.isdigit()]
            if nums:
                hp = nums[0]
                player.heal(hp)
        elif "gain" in event and "coin" in event:
            nums = [int(s) for s in event.split() if s.isdigit()]
            if nums:
                coins = nums[0]
                player.coins = player.coins + coins
                print("Gained " + str(coins) + " coins!")
        elif "-" in event:
            # crude negative parse
            parts = event.replace("-", " -").split()
            nums = [int(s) for s in parts if s.lstrip("-").isdigit()]
            if nums:
                dmg = nums[0]
                player.hp = player.hp + dmg
                if player.hp < 0:
                    player.hp = 0
                print("Ouch! HP now " + str(player.hp))
        elif "exp" in event:
            nums = [int(s) for s in event.split() if s.isdigit()]
            if nums:
                exp = nums[0]
                player.gain_exp(exp)
        elif "Debug Kit" in event:
            player.inventory.append("Debug Kit")
            print("Found a Debug Kit!")
        elif "snack" in event or "Snack" in event:
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
            print("Achievement unlocked: " + ach + "!")
            player.achivesments.add(ach)


def achivess_show(player):
    print("")
    print("achivesments unlocked:")
    for ach, desc in achivesments:
        got = ach in player.achivesments
        mark = "[X]" if got else "[ ]"
        print(mark + " " + ach + ": " + desc)


def fights(player):
    enemy = make_enemy(player.level)
    print("")
    print(" " + enemy.name + " appears! (HP: " + str(enemy.hp) + ")")
    if enemy.is_boss:
        print("BOSS FIGHT!")

    buff = 0
    while enemy.hp > 0 and player.hp > 0:
        print("")
        print("Your HP: " + str(player.hp) + "/" + str(player.max_hp) + " | " +
              enemy.name + "'s HP: " + str(enemy.hp) + "/" + str(enemy.max_hp))
        print("1) Attack   2) Use Item   3) Skill   4) Attempt Escape")
        move = input("> ").strip()
        if move == "1":
            attack(player, enemy)
        elif move == "2":
            use_item(player, in_fights=True, target=enemy if False else player)

        elif move == "3":
            if player.skills:
                print("Skills: " + ", ".join(player.skills))
                print("Not implemented yet (coming soon!)")
            else:
                print("You have no skills yet.")
            continue
        elif move == "4":
            if enemy.is_boss:
                print("Can't escape this time!")
            elif random.random() < 0.25:
                print("You slipped away successfully!")
                return True
            else:
                print("Couldn't escape!")
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
                enemy.hp = enemy.hp + heal_amt
                print(enemy.name + " repairs itself for " + str(heal_amt) +
                      "!")
            else:
                if random.random() < 0.5:
                    print(
                        enemy.name +
                        " tries to confuse your code! Lose your next attack turn."
                    )
                    # set a flag but we do not enforce strictly, just print to keep behaviour similar
                    enemy.skipped_turn = True
                else:
                    print(enemy.name + " lags—no effect this turn.")

            # handle buff turns on player (from using Debug Kit)
            if hasattr(player, 'buff_turns') and player.buff_turns > 0:
                player.buff_turns = player.buff_turns - 1
                if player.buff_turns == 0:
                    player.attack[0] = player.attack[0] - 6
                    player.attack[1] = player.attack[1] - 6
                    print("Your debug buff faded.")

    if player.hp <= 0:
        print("")
        print("You burned out...")
        return False

    print("")
    print(" Debugged " + enemy.name + "! +" + str(enemy.exp) + " EXP, +" +
          str(enemy.coins) + " coins!")
    player.gain_exp(enemy.exp)
    player.coins = player.coins + enemy.coins
    check_achivesments(player,
                       context="boss" if enemy.is_boss else "win_fights")
    return True


def travel(player):
    print("")
    print("location:")
    i = 1
    for loc in location:
        print(str(i) + ") " + loc)
        i = i + 1
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


def mmenu(player):
    while True:
        print("")
        print("--- Main Menu ---")
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
            print("")
            print(" Name: " + player.name)
            print(" Class: " + str(player.role))
            print(" HP: " + str(player.hp) + "/" + str(player.max_hp))
            print(" Attack Power: " + str(player.attack))
            print(" Level: " + str(player.level))
            print(" EXP: " + str(player.exp) + "/" + str(player.lvlupcp))
            print(" Coins: " + str(player.coins))
            print(" Tools: " + ", ".join(player.tools))
            print(" Inventory: " + (", ".join(player.inventory) or "Empty"))
            print(" Skills: " + (", ".join(player.skills) or "None yet."))
        elif choice == "3":
            if player.rests_left > 0:
                player.heal(player.max_hp)
                player.rests_left = player.rests_left - 1
                print("You feel refreshed! Rests left: " +
                      str(player.rests_left))
                rand_event(player, player.location)
            else:
                print("No rests left!")
        elif choice == "4":
            shop(player)
        elif choice == "5":
            travel(player)
        elif choice == "6":
            achivess_show(player)
        elif choice == "7":
            print(" Thanks for playing Hack Clubber RPG!")
            break
        else:
            print("?? Invalid choice.")


def start():
    print(logo)
    print("Welcome to Hack Clubber RPG!")
    print("")
    name = input("Your Hack Club name: ").strip() or "Hack Clubber"
    pclass = choose_class()
    player = Player(name, pclass)
    mmenu(player)


if __name__ == "__main__":
    start()
