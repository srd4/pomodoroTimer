import time

def cummulativeSum(aList):
    # Takes a list of numbers and returns its cummulative sum.
    count = 0
    newList = []
    for num in aList:
        count += num
        newList.append(count)
    
    return newList


def inSecs(string):
    # Converts time in format HH:MM:SS as integer representing seconds.
    t = [int(i) for i in string.split(":")]
    return (t[0]*60*60)+(t[1]*60)+t[2]

def timeFormat(seconds):
    # Turns secs into nice format.
    # takes: int
    # returns: string"""
    days = int(seconds/60/60/24)
    hours = int((seconds/60/60)%24)
    minutes = int((seconds/60) % 60)
    secs = int((seconds) % 60)
    return "{0} days {1:02d}:{2:02d}:{3:02d}".format(days, hours, minutes,secs)


def cleanString(aString):
    # Returns same string without garbage characters.
    garbage = ["\t","\n","\r","\x0b","\x0c", "\ufeff"]
    newString = aString
    for char in garbage:
        if char in aString:
            newString = newString.replace(char,"")
            
    return newString

def histogram(aList):
    # Counts appearences of each element in list.
    # returns:  dict()
    d = dict()
    for element in aList:
        d[element] = d.get(element, 0)+1
    
    return d


def countDownIterator(secs):
    # Creates countdown iterator.
    # takes : int"""
    for num in range(secs,0,-1):
        minutes = int(num/60)
        seconds = (num%60)
        yield "%02d:%02d"%(minutes,seconds)

def printCountDown(secs, wait=True):
    # Calls creationg of countdown iterator and prints it.
    for count in countDownIterator(secs):
        print(count, end="\r")
        time.sleep(wait)

    return True

