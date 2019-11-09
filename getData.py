import auxiliarFunctions as aux
from datetime import datetime
import tomatoRecord as tr
import datetime as dt
import time


def totalTime():
    # Returns total time spent doing pomodoros in MINUTES.
    return int(sum(tr.getEvery("duration")))


def sinceFirst():
    # Days since first pomodoro
    firstPom = tr.getPoms()[0]
    d1 = datetime.strptime(firstPom[1], "%d/%m/%Y")
    d2 = datetime.now()
    return abs((d2 - d1).days)


def pomsToday(date=time.strftime("%d/%m/%Y")):
    # Returns dictionary of poms done today.
    # Keys are codes, values are duration.
    poms = [pom for pom in tr.getPoms() if pom[1] == date]
    d = dict()

    for pom in poms:
        d[pom[3]] = int(d.get(pom[3],0)+pom[4])
        
    return d


def getWeekPoms(start=time.strftime("%d/%m/%Y")):
    # Returns histogram of everything done in last seven days including today.
    dates = []
    d = dict()
    for i in range(0,7):
        change = dt.datetime.strptime(start, "%d/%m/%Y") + dt.timedelta(days=-i)
        dates.append(pomsToday(change.strftime("%d/%m/%Y")))

    for date in dates:
        for key in date:
            d[key] = d.get(key,0)+date[key]

    return d


def weekAverage():
    # Returns average worked last seven days.
    d = getWeekPoms()
    return aux.timeFormat( int( ( ( sum( d.values() ) *60) /7) ) )[7:]


def fromCode(code):
    # Returns all pomodoros of certain code.
    return [pom for pom in tr.getPoms() if pom[3] == code]


def getPomTime(code):
    # Counts time spent on pomodoros of given code
    # takes: string
    # returns: int minutes.
    return sum(pom[4] for pom in tr.getPoms() if pom[3] == code)


def mostRecent(code):
    # Most recent pomodoro of given code that was done.
    poms = fromCode(code)
    return poms[-1]
    

def longAgo(code):
    # Difference between last date in which did pom with 'code' and today IN DAYS.
    mostRecentDate = tr.getPomsBy("code",code)[-1][1]
    d1 = datetime.strptime(mostRecentDate, "%d/%m/%Y")
    d2 = datetime.now()
    return abs((d2 - d1).days)


def getAllCodes():
    # Returns list of strings, each one is a code, they're sorted by appearences.
    codes = aux.histogram(tr.getEvery("code"))
    tuplesList = [(code, codes[code]) for code in codes]
    tuplesList.sort(key=lambda x: x[1], reverse=True)

    return [tup[0] for tup in tuplesList]


def infoMessage():
    # General information prompt.
    message = "You have made {} pomodoros, that is {} or {} of productive focused work. Your average this week is {} a day so far and started {} days ago.\n\nToday you have done {}\n"
    pomCount = len(tr.getPoms())
    hourCount = totalTime()/60
    timeFormatted = aux.timeFormat(hourCount*60*60)
    weekAv = weekAverage()
    started = sinceFirst()
    today = pomsToday()

    return message.format(pomCount, int(hourCount), timeFormatted, weekAv, started, today)


def codeMessage(code):
    # Code specific information prompt.
    message = "You have worked on {} for {} hours ({} pomodoros or {} total hours). The last time you worked on {} was in {} or {} days ago."
    worked = aux.timeFormat(getPomTime(code)*60)
    workedPoms = str(len(fromCode(code)))
    hours = int(getPomTime(code)/60)
    lastTime = mostRecent(code)[1]

    return message.format(code, worked, workedPoms, hours, code, lastTime, longAgo(code))