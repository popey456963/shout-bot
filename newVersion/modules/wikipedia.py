# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles all wikipedia commands and definition
lookups.  Sentence splitting is done via NLTK tokenizers.
"""

import wikipedia


def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

def w_define(message):
    query = "Hi"
    summary = ""
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
    except wikipedia.exceptions.DisambiguationError as e:
        e = str(e).split("\n")
        e.pop(0)
        x = False
        if len(e) > 6:
            x = e
            e = e[0:6]
        summary = "Disambiguation Error.  Query may refer to: " + ", ".join(e)
        if x:
            summary = summary + " plus " + str(len(x) - 6) + " other options."
    print(summary)
    sendMessage(summary) 

commands = {
    "define": w_define,
    "wiki": w_define
}
