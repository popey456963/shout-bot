from modules.helpers import *
import modules.clwo as clwo
import modules.general as general
import modules.trivia as trivia
import modules.steam as steam

userData = loadData()

clwo.login(userData['username'], userData['password'])
clwo.setKeys(userData['postkey'], userData['mybbuser'])
clwo.sendMessage("Test Bot Online!", private=True)

setMessage(clwo.sendMessage)
general.setMessage(clwo.sendMessage)
trivia.setMessage(clwo.sendMessage)
steam.setMessage(clwo.sendMessage)

registeredCommands = {}
registeredCommands.update(general.commands)
registeredCommands.update(trivia.commands)
registeredCommands.update(steam.commands)

print("Commands:     " + ", ".join(["!" + i for i in list(registeredCommands.keys())]))

while 1:
    for message in reversed(clwo.scrapeShoutbox()):
        clwo.lastMessageID = handleMessage(message, registeredCommands, clwo.lastMessageID)
    trivia.testTrivia()
