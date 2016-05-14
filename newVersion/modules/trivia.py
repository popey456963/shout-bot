# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles all trivia related commands, such as /trivia,
/answer and /leaderbaord.
"""

import re #Stripping Answers
import json #Leaderboard
from time import time #Trivia
from random import choice #Trivia
from modules.helpers import ordinal
from modules.helpers import ensureExists #Leaderboard

def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

"""
Desc:   Start a trivia if one isn't currently running
Input:  message dictionary
Output: None
"""
def t_trivia(message):
    global trivia
    if trivia['running']:
        msg = "A trivia is already running!"
        sendMessage(msg, private=mess['private'], user=message['user-id'])
    else:
        question = choice(open("data/questions.psv").readlines()).split("|")
        trivia['running'] = True
        trivia['difficulty'] = int(question[0])
        trivia['category'] = question[1]
        trivia['question'] = question[2]
        trivia['answers'] = question[3:]
        trivia['started'] = time()
        sendMessage(trivia['question'], private=False)

"""
Desc:   Test to see whether a user has answered a question correctly or not
Input:  message dictionary
Output: None
"""
def t_answer(message):
    if trivia['running']:
        theirAnswer = re.sub(r'\W+', '', message['message'].replace("!answer ", ""))
        correct = False
        for answer in trivia['answers']:
            ourAnswer = re.sub(r'\W+', '', answer)
            if theirAnswer.lower() == ourAnswer.lower():
                correct = True
        if correct:
            if message['data-username'] in leaderboard:
                leaderboard[message['data-username']] += 1
            else:
                leaderboard[message['data-username']] = 1
            storeLeaderboard()
            trivia['running'] = False
            msg = "Congratulations " + message['data-username'] + " on getting the answer right! That is the " + ordinal(leaderboard[message['data-username']]) + " question you've got right!"
            sendMessage(msg, private=False)
    else:
        msg = "You can't answer the trivia as there isn't one running."
        sendMessage(msg, private=message['private'], user=message['user-id'])

"""
Desc:   Get a users position in a leaderboard
Input:  message dictionary
Output: None
"""
def t_leaderboard(message):
    position = sorted(leaderboard, key=leaderboard.get, reverse=True).index(message['data-username'])+1
    msg = "You are currently in position " + str(position) + " out of the " + str(len(leaderboard)) + " people currently tracked."
    sendMessage(msg, private=message['private'], user=str(message['user-id']))

"""
Desc:   Update the leaderboard file so that it is persistant.
Input:  None
Output: None
"""
def storeLeaderboard():
    with open("data/triviaScores.json", "w") as f:
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

commands = {
    "trivia": t_trivia,
    "answer": t_answer,
    "leaderboard": t_leaderboard
}

trivia = {
    "running": False
}

ensureExists('data/triviaScores.json')
leaderboard = []
with open('data/triviaScores.json', "r") as f:
    leaderboard = json.load(f)
