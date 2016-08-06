# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles helper functions for the main thread.  Occasionally
this may also be called from non-main threads, hence this program will
contain only functions and will not computer anything on import.
"""

import time # Rate Limiter
import json # Load Data
import os # Ensure Exists
import sys # Error Handling
import traceback # Error Handling
import threading # For async repeats

"""
Desc:   The ordinal function exists to turn numbers from the form of 1,
        2, 3 to "1st", "2nd", "3rd".
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
Desc:   Ensures that there is at very least an empty json file at the
        specified path.  
Input:  The location to a file
Ouptut: None
"""
def ensureExists(file):
    if not os.path.isfile(file):
        with open(file, "w") as f:
            f.write("{}")

"""
Desc:   A decorator function to force a function to only run once ever
        x seconds.
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
Desc:   A decorator that forces the first argument to a function to be
        under 480 characters, else it splits it up and sends it to the
        function in chunks.
Input:  A string of any length.
Output: Calls the decorated function X times with shorter messages.
"""
def wordLimit(func):
    def limit(string, *args, **kwargs):
        maxLength = 480
        words = string.split(" ")
        parts = [""]

        for word in words:
            if len(parts[-1]) + len(word) + len(" ") > maxLength:
                parts.append(word)
            else:
                parts[-1] += " " + word
        for message in parts:
            func(message, *args, **kwargs)
    return limit

def loadData():
    return json.loads("\n".join(open("data/config.json", "r").readlines()))

def setMessage(sendMessageArg):
    global sendMessage
    sendMessage = sendMessageArg

def handleException(job, errorFunc=None):
    def decorate(func):
        def exception(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as err:
                print(job + "`" + "`,`".join([*args]) + "`")
                print(sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1]))
                traceback.print_tb(err.__traceback__)
                if errorFunc:
                    errorFunc()
        return exception
    return decorate

def handleMessageException(job):
    def decorate(func):
        def exception(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(job + "`" + "`,`".join([*args]) + "`")
                print(sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1]))
                traceback.print_tb(err.__traceback__)
                return args[2] + 1
        return exception
    return decorate

@handleMessageException("An error occurred whilst parsing the following command: ")
def handleMessage(message, commands, lastMessageID):
    if int(message['data-id']) > lastMessageID:
        if message['message'] != None:
            text = message['message'].lstrip()
            if text.split(" ")[0][0] == "!" or text.split(" ")[0][0] == "/":
                try:
                    commands[text.split(" ")[0][1:]](message)
                    print("Handled Command: " + text)
                except KeyError as err:
                    print("Unknown Command: " + str(err))
                    sendMessage("Unknown Command...", private=True, user=message['user-id'])
        return int(message['data-id'])
    else:
        return lastMessageID

def repeatAsync():
    print("Running")
    threading.Timer(5, f).start()
