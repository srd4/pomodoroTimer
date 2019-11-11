import matplotlib.pyplot as plt
import tomatoRecord as tr
from datetime import date, timedelta,datetime
import auxiliarFunctions as aux
from matplotlib.ticker import FuncFormatter, MaxNLocator
import getData

FIRSTDATE = datetime.strptime(tr.getPoms()[0][1], "%d/%m/%Y")

def bar(d):
    # Bar plots a dictionary, Maps x,y = keys, values.
    x,y = d.keys(),d.values()

    plt.bar(x,y)
    plt.grid()
    plt.show()

    return True

def allDates():
    # List of absolutely all dates as datetime objects since the first pomodoro.
    delta = datetime.today() - FIRSTDATE
    dates = []
    for i in range(delta.days+1):
        date = FIRSTDATE + timedelta(days=i)
        dates.append(date)

    return dates

def countAppearances(code):
    # Returns minutes done of 'code' on every date since FIRSTDATE.
    datesDict = dict([(date,0) for date in allDates()])
    poms = getData.fromCode(code)
    
    for pom in poms:
        date = datetime.strptime(pom[1], "%d/%m/%Y")
        datesDict[date] = datesDict.get(date,0)+pom[4]
    
    return datesDict


def plotTimeSpentOn(code,ax):
    # plots time spent on specific activity (code).
    dates = countAppearances(code)

    x,y = [],[]
    labels = []
    for date in dates:
        x.append((date - FIRSTDATE).days)
        y.append(dates[date])
        labels.append(date.strftime("%d/%m/%Y"))

    def format_fn(tick_val, tick_pos):
        if int(tick_val) in x:
            return labels[int(tick_val)]
        else:
            return ''

    
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.plot(x,aux.cummulativeSum(y), label=code)
    


def plotCodes(limit = 99999,codes=getData.getAllCodes()):
    codes = codes[:limit]

    fig,ax = plt.subplots()

    for code in codes:
        plotTimeSpentOn(code,ax)

    plt.grid()
    plt.legend()
    plt.show()
