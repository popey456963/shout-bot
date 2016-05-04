#!/usr/bin/env python3
import requests, json, time, random, os, re, sys

if __name__ == '__main__':
    from bs4 import BeautifulSoup
    from urllib.parse import urlencode
    from rpg import *

userData = {}

with open("config.txt", "r") as f:
    for i in f.readlines():
        userData[i.split("=")[0]] = i.split("=")[1].strip()

if __name__ == '__main__':
    print(userData)

"""
Desc:   The ordinal function exists to turn numbres from the form of "1", "2", "3" to "1st", "2nd", "3rd"
Input:  An integer number
Output: An ordinal string
"""
SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

"""
Desc:   Ensures that a file exists by testing whether it is there, and if it is not creating it
Input:  The location to a file
Ouptut: None
"""
def ensureExists(file):
    if not os.path.isfile(file):
        with open("data.json", "w") as f:
            f.write("{}")

"""
Desc:   A decorator function to force a function to only run once ever x seconds
Input:  The max amount of times this function can be run every second.
Output: None
"""
def rateLimiter(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

"""
Desc:   Grab the latest received message
Input:  None
Output: Integer representing the last message ID
"""
def lastMessage():
    response = requests.get("https://clwo.eu/xmlhttp.php?action=dvz_sb_get_shouts&from=3500").text
    response = json.loads(response)
    return int(response['last'])

"""
Desc:   Requests login function for the forums
Input:  None
Output: None
"""
def loginAPI():
    login_data = {
        "action": "do_login",
        "quick_login": "1",
        "quick_username": userData['forumUsername'],
        "quick_password": userData['forumPassword'],
        "quick_remember": "yes"
    }

    s.post('https://clwo.eu/portal.php', login_data)

"""
Desc:   Scrapes the shoutbox on the forums for all new messages
Input:  None
Output: Array of message dictionaries
"""
@rateLimiter(0.33)
def scrapeShoutbox():
    cookie = {
        "mybbuser": userData['mybbuser']
    }
    entries = s.get("https://clwo.eu/xmlhttp.php?action=dvz_sb_get_shouts&from=" + str(lastMessageID), cookies=cookie).text
    # print("We got some messages since " + str(lastMessageID))
    if entries == "":
        return []
    else:
        # entries = json.loads((bytes(entries, "utf-8").decode('unicode_escape')).replace("\\/", "/"))['html']
        entries = json.loads(entries)['html']
        # print(entries)
        soup = BeautifulSoup(entries, 'html.parser')
        messages = []
        for html in soup.findAll("div", { "class" : "entry" }):
            message = {}
            message['data-id'] = html['data-id']
            message['data-username'] = html['data-username']
            message['user-id'] = html.div.a['href'].split("&")[1]
            message['date'] = html.find("span", { "class" : "date" }).string
            message['private'] = True if "Private shout" in str(html.find("span", { "class" : "private-message" })) else False
            if message['private']:
                text = html.find("div", { "class" : "text" })
                span = html.find("span", { "class" : "private-message" })
                message['message'] = (text.get_text()).replace(span.get_text(), "")
            else:
                message['message'] = html.find("div", { "class" : "text" }).string
            # print(message)
            messages.append(message)
            print("Received Message: " + message['message'])
        return messages

"""
Desc:   Run a function depending on the message input received
Input:  List of message dictionaries
Output: None
"""
def handleMessages(messages):
    global lastMessageID
    for message in reversed(messages):
        if int(message['data-id']) > lastMessageID:
            # print(message)
            lastMessageID = int(message['data-id'])
            if message['message'] != None:
                text = message['message'].lstrip()
                if text.split(" ")[0][0] == "!" or text.split(" ")[0][0] == "/":
                    try:
                        registeredCommands[text.split(" ")[0][1:]](message)
                        print("Handled Command: " + text)
                    except KeyError as err:
                        print("Unknown Command: " + str(err))
                        sendMessage("Unknown Command...", private=True, user=message['user-id'])
            else:
                pass

"""
Desc:   Sends a message through the chatbox
Input:  String for message text, Boolean for whether it is private or not, User to message if it is private
Output: None
"""
def splitPreserveWord(sentence):
    partLength = 470
    words = sentence.split(" ")
    parts = [""]
    partCounter = 0
    for word in words:
        if len(word) + len(parts[partCounter]) + 1 > partLength:
            partCounter += 1
        if parts[partCounter]:
            parts[partCounter] += " " + word
        else:
            parts[partCounter] = word
    return parts

@rateLimiter(0.5)
def sendMessage(message, private=False, user="897"):
    indMessages = [message[i:i+470] for i in range(0, len(message), 470)]
    for toSend in indMessages:
        rawSendMessage(toSend, private=private, user=user)

def rawSendMessage(message, private=False, user="897", again=False):
    if not again:
        print("Message Sent:    " + message[:63])
        if private:
            message = "/pvt " + user + " (ShoutboxBot) " + message
        else:
            message = "(ShoutboxBot) " + message

    data = {
        "action": "dvz_sb_shout",
        "key": userData['postKey'],
        "text": message
    }

    cookie = {
        "mybbuser": userData['mybbuser']
    }

    reply = s.post("https://clwo.eu/xmlhttp.php", data, cookies=cookie)
    if reply.text == "A":
        rawSendMessage(message, private=private, user=user, again=True)
    
# global_send(sendMessage)

"""
Desc:   List all currently possible commands and their syntax
Input:  message dictionary
Output: None
"""
def sm_help(message):
    helpMessage = "Currently Supported Commands: !help, !trivia, !answer <answer>, !leaderboard, !setSteam <Steam3ID>, !getSteam, !warnings, !info, !players" 
    sendMessage(helpMessage, private=message['private'], user=str(message['user-id']))

"""
Desc:   Start a trivia if one isn't currently running
Input:  message dictionary
Output: None
"""
def sm_trivia(message):
    global trivia
    if trivia['running']:
        sendMessage("A trivia is already running!", private=message['private'], user=str(message['user-id']))
    else:
        question = random.choice(open("questions.psv").readlines()).split("|")
        trivia['running'] = True
        trivia['difficulty'] = int(question[0])
        trivia['category'] = question[1]
        trivia['question'] = question[2]
        trivia['answers'] = question[3:]
        trivia['started'] = time.time()
        sendMessage(trivia['question'], private=False)

"""
Desc:   Test to see whether a user has answered a question correctly or not
Input:  message dictionary
Output: None
"""
def sm_answer(message):
    theirAnswer = re.sub(r'\W+', '', message['message'].replace("!answer ", ""))
    correct = False
    for answer in trivia['answers']:
        ourAnswer = re.sub(r'\W+', '', answer)
        if theirAnswer.lower() == ourAnswer.lower():
            correct = True
    if correct:
        if message['data-username'] in leaderboard: leaderboard[message['data-username']] += 1
        else: leaderboard[message['data-username']] = 1
        userMessage = "Congratulations " + message['data-username'] + " on getting the answer right! That is the " + ordinal(leaderboard[message['data-username']]) + " question you've got right!"
        trivia['running'] = False
        sendMessage(userMessage, private=False, user=str(message['user-id']))

"""
Desc:   Get a users position in a leaderboard
Input:  message dictionary
Output: None
"""
def sm_leaderboard(message):
    position = sorted(leaderboard, key=leaderboard.get, reverse=True).index(message['data-username'])+1
    msg = "You are currently in position " + str(position) + " out of the " + str(len(leaderboard)) + " people currently tracked."
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Attempt to set a steam id for a user
Input:  message dictionary
Output: None
"""
"""
# An in progress setSteam version that allows for SteamIDs other than 64.
def sm_setSteam(message):
    global steamIDs
    searchValue = message['message'].split(" ")[1]
    print(searchValue)
    data = json.loads(requests.get(api + "accounts.php?Key=*&Value=" + searchValue).text)
    print(data)
    steamIDs[message['data-username']] = data['data'][searchValue]
    print(data['data'][searchValue])
    msg = message['data-username'] + ", I've successfully set your AccountID to be: " + data['data'][searchValue]
    sendMessage(msg, private=message['private'], user=str(message['user-id']))
"""
def sm_setSteam(message):
    print(message['message'])
    print(message['message'].split(" "))
    value = message['message'].split(" ")
    values = []
    for i in value:
        if i != "":
            values.append(i)
    print(values[1])
    value = values[1]
    steamIDs[message['data-username']] = value
    msg = message['data-username'] + ", I've set your AccountID to be: " + value
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Get a steam id for a user
Input:  message dictionary
Output: None
"""
def sm_getSteam(message):
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
def sm_warnings(message):
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
def sm_info(message):
    data = json.loads(requests.get(api + "server/info.php").text)
    msg = "There are currently " + str(data['data']['numberOfPlayers']) + " out of " + str(data['data']['maxPlayers']) + " players online playing " + data['data']['mapName']
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Get current online playesr
Input:  message dictionary
Output: None
"""
def sm_players(message):
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

"""
Desc:   Save all of the trivia scores to file
Input:  None
Output: None
"""
def storeLeaderboard():
    with open("data.json", "w") as f:
        json.dump(leaderboard, f)

"""
Desc:   Check to see whether the trivia should still be running
Input:  None
Output: None
"""
def testTrivia():
    global trivia
    if trivia['running']:
        if trivia['runtime'] < time.time() - trivia['started']:
            sendMessage("Noone answered the question in time! The answer was: " + trivia['answers'][0])
            trivia['running'] = False

s = requests.session()

print("Request Sesssion Successfully Instatiated")

lastMessageID = 90000
api = "https://clwo.eu/jailbreak/api/v1/"

if __name__ == '__main__':
    trivia = { "running": False, "runtime": 60 }
    ensureExists("data.json")
    ensureExists("steam.json")

    print("All Necessary Files Exist")

    steamIDs = []
    with open('steam.json') as f:
        steamIDs = json.load(f)

    leaderboard = []
    with open('data.json') as f:
        leaderboard = json.load(f)

    print("We've Loaded Previous Configurations")

    registeredCommands = {
        "help": sm_help,
        "trivia": sm_trivia,
        "answer": sm_answer,
        "leaderboard": sm_leaderboard,
        "setSteam": sm_setSteam,
        "getSteam": sm_getSteam,
        "warnings": sm_warnings,
        "info": sm_info,
        "players": sm_players,
        "rpg": sm_rpg,
        "rpg_help": sm_rpg_help,
        "rpg_setup": sm_rpg_setup,
        "rpg_listClasses": sm_rpg_listClasses,
        "rpg_fight": sm_rpg_fight,
        "rpg_attack": sm_rpg_attack,
        "rpg_stats": sm_rpg_stats,
        "rpg_estats": sm_rpg_estats,
        "rpg_shop": sm_rpg_shop,
        "rpg_buy": sm_rpg_buy,
        "rpg_rest": sm_rpg_rest
    }

loginAPI()
cookies = s.cookies.get_dict()

if __name__ == '__main__':
    print("Our Cookie SID Is: " + cookies['sid'])

lastMessageID = lastMessage()

if __name__ == '__main__':
    print("The last message appears to be: " + str(lastMessageID))

    sendMessage("The bot is now up and functional!", private=True)
    while 1:
        try:
            testTrivia()
            handleMessages(scrapeShoutbox())
            # sendMessage("An unhandled error came about.  Check logs for more info", private=True)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("Unexpected Error: " + str(sys.exc_info()[0]))
            print("Unexpected Error: " + str(sys.exc_info()[1]))
            print("Unexpected Error: " + str(sys.exc_info()[2]))
            
