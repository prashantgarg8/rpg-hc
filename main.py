import random
import time
import os
from typing import List, Dict

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, x): return ""
    Fore = Dummy()
    Style = Dummy()

ASCII_LOGO = rf"""
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
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
        self.lvl = 1
        self.xp = 0
        self.next_xp = 50
        self.hp = self.max_hp = cls['hp']
        self.atk = list(cls['attack'])
        self.gold = 0
        self.items = []
        self.gear = cls['tools'][:]
        self.moves = []
        self.badges = set()
        self.spot = "Coworking Space"
        self.breaks = 3

    def add_xp(self, amt):
        self.xp += amt
        while self.xp >= self.next_xp:
            self.xp -= self.next_xp
            self.lvl += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.atk[0] += 2
            self.atk[1] += 2
            self.next_xp = int(self.next_xp * 1.4)
            print(f"{Fore.YELLOW}\nLEVEL UP! Now level {self.lvl}!\n{Style.RESET_ALL}")
            self.new_move()

    def new_move(self):
        opts = ["Debug Surge", "Stack Overflow", "Pizza Heal"]
        for m in opts:
            if m not in self.moves:
                self.moves.append(m)
                print(f"{Fore.MAGENTA}Unlocked skill: {m}!{Style.RESET_ALL}")
                break

    def heal(self, amt):
        self.hp = min(self.max_hp, self.hp + amt)
        print(f"{Fore.GREEN}Healed for {amt}! HP is now {self.hp}/{self.max_hp}.{Style.RESET_ALL}")

class Enemy:
    def __init__(self, data: Dict):
        self.name = data['name']
        self.max_hp = self.hp = data['hp']
        self.atk = list(data['attack'])
        self.xp = data['exp']
        self.gold = data.get('coins', random.randint(10, 25))
        self.boss = data.get('is_boss', False)

    def think(self, p):
        return 'attack'

CLASSES = {
    'Frontend Dev': {
        'hp': 95, 'attack': (7, 17), "tools": ["Laptop", "Wi-Fi", "CSS Flexbox"]
    },
    'Backend Dev': {
        'hp': 110, 'attack': (9, 19), "tools": ["Laptop", "APIs", "SQL"]
    },
    'Fullstack': {
        'hp': 100, 'attack': (8, 18), "tools": ["Laptop", "Git", "Debug Goggles"]
    },
    'Hardware Hacker': {
        'hp': 105, 'attack': (6, 21), "tools": ["Soldering Iron", "Breadboard"]
    }
}

def pick_class() -> Dict:
    print("\nChoose your class:")
    for i, (cls, stats) in enumerate(CLASSES.items(), 1):
        print(f"{i}) {cls} - HP: {stats['hp']} | ATK: {stats['attack']} | Tools: {', '.join(stats['tools'])}")
    while True:
        choice = input("> ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(CLASSES):
                return list(CLASSES.values())[idx-1]
        except:
            pass
        print("Invalid. Enter a number to pick your class.")

BUGS = [
    {"name": "Segmentation Fault", "hp": 45, "attack": (8, 15), "exp": 12},
    {"name": "Merge Conflict", "hp": 55, "attack": (12, 22), "exp": 18},
    {"name": "JavaScript Bug", "hp": 65, "attack": (13, 23), "exp": 24},
    {"name": "Stack Overflow Demon", "hp": 80, "attack": (16, 25), "exp": 31},
    {"name": "Null Pointer Ninja", "hp": 90, "attack": (19, 29), "exp": 42},
    {"name": "Regex Goblin", "hp": 100, "attack": (17, 32), "exp": 55},
    {"name": "Legacy Code Dragon", "hp": 160, "attack": (22, 38), "exp": 100, "is_boss": True, "coins": 90}
]

def spawn_bug(lvl):
    if lvl % 5 == 0:
        return Enemy([b for b in BUGS if b.get("is_boss")][0])
    opts = [b for b in BUGS if not b.get("is_boss")]
    base = random.choice(opts)
    mult = 1 + 0.08*(lvl-1)
    info = base.copy()
    info['hp'] = int(info['hp']*mult)
    info['attack'] = (int(info['attack'][0]*mult), int(info['attack'][1]*mult))
    info['exp'] = int(info['exp']*mult)
    info['coins'] = int(base.get('coins', random.randint(10,25))*mult)
    return Enemy(info)

def hit(attacker, target):
    dmg = random.randint(*attacker.atk)
    crit = random.random() < 0.10
    if crit:
        dmg = int(dmg*1.5)
        print(f"{Fore.YELLOW}{attacker.name} lands a CRITICAL hit!{Style.RESET_ALL}")
    target.hp = max(0, target.hp - dmg)
    print(f"{attacker.name} hits {target.name} for {dmg} damage! ({target.hp}/{target.max_hp} HP left)")

def fight(p: Player):
    bug = spawn_bug(p.lvl)
    print(f"\n {bug.name} appears! (HP: {bug.hp})")
    if bug.boss:
        print(f"{Fore.RED}BOSS FIGHT!{Style.RESET_ALL}")

    buff_left = 0

    while bug.hp > 0 and p.hp > 0:
        print(f"\n{Fore.CYAN}Your HP: {p.hp}/{p.max_hp} | {bug.name}'s HP: {bug.hp}/{bug.max_hp}{Style.RESET_ALL}")
        print("1) Attack   2) Use Item   3) Skill   4) Attempt Escape")
        move = input("> ").strip()
        if move == "1":
            hit(p, bug)
        elif move == "2":
            use_stuff(p, in_fight=True, target=p)
            continue
        elif move == "3":
            if p.moves:
                print("Skills:", ", ".join(p.moves))
                print("Not implemented yet (coming soon!)")
            else:
                print("You have no skills yet.")
            continue
        elif move == "4":
            if bug.boss:
                print(f"{Fore.RED}Can't escape this time!{Style.RESET_ALL}")
            elif random.random() < 0.25:
                print(f"{Fore.GREEN}You slipped away successfully!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Couldn't escape!{Style.RESET_ALL}")
        else:
            print("Choose a valid move.")
            continue

        if bug.hp > 0:
            action = random.choices(
                population=["attack", "heal", "special"],
                weights=[0.7, 0.15, 0.15], k=1)[0]
            if action == "attack":
                hit(bug, p)
            elif action == "heal":
                heal_amt = min(25, bug.max_hp-bug.hp)
                bug.hp += heal_amt
                print(f"{Fore.BLUE}{bug.name} repairs itself for {heal_amt}!{Style.RESET_ALL}")
            else:
                if random.random() < 0.5:
                    print(f"{bug.name} tries to confuse your code! Lose your next attack turn.")
                else:
                    print(f"{bug.name} lags—no effect this turn.")

            if hasattr(p, 'buff_left') and p.buff_left > 0:
                p.buff_left -= 1
                if p.buff_left == 0:
                    p.atk[0] -= 6
                    p.atk[1] -= 6
                    print("Your debug buff faded.")

    if p.hp <= 0:
        print(f"{Fore.LIGHTRED_EX}\nYou burned out...{Style.RESET_ALL}")
        return False
    print(f"{Fore.GREEN} Debugged {bug.name}! +{bug.xp} EXP, +{bug.gold} coins!{Style.RESET_ALL}")
    p.add_xp(bug.xp)
    p.gold += bug.gold
    check_badges(p, context="boss" if bug.boss else "win_fight")
    return True

def menu(p: Player):
    while True:
        print("\n--- Main Menu ---")
        print("1) Take On a Challenge")
        print("2) View Stats")
        print("3) Rest (Restore Energy)")
        print("4) Shop")
        print("5) Travel")
        print("6) Achievements")
        print("7) Quit")
        choice = input("> ").strip()
        if choice == "1":
            ok = fight(p)
            if not ok:
                break
        elif choice == "2":
            print(f"\n Name: {p.name}")
            print(f" Class: {p.cls}")
            print(f" HP: {p.hp}/{p.max_hp}")
            print(f" Attack Power: {p.atk}")
            print(f" Level: {p.lvl}")
            print(f" EXP: {p.xp}/{p.next_xp}")
            print(f" Coins: {p.gold}")
            print(f" Tools: {', '.join(p.gear)}")
            print(f" Inventory: {', '.join(p.items) or 'Empty'}")
            print(f" Skills: {', '.join(p.moves) or 'None yet.'}")
        elif choice == "3":
            if p.breaks > 0:
                p.heal(p.max_hp)
                p.breaks -= 1
                print(f"{Fore.BLUE}You feel refreshed! Rests left: {p.breaks}{Style.RESET_ALL}")
                random_stuff(p, p.spot)
            else:
                print(f"{Fore.RED}No rests left!{Style.RESET_ALL}")
        elif choice == "4":
            store(p)
        elif choice == "5":
            go_places(p)
        elif choice == "6":
            show_badges(p)
        elif choice == "7":
            print(f"{Fore.CYAN} Thanks for playing Hack Clubber RPG!{Style.RESET_ALL}")
            break
        else:
            print("?? Invalid choice.")

def start():
    print(ASCII_LOGO)
    print("Welcome to Hack Clubber RPG!\n")
    name = input("Your Hack Club name: ").strip() or "Hack Clubber"
    cls = pick_class()
    p = Player(name, cls)
    menu(p)

STUFF = {
    "Coffee": {"type": "heal", "power": 40, "cost": 15, "desc": "Restores 40HP instantly."},
    "Energy Drink": {"type": "heal", "power": 80, "cost": 32, "desc": "Restores 80HP but stuns next turn."},
    "Debug Kit": {"type": "buff", "power": 6, "duration": 3, "cost": 30, "desc": "Boost ATK by 6 for 3 turns."},
    "Rubber Duck": {"type": "special", "cost": 25, "desc": "Resets one enemy action."},
    "Snack Bar": {"type": "heal", "power": 20, "cost": 8, "desc": "Minor HP recovery."},
}

def store(p):
    print(f"\n{Fore.LIGHTYELLOW_EX}== Code Supply Shop =={Style.RESET_ALL}")
    while True:
        print("Coins:", p.gold)
        for i, (name, data) in enumerate(STUFF.items(), 1):
            print(f"{i}. {name} ({data['cost']}g): {data.get('desc','')}")
        print("X. Leave Shop")
        choice = input("Buy what? > ").strip().upper()
        if choice == "X":
            break
        try:
            idx = int(choice)
            if 1 <= idx <= len(STUFF):
                item = list(STUFF.keys())[idx-1]
                if p.gold >= STUFF[item]['cost']:
                    p.gold -= STUFF[item]['cost']
                    p.items.append(item)
                    print(f"{Fore.GREEN}Purchased {item}!{Style.RESET_ALL}")
                else:
                    print("Not enough coins.")
            else:
                print("Pick a valid item number.")
        except ValueError:
            print("Enter item number or X.")

def use_stuff(p, in_fight=False, target=None):
    if not p.items:
        print("Inventory empty!")
        return False
    print("Inventory:", ", ".join(p.items))
    item = input("Use what? ").strip()
    if item not in p.items:
        print("Not in inventory.")
        return False

    info = STUFF.get(item)
    if not info:
        print("Unknown item.")
        return False
    if info["type"] == "heal":
        p.heal(info["power"])
    elif info["type"] == "buff":
        if in_fight and target:
            target.atk[0] += info["power"]
            target.atk[1] += info["power"]
            print(f"Attack power increased by {info['power']} for {info['duration']} turns!")
            target.buff_left = info['duration']
        else:
            print("Can only use in battle!")
    elif info["type"] == "special":
        if in_fight and target:
            target.skip = True
            print("The enemy looks confused... turn skipped!")
        else:
            print("Can only use in battle!")

    p.items.remove(item)
    return True

PLACES = [
    "Coworking Space",
    "Hackathon",
    "Basement Lab",
    "Rooftop Garden",
    "Mars Hacker Colony"
]
EVENTS = {
    "Hackathon": [
        "A free pizza break! Restore 30HP.",
        "Win mini-hack: gain 25 coins.",
        "Lose in bug bash: -10 hp."
    ],
    "Basement Lab": [
        "Find a mysterious old gadget (get Debug Kit).",
        "Trip over loose cable: -5 hp.",
        "Find snack bar under the desk."
    ],
    "Rooftop Garden": [
        "Breathe in fresh air: +10 hp.",
        "Meet a wise mentor: +25 exp.",
        "Laptop battery dies: must rest."
    ],
    "Mars Hacker Colony": [
        "Low gravity helps focus, +10 atk for next challenge.",
        "Solar flare! Lose a rest.",
        "Martian finds your bug: gain rare item."
    ]
}

def go_places(p):
    print("\nLocations:")
    for i, loc in enumerate(PLACES, 1):
        print(f"{i}) {loc}")
    print("X) Stay put")
    choice = input("Go where? > ").strip().upper()
    if choice == "X":
        return
    try:
        idx = int(choice)
        if 1 <= idx <= len(PLACES):
            new_spot = PLACES[idx-1]
            p.spot = new_spot
            random_stuff(p, new_spot)
        else:
            print("Invalid location.")
    except ValueError:
        print("Type number or X.")

def random_stuff(p, spot):
    if spot in EVENTS and random.random() < 0.6:
        event = random.choice(EVENTS[spot])
        print(f"{Fore.LIGHTMAGENTA_EX}Event: {event}{Style.RESET_ALL}")
        if "Restore" in event:
            hp = int([s for s in event.split() if s.isdigit()][0])
            p.heal(hp)
        elif "gain" in event and "coin" in event:
            coins = int([s for s in event.split() if s.isdigit()][0])
            p.gold += coins
            print(f"Gained {coins} coins!")
        elif "-hp" in event or "-" in event:
            dmg = int([s for s in event.replace("-"," -").split() if s.lstrip("-").isdigit()][0])
            p.hp = max(0, p.hp + dmg)
            print(f"Ouch! HP now {p.hp}")
        elif "exp" in event:
            exp = int([s for s in event.split() if s.isdigit()][0])
            p.add_xp(exp)
        elif "Debug Kit" in event:
            p.items.append("Debug Kit")
            print("Found a Debug Kit!")
        elif "snack bar" in event:
            p.items.append("Snack Bar")
            print("Yum! Got a Snack Bar.")
        elif "rare item" in event:
            p.items.append("Rubber Duck")
            print("You got... a Rubber Duck?!")

BADGES = [
    ("First Challenge", "Win your first battle."),
    ("Coffee Overdose", "Use 5 Coffee items in one run."),
    ("Mars Adventure", "Travel to Mars Hacker Colony."),
    ("Boss Buster", "Defeat a boss."),
    ("Overachiever", "Reach level 5.")
]

def check_badges(p, context=None):
    got = set(p.badges)
    if p.lvl >= 5:
        got.add("Overachiever")
    if p.spot == "Mars Hacker Colony":
        got.add("Mars Adventure")
    if any(item == "Coffee" for item in p.items) and p.items.count("Coffee") >= 5:
        got.add("Coffee Overdose")
    if context == "win_fight" and p.lvl == 1:
        got.add("First Challenge")
    if context == "boss" and p.lvl >= 2:
        got.add("Boss Buster")
    for badge, _ in BADGES:
        if badge in got and badge not in p.badges:
            print(f"{Fore.YELLOW}Achievement unlocked: {badge}!{Style.RESET_ALL}")
            p.badges.add(badge)

def show_badges(p):
    print("\nAchievements unlocked:")
    for badge, desc in BADGES:
        got = badge in p.badges
        mark = "[X]" if got else "[ ]"
        print(f"{mark} {badge}: {desc}")

if __name__ == "__main__":
    start()
