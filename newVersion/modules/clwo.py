# Made by Popey Gilbert (@Popey45963) for CLWO.EU
# Description: An automated bot for the shoutbox

"""
This file handles communication with CLWO.eu.  It does this
via interfacing with two API endpoints, which are:
 - https://clwo.eu/xmlhttp.php?action=dvz_sb_get_shouts
 - https://clwo.eu/xmlhttp.php?action=dvz_sb_shout
Note that there is a ratelimit on sending messages of a second,
and if this rate limit isthen the response to the post request
becomes "A", requiring a resend.

This shoutbox requires authentication, thus login() needs to be
called before use, it's parameters are the forum username and
forum password.  Using a session, we grab the cookies from this
login in order to get the unique SID to pretend to be the user.
"""

import requests, json # Various
from bs4 import BeautifulSoup # Scrape Shoutbox
from modules.helpers import rateLimiter # Rate Limiting Functionality
from modules.helpers import wordLimit # Word Limiter Functionality
from modules.helpers import handleException

BASE_URL = "https://clwo.eu/xmlhttp.php"
BASE_LOGIN = "https://clwo.eu/portal.php"

"""
Desc:   Logs the user in, provided it has the correct username
        and password provided to it
Input:  Two strings containing the username and a plaintext password.
Output: The sid value provided by the forums
"""
def login(username, password):
    login_data = {
        "action": "do_login",
        "quick_login": "1",
        "quick_username": username,
        "quick_password": password,
        "quick_remember": "yes"
    }

    session.post(BASE_LOGIN, login_data)

    cookies = session.cookies.get_dict()
    return cookies['sid']

"""
Desc:   Grabs the latest message ID to start tracking from
Input:  None
Output: Integer value of the last message ID
"""
def lastMessage():
    response = session.get(BASE_URL + "?action=dvz_sb_get_updates&from=3700").text
    return int(json.loads(response)['last'])

"""
Desc:   Gets a list of new shoutbox messages and parses them for
        their content (data-id, data-username, data-id, date, private
        message).
Input:  A string, mybbuser.
Output: An array of message objects.
"""
@rateLimiter(1)
def scrapeShoutbox():
    cookies = {
        "mybbuser": mybbuser
    }

    response = session.get(BASE_URL + "?action=dvz_sb_get_updates&from=" + str(lastMessageID), cookies=cookies).text
    
    if response:
        entries = json.loads(response)['html']
        soup = BeautifulSoup(entries, 'html.parser')
        messages = []

        for entry in soup.findAll("div", { "class" : "entry" }):
            message = {
                'data-id': entry['data-id'],
                'data-username': entry['data-username'],
                'user-id': entry.find("div", { "class" : "user" }).a['href'].split("/")[3].split(".")[0],
                'date': entry.find("span", { "class" : "date" }).get_text()
            }
            message['message'] = entry.find("div", { "class" : "text" }).get_text()
            messages.append(message)
        return messages
    else:
        return []

def setKeys(postkey, bbuser):
    global postKey, mybbuser
    postKey = postkey
    mybbuser = bbuser

@handleException("Error Sending Message: ")
@wordLimit
@rateLimiter(0.5)
def sendMessage(message, private=False, user=897, again=False):
    if not again:
        print("Message Sent: " + message[:63].lstrip())
        message = "(ShoutboxBot) " + message
    data = {
        "action": "dvz_sb_shout",
        "key": postKey,
        "text": message.lstrip()
    }

    cookies = {
        "mybbuser": mybbuser
    }
    """
    response = session.post(BASE_URL, data, cookies=cookies)
    print(response.text)
    if response.text == "A":
        sendMessage(message, private=private, user=user, again=True)
    """

session = requests.session()
lastMessageID = lastMessage()
postKey = ""
mybbuser = ""
