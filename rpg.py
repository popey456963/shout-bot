from random import randint

# hp, accuracy, agility, strength, weapon (name, hp, accuracy, agility, strength)
basePlayerStats = {
    "Warrior": [20, 5, 2, 10, ["Cheap Sword", 0, 0, 0, 5]],
    "Archer": [10, 5, 4, 6, ["Plastic Bow", 0, 0, 0, 5]],
    "Mage": [15, 5, 3, 8, ["Toy Wand", 0, 0, 0, 5]]
}

baseEnemyStats = {
    "Goblin": [5, 3, 5, 5, ["Stick", 0, 0, 0, 5]],
    "Orc": [10, 6, 10, 5, ["Club", 0, 0, 0, 5]]
}

levelXP = [0, 20, 50, 125, 300, 750, 1875, 4500]

players = {}

class Dice:
    def __init__(self, num):
        self.sides = num
    def __repr__(self):
        die = randint(1, self.sides)
        return str(die)

class Player:
    def __init__(self, name, unit, hp, accuracy, agility, strength, weapon, exp, level):
        self.name = name
        self.unit = unit
        self.hp = hp
        self.accuracy = accuracy
        self.agility = agility
        self.strength = strength
        self.weapon = weapon
        self.exp = exp
        self.level = level
    def attack(self, enemyAgility):
        roll = int(str(Dice(enemyAgility + self.accuracy)))
        damage = self.strength
        if  roll > enemyAgility:
            return damage
        else:
            return 0
    def defend(self, enemyAccuracy, enemyStrength):
        roll = int(str(Dice(enemyAccuracy + self.agility)))
        if roll > self.agility:
            return enemyStrength
        else:
            return 0
    def levelUp(self):
        while self.exp > levelXP[self.level]:
            self.exp = self.exp - levelXP[self.level]
            self.level = self.level + 1


class Goblin:
    def __init__(self, unit, hp, accuracy, agility, strength, weapon):
        self.unit = unit
        self.hp = hp
        self.accuracy = accuracy
        self.agility = agility
        self.strength = strength
        self.weapon = weapon

def global_send(send):
    global sendMessage
    sendMessage = send

def sm_rpg(message):
    if message['user-id'] in players:
        sm_rpg_help(message)
    else:
        sm_rpg_setup(message)

def sm_rpg_listClasses(message):
    msg = "Currently supported classes include: Warrior, Archer and Mage"
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

def sm_rpg_help(message):
    msg = "Supported RPG Commands: /rpg, /rpg_help, /rpg_setup <class>, /rpg_listClasses"
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

def sm_rpg_setup(message):
    global players
    try:
        text = list(filter(None, message['message'].split(" ")))
        if text[1].title() in list(basePlayerStats.keys()):
            a = basePlayerStats[text[1].title()]
            players[message['user-id']] = {"player": Player(message['data-username'], text[1].title(), a[0], a[1], a[2], a[3], a[4], 0, 0)}
            players[message['user-id']]["enemy"] = None
            msg = message['data-username'] + ", we've created you a new character of class " + text[1].title()
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = text[1] + " is not a known class, please select one of either Warrior, Archer or Mage"
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    except:
        msg = "That is not a known class, please select one of either Warrior, Archer or Mage"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
        
def sm_rpg_fight(message):
    if message['user-id'] in players:
        if players[message['user-id']]['enemy'] == None:
            monster = "Goblin" if randint(0, 1) else "Orc"
            a = baseEnemyStats[monster]
            players[message['user-id']]['enemy'] = Goblin(monster, a[0], a[1], a[2], a[3], a[4])
            msg = "Oh no!  You encountered the fearsome " + monster + "."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = message['data-username'] + ", you're already fighting a monster!  You don't want to fight two at once."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", how are you going to fight if you don't have a character?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def sm_rpg_attack(message):
    if message['user-id'] in players:
        if 'enemy' in players[message['user-id']]:
            # players[message['user-id']]['player']
            # players[message['user-id']]['enemy']
            e = players[message['user-id']]['enemy']
            p = players[message['user-id']]['player']
            userDamage = p.attack(e.agility)
            goblinDamage = p.defend(e.accuracy, e.strength)
            if e.hp - userDamage > 0:
                # Enemy Lives
                e.hp = e.hp - userDamage
                if p.hp - goblinDamage > 0:
                    # Player Lives
                    p.hp = p.hp - goblinDamage
                    msg = "You damaged the goblin for " + str(userDamage) + " and it damaged you for " + str(goblinDamage) + "."
                    sendMessage(msg, private=message['private'], user=str(message['user-id']))
                else:
                    msg = "Oh noes, " + message['data-username'] + ", you died!"
                    sendMessage(msg, private=message['private'], user=str(message['user-id']))
                    players.pop(message['user-id'], None)
            else:
                msg = "You killed the goblin!  Congratulations!  You've earn 20XP."
                sendMessage(msg, private=message['private'], user=str(message['user-id']))
                players[message['user-id']]['player'].exp += 20
        else:
            msg = message['data-username'] + ", you're not fighting anyone at the moment!  Do /rpg_fight."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", how are you going to fight if you don't have a character?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def sm_rpg_stats(message):
    if message['user-id'] in players:
        p = players[message['user-id']]['player']
        msg = "| Name: " + p.name + " | Unit: " + p.unit + " | HP: " + str(p.hp) + " | Acc: " + str(p.accuracy) + " | Agt: " + str(p.agility) + " | Str: " + str(p.strength) + " | Wep: " + p.weapon[0] + " | Exp: " + str(p.exp) + " | Lvl: " + str(p.level) + " |"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    
def sm_rpg_estats(message):
    if message['user-id'] in players:
        if 'enemy' in players[message['user-id']]:
            p = players[message['user-id']]['enemy']
            msg = "| Unit: " + p.unit + " | HP: " + str(p.hp) + " | Acc: " + str(p.accuracy) + " | Agt: " + str(p.agility) + " | Str: " + str(p.strength) + " | Wep: " + p.weapon[0] + " |"
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = message['data-username'] + ", you're not fighting anyone at the moment!  Do /rpg_fight."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
