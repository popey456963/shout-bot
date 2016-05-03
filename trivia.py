from bot import sendMessage
from bot import ensureExists

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

trivia = { "running": False, "runtime": 60 }
ensureExists("data.json")
ensureExists("steam.json")

print("All Necessary Files Exist")

leaderboard = []
with open('data.json') as f:
    leaderboard = json.load(f)
