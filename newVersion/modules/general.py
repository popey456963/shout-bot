# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles all general command requests, such as help,
or assistance commands as well as others should they arise.
"""

def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

def g_help(message):
    msg = "Currently Supported Commands: !help and !wiki (or !define)"
    sendMessage(msg, private=message['private'], user=message['user-id']) 

commands = {
    "help": g_help
}
