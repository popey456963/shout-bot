# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles all CLWO server interactions or other services
that utilise the Steam API/service in any way.
We use a dictionary to store the interactions between Steam3ID
and any other possible formats.  This has a user endpoint through
the commands of /setSteam and /getSteam.
"""

from modules.helpers import ensureExists # Persistance of SteamIDs
import json # SteamIDs and API

def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

def s_setSteam(message):
    global steamIDs
    searchValue = message['message'].lstrip(" ").split(" ")[1]
    print("Checking for SteamID: " + searchValue)
    data = json.loads(requests.get(api + "accounts.php?key=*&value=" + searchValue).text)
    keys = []
    for key in data['data'].keys():
        keys.append(key)
    print(keys)
    if len(keys) == 1:
        steamIDs[message['data-username']] = keys[0]
        msg = message['data-username'] + ", I've set your AccountID to be: " + keys[0]
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
        storeSteam()
    else:
        msg = "That SteamID is either invalid, or there were multiple options that it could be"
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    # print(data['data'])

"""
Desc:   Get a SteamID for a user
Input:  message dictionary
Output: None
"""
def s_getSteam(message):
    name = message['data-username']
    if name in steamIDs:
        msg = "Your currently set Account ID is: " + steamIDs[name]
    else:
        msg = "You haven't set your own Account ID!  You can do so by doing !setSteam <>."
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   See the current warning level of a user
Input:  message dictionary
Output: None
"""
def s_warnings(message):
    try:
        steamID = steamIDs[message['data-username']]
        text = json.loads(requests.get(api + "warnings.php?Key=*&Value=" + steamID).text)
        data = text['data'][steamID]
        msg = message['data-username'] + ", your low warning level is " + str(data['low']) + "%, your medium warning level is " + str(data['medium']) + "% and your high warning level is " + str(data['high']) + "%."
        sendMessage(msg, private=message['private'], user=str(message['user-id']))
    except:
        sendMessage(message['data-username'] + ", either your Steam3ID is wrong, or the API is down for the moment", private=message['private'], user=str(message['user-id']))

"""
Desc:   Get current server information
Input:  message dictionary
Output: None
"""
def s_info(message):
    data = json.loads(requests.get(api + "server/info.php").text)
    msg = "There are currently " + str(data['data']['numberOfPlayers']) + " out of " + str(data['data']['maxPlayers']) + " players online playing " + data['data']['mapName']
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Get current online playesr
Input:  message dictionary
Output: None
"""
def s_players(message):
    data = json.loads(requests.get(api + "server/players.php").text)
    players = []
    for i in data['data']:
        if i['clientPort'] != "null":
            players.append(str(i['name'].encode('ascii','ignore'))[2:-1])
    # print(str(data['datainfo']['active']))
    # print(players)
    msg = "Players Online (" + str(data['datainfo']['active']) + "): " + ", ".join(players)
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Save all of the steamIDs to file
Input:  None
Output: None
"""
def storeSteam():
    with open("steam.json", "w") as f:
        json.dump(steamIDs, f)

commands = {
    "setSteam": s_setSteam,
    "getSteam": s_getSteam,
    "warnings": s_warnings,
    "warning": s_warnings,
    "info": s_info,
    "players": s_players,
    "online": s_players
}

ensureExists("data/steamIDs.json")

steamIDs = []
with open('data/steamIDs.json') as f:
    steamIDs = json.load(f)
