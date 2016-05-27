# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles the RPG aspect of the shoutbox. It stores
user-data and enemy-data in arrays, which although inefficient,
should work with the small number of people that are likely to
use it.

Classes are provided for players and enemies, and these classes
need to interact with each other to provide the RPG.
"""

def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

from random import randint
from math import floor
import sys

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

coeaponShop = {
    # Cost, HP, Accuracy, Agility, Strength
    "Warrior": {
        "Wooden Sword": [0, 0, 0, 0, 5],
        "Tiny Dagger": [50, 0, 0, 3, 6]
    },
    "Archer": {
        "Plastic Bow": [0, 0, 0, 0, 5],
        "Crossow": [50, 0, 3, 0, 6]
    },
    "Mage": {
        "Toy Wand": [0, 0, 0, 0, 5],
        "Defense Wand": [50, 5, 0, 0, 6]
    }
}

levelXP = [0, 20, 50, 125, 300, 750, 1875, 4500]
restingCost = 10
players = {}

class Dice:
    def __init__(self, num):
        self.sides = num
    def __repr__(self):
        die = randint(1, self.sides)
        return str(die)

class Player:
    def __init__(self, name, unit, hp, accuracy, agility, strength, weapon, exp, level, gold):
        self.name = name
        self.unit = unit
        self.hp = hp
        self.maxhp = hp
        self.accuracy = accuracy
        self.agility = agility
        self.strength = strength
        self.weapon = weapon
        self.exp = exp
        self.level = level
        self.gold = gold
    def attack(self, enemyAgility):
        roll = int(str(Dice(enemyAgility + self.accuracy)))
        damage = self.strength + self.weapon[4]
        if  roll > enemyAgility:
            return damage
        else:
            return 0
    def defend(self, enemyAccuracy, enemyStrength):
        roll = int(str(Dice(enemyAccuracy + self.agility)))
        if roll > self.agility:
            return enemyStrength + enemyWeapon[4]
        else:
            return 0
    def levelUp(self):
        didLevelUp = False
        while self.exp > levelXP[self.level]:
            self.exp = self.exp - levelXP[self.level]
            self.level = self.level + 1
            self.hp = floor(self.hp * 1.5)
            self.maxhp = floor(self.maxhp * 1.5)
            self.accuracy = floor(self.accuracy * 1.5)
            didLevelUp = True
        return didLevelUp

class Goblin:
    def __init__(self, unit, hp, accuracy, agility, strength, weapon):
        self.unit = unit
        self.hp = hp
        self.accuracy = accuracy
        self.agility = agility
        self.strength = strength
        self.weapon = weapon

def rpg_home(message):
    if message['user-id'] in players:
        sm_rpg_help(message)
    else:
        sm_rpg_setup(message)

def rpg_listClasses(message):
    msg = "Currently supported classes include: Warrior, Archer and Mage"
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_help(message):
    msg = "Supported RPG Commands: /rpg, /rpg_help, /rpg_setup <class>, /rpg_listClasses, /rpg_fight, /rpg_attack, /rpg_stats, /rpg_estats, /rpg_shop, /rpg_buy"
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_setup(message):
    global players
    try:
        text = list(filter(None, message['message'].split(" ")))
        if text[1].title() in list(basePlayerStats.keys()):
            a = basePlayerStats[text[1].title()]
            players[message['user-id']] = {"player": Player(message['data-username'], text[1].title(), a[0], a[1], a[2], a[3], a[4], 0, 0, 50)}
            players[message['user-id']]["enemy"] = None
            msg = message['data-username'] + ", we've created you a new character of class " + text[1].title()
            #sendMessage(msg, private=message['private'], user=str(message['user-id']))
            #msg = "You arrive in town after a long walk from the forest.  There seems to be a commotion at the town square.  You head to the town square.  You see an old man standing on a crate - it makes him a bit taller than the people around him.  When you come closer, you can see that the old man is actually the local town sage!  The sage speaks: \"I have seen them, the foul demons from hell!  They appeared right in front of me, when I was on my ingredient hunt.  They started to attack me... and... *cough*.. I was just barely capable of beating them... \" He grabs a small bottle out of his pocket and takes a sip.  \"We must fight back against these demons!\", he shouts.  But the people around him are starting to believe the sage fell to the famous alcohol of the inn on the way back to town.  The sage stumbles off.  You follow him to get to know more - as you always wanted to go on an adventure.  The sage enters his house.  You follow him inside, and take a seat on the floor.  It seems that the sage hasn't noticed you yet.  He shouts: \"Why won't they believe th-\" He sees you, and first looks surprised, then hopeful.  \"You do believe me, don't you?\" He thinks for a moment, and then walks to his bed.  He reaches under his bed, muttering some curses, and then holds up a small box.  \"You must defeat the demons.  I can sense that the demons that attacked me are nothing in comparison with the demons that will be coming.\"  He hands you a tiny wooden dagger. \"Go now, warrior.  I think the greater evils are rising as we speak.  I fear that Diablo, the Lord of Terror walks the earth once more...\"  You accept the dagger, and set out to start your adventure..."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = text[1] + " is not a known class, please select one of either Warrior, Archer or Mage"
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    except:
        print(sys.exc_info()[0])
        msg = "That is not a known class, please select one of either Warrior, Archer or Mage with /rpg <className>"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
        
def rpg_fight(message):
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

def rpg_attack(message):
    if message['user-id'] in players:
        if 'enemy' in players[message['user-id']]:
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
                players[message['user-id']]['player'].gold += 10
                if players[message['user-id']]['player'].levelUp():
                    msg = message['data-username'] + ", You've levelled up!  You're now level " + str(players[message['user-id']]['player'].level) + "."
                    sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = message['data-username'] + ", you're not fighting anyone at the moment!  Do /rpg_fight."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", how are you going to fight if you don't have a character?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_stats(message):
    if message['user-id'] in players:
        p = players[message['user-id']]['player']
        msg = "| Name: " + p.name + " | Unit: " + p.unit + " | HP: " + str(p.hp) + " | Acc: " + str(p.accuracy) + " | Agt: " + str(p.agility) + " | Str: " + str(p.strength) + " | Wep: " + p.weapon[0] + " | Exp: " + str(p.exp) + " | Lvl: " + str(p.level) + " | Gold: " + str(p.gold) + " |"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    
def rpg_estats(message):
    if message['user-id'] in players:
        if 'enemy' in players[message['user-id']]:
            p = players[message['user-id']]['enemy']
            if p != None:
                msg = "| Unit: " + p.unit + " | HP: " + str(p.hp) + " | Acc: " + str(p.accuracy) + " | Agt: " + str(p.agility) + " | Str: " + str(p.strength) + " | Wep: " + p.weapon[0] + " |"
                sendMessage(msg, private=message['private'], user=str(message['user-id']))
            else:
                msg = message['data-username'] + ", you're not fighting anyone at the moment!  Do /rpg_fight."
                sendMessage(msg, private=message['private'], user=str(message['user-id']))
        else:
            msg = message['data-username'] + ", you're not fighting anyone at the moment!  Do /rpg_fight."
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment?  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_shop(message):
    if message['user-id'] in players:
        msg = message['data-username'] + ", to buy an item, do /rpg_buy <itemNumber>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
        unit =  players[message['user-id']]['player'].unit
        print("Grabbing shop for: " + unit)
        weapons = weaponShop[unit]
        sortedWeapons = sorted(weaponShop[unit], key=lambda k: k[0])
        print(weapons)
        index = len(list(sortedWeapons))
        for weapon in sortedWeapons:
            print("Printing index " + str(index) + " with weapon " + weapon)
            try:
                print(weapons[weapon])
            except:
                print("Weapons has no index, this makes us sad.")
                print("What happens next isn't going to go well,  we should probably do something.")
                print("But, I don't think I can be bothered right now.  This might not happen often.")
            msg = str(index) + ". " + weapon + " | Cost: " + str(weapons[weapon][0]) + " | HP: " + str(weapons[weapon][1]) + " | Acc: " + str(weapons[weapon][2]) + " | Agt: " + str(weapons[weapon][3]) + " | Str: " + str(weapons[weapon][4]) + " |"
            print(msg)
            sendMessage(msg, private=message['private'], user=str(message['user-id']))
            index -= 1
        msg = "You currently have " + str(players[message['user-id']]['player'].gold) + " gold and your equipped weapon is " + players[message['user-id']]['player'].weapon[0] + "."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment, how are you going to buy things!  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_buy(message):
    userMsg = list(filter(None, message['message'].split(" ")))
    if message['user-id'] in players:
        unit =  players[message['user-id']]['player'].unit
        gold = players[message['user-id']]['player'].gold
        items = weaponShop[players[message['user-id']]['player'].unit]
        numberItems = len(items)
        sortedItems = sorted(weaponShop[unit], key=lambda k: k[0], reverse=True)
        itemPurchase = items[sortedItems[int(userMsg[1]) - 1]]
        if itemPurchase[0] <= gold:
            msg = "You have purchased a " + sortedItems[int(userMsg[1]) - 1] + " for the sum total of " + str(itemPurchase[0]) + " coins."
            players[message['user-id']]['player'].gold -= itemPurchase[0]
            itemName = sortedItems[int(userMsg[1]) - 1]
            players[message['user-id']]['player'].weapon = [itemName, itemPurchase[1], itemPurchase[2], itemPurchase[3], itemPurchase[4]]
        else:
            msg = "You don't have enough money to buy a " + sortedItems[int(msg[1]) - 1] + ".  You need " + str(itemPurchase[0] - gold) + " more coins to buy it!"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment, how are you going to buy things!  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_rest(message):
    userMsg = list(filter(None, message['message'].split(" ")))
    if message['user-id'] in players:
        gold = players[message['user-id']]['player'].gold
        if restingCost <= gold:
            msg = "You have rested and your health has been restored."
            players[message['user-id']]['player'].gold -= 10
            players[message['user-id']]['player'].hp = players[message['user-id']]['player'].maxhp
        else:
            msg = "You don't have enough money to rest.  You need " + str(10 - gold) + " more coins to buy it!"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    else:
        msg = message['data-username'] + ", you don't have a character at the moment, how are you going to rest!  Do /rpg <className>."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))

def rpg_save():
    # Save the players dictionary with pickle

def rpg_load():
    # Load the players dictionary from pickle

commands = {
    "rpg": rpg_home,
    "rpg_listClasses": rpg_listClasses,
    "rpg_help": rpg_help,
    "rpg_setup": rpg_setup,
    "rpg_fight": rpg_fight,
    "rpg_attack": rpg_attack,
    "rpg_stats": rpg_stats,
    "rpg_estats": rpg_estats,
    "rpg_shop": rpg_shop,
    "rpg_buy": rpg_buy,
    "rpg_rest": rpg_rest
}
