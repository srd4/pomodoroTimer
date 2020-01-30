import auxiliarFunctions as aux
from datetime import datetime
import tomatoRecord as tr
import datetime as dt
import time



def allDates():
    # List of absolutely all dates as datetime objects since the first pomodoro.
    FIRSTDATE = datetime.strptime(tr.getPoms()[0][1], "%d/%m/%Y")
    delta = dt.datetime.today() - FIRSTDATE
    dates = []
    for i in range(delta.days+1):
        date = FIRSTDATE + dt.timedelta(days=i)
        dates.append(date)

    return dates

def getDoneIn(date):
    # Returns every pomodoro done at date. Date format is spected to be %d/%m/%Y.
    return [pom for pom in tr.getPoms() if pom[1] == date.strftime("%d/%m/%Y")]
    

def weeks():
    # Returns weeks list, a list of lists that each have days, where a Day is a list of tuples.
    # Each tuple has a date as first value and a list of pomodoros registered that day as second value.
    dates = allDates()
    weeks = []

    week = []
    for date in dates:
        if date.weekday() == 0:
            weeks.append(week)
            week = []

        week.append((date,))

    weeks.append(week)
    
    return weeks


def fillWeek(week):
    # To fill one week data structure of the pomodoros done on each day.
    # This since doing every week at the same time was slow.
    return [(day[0], getDoneIn(day[0])) for day in week]


def getWeek(index):
    t = weeks()
    return fillWeek(t[index])


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
    mostRecentPom = tr.getPomsBy("code", code)[-1]
    d1 = datetime.strptime(mostRecentPom[0] +"-"+mostRecentPom[1], "%H:%M:%S-%d/%m/%Y")
    d2 = datetime.now()
    delta = abs(d2-d1)

    return delta


def getAllCodes():
    # Returns list of strings, each one is a code, they're sorted by appearences.
    codes = aux.histogram(tr.getEvery("code"))
    tuplesList = [(code, codes[code]) for code in codes]
    tuplesList.sort(key=lambda x: x[1], reverse=True)

    return [tup[0] for tup in tuplesList]


def getInfo():
    #Returns a tuple with several information about pomodoro database.
    # (pomcount, hourCount, formatedHourCount, weekAverage, sinceStarted, doneToday)
    pomCount = len(tr.getPoms())
    hourCount = totalTime()/60
    days = str(int(hourCount/24)) + " days"
    weekAv = weekAverage()
    started = sinceFirst()
    today = pomsToday()

    return (pomCount, int(hourCount), days, weekAv, started, today)
    


def infoMessage():
    # General information message.
    message = "You have made {} pomodoros, that is {} hours or {} of productive focused work. Your average this week is {} a day so far and started {} days ago.\n\nToday you have done {}\n"

    return message.format(*getInfo())


def codeMessage(code):
    # Code specific information prompt.
    message = "You have worked on {} for {} hours ({} pomodoros or {} total hours). The last time you worked on {} was in {} or {} days ago."
    worked = aux.timeFormat(getPomTime(code)*60)
    workedPoms = str(len(fromCode(code)))
    hours = int(getPomTime(code)/60)
    lastTime = mostRecent(code)[1]

    return message.format(code, worked, workedPoms, hours, code, lastTime, longAgo(code))