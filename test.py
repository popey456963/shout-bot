def wordLimit(func):
    def limit(string):
        maxLength = 480
        words = string.split(" ")
        parts = [""]

        for word in words:
            if len(parts[-1]) + len(word) + len(" ") > maxLength:
                parts.append(word)
            else:
                parts[-1] += " " + word
        for message in parts:
            func(message)
    return limit
    


@wordLimit
def sendMessage(message):
    print(message)


sendMessage("Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  Hello.  This is a very very very long sentence!  Have fun.  ")
