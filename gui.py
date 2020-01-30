import tkinter as tk
import getData as gd
import tomatoRecord as tr
import time
from auxiliarFunctions import timeFormat
import os
import vlc
from tkinter import Grid,N,S,E,W

currentPath = os.getcwd()+"\\"
alarmSong = vlc.MediaPlayer(currentPath+"song.mp3")

WIDTH = 300
HEIGHT = 400

FRAME_BG_COLOR = "#ff8a85"
GREEN = "#008650"
RED = "#c82922"
FONT = "consolas"

#This class is mainly to automate the process of making frames, they are all under the three main menu tabs.
class pageFrame(tk.Frame):
    def __init__(self, *ags, **kwargs):
        tk.Frame.__init__(self, *ags, **kwargs, bg=FRAME_BG_COLOR)

        self.place(relx=0, rely=0.08, relwidth=1, relheight=1)


master = tk.Tk()

canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT)
canvas.pack()

#Menu bar container wich would have three buttons created below in it.
menuFrame = tk.Frame(master)
menuFrame.place(relwidth=1, relheight=0.08)

#   Button 1. Takes to respective page.
allButton = tk.Button(menuFrame, text="All", command=lambda :all_update(),
bg=RED, font=(FONT, 16), fg="white", relief="flat")
allButton.place(relx=0, relwidth=1/3, relheight=1)

#   Button 2. "
todayButton = tk.Button(menuFrame, text="Today", command=lambda :today_update(),
bg=RED, font=(FONT, 16), fg="white", relief="flat")
todayButton.place(relx=1/3, relwidth=1/3, relheight=1)

#   Button 3. "
recordButton = tk.Button(menuFrame, text="Record", command=lambda :record_update(),
bg=RED, font=(FONT, 16), fg="white", relief="flat")
recordButton.place(relx=2/3, relwidth=1/3, relheight=1)

mostRecentFrame = pageFrame(master)

mostRecentTable = tk.Frame(mostRecentFrame, bg=FRAME_BG_COLOR)
mostRecentTable.place(relx=1/2, rely=1/6, anchor="n")

def mostRecent_Frame():
    mostRecentFrame.tkraise()
    mostRecentTable.tkraise()

    codes = gd.getAllCodes()
    codes.sort(key=lambda code: gd.longAgo(code).total_seconds())

    label1 = tk.Label(mostRecentFrame, text="Recently done", bg=FRAME_BG_COLOR, font=(FONT, 28), fg="white")
    label1.place(relx=1/2, anchor="n")


    label1 = tk.Label(mostRecentTable, text="Code", bg=FRAME_BG_COLOR, font=(FONT, 14), fg="white")
    label1.grid(row=0, column=0, sticky="W")

    label2 = tk.Label(mostRecentTable, text="Long ago",bg=FRAME_BG_COLOR, font=(FONT, 14), fg="white")
    label2.grid(row=0, column=1, sticky="E")


    index = 1
    for code in codes[:10]:
        since = timeFormat(gd.longAgo(code).total_seconds())
        label1 = tk.Label(mostRecentTable, text=code+":", bg=FRAME_BG_COLOR, font=(FONT, 12), fg="white")
        label1.grid(row=index, column=0, sticky="W")

        label2 = tk.Label(mostRecentTable, text=since if since[0] != "0" else since[-8:],bg=FRAME_BG_COLOR, font=(FONT, 12), fg="white")
        label2.grid(row=index, column=1, sticky="E")

        index += 1


def week_frame(weekIndex):
    weekFrame = pageFrame(master)

    weekTable = tk.Frame(weekFrame, bg=FRAME_BG_COLOR)
    weekTable.place(relx=1/2, rely=1/6, anchor="n", relwidth=1/2, relheight=1)

    title = tk.Label(weekFrame, text="Week Balance", bg=FRAME_BG_COLOR, font=(FONT, 28), fg="white")
    title.place(relx=1/2, anchor="n")

    week = gd.getWeek(weekIndex)
    daysOfWeek = ["#","Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    previousButton = tk.Button(weekFrame, bg=GREEN, text="PREVIOUS", font=(FONT, 16), fg="white",
    relief="flat", command= lambda : week_frame(weekIndex - 1))
    previousButton.place(relx=1/2, rely=3/4, relwidth=1/12, anchor="e", relheight=1/24)

    nextButton = tk.Button(weekFrame, bg=GREEN, text="NEXT", font=(FONT, 16), fg="white",
    relief="flat", command= lambda : week_frame(weekIndex + 1))
    nextButton.place(relx=1/2, rely=3/4, relwidth=1/24, anchor="w", relheight=1/24)


    for day in daysOfWeek:
        label1 = tk.Label(weekTable, text=day, bg=FRAME_BG_COLOR, font=(FONT, 12), fg="white")
        label1.grid(row=0, column=daysOfWeek.index(day), sticky="W")


    for i in range(1,37):
        label1 = tk.Label(weekTable, text=str(i), bg=FRAME_BG_COLOR, font=(FONT, 12), fg="white")
        label1.grid(row=i, column=0, sticky="W")

    for x in range(60):
        Grid.columnconfigure(weekTable, x, weight=1)

    for y in range(60):
        Grid.rowconfigure(weekTable, y, weight=1)

    for day in week:
        for pom in day[1]:
            label1 = tk.Label(weekTable, text=pom[3], bg=FRAME_BG_COLOR, font=(FONT, 12), fg="white")
            label1.grid(row=day[1].index(pom) + 1, column=day[0].weekday() + 1, sticky="W")
    


class statsViewer:
    def __init__(self):
        self.selected = None
        self.items = ["Most recent", "Week balance"]

    def select(self, event):
        # Assigns listbox selection.
        w = event.widget
        index = int(w.curselection()[0])
        self.selected = index
    
    def see(self):
        # Executed when see button is pressed.
        if(self.selected == 0):
            #Supposted to run the function that'll show 'most recent' frame.
            mostRecent_Frame()
        elif self.selected == 1:
            week_frame(-1)
    

#First page "All".
allFrame = pageFrame(master)

statsFrame = pageFrame(master)

stats = statsViewer()

def stats_frame():
    statsFrame.tkraise()

    optionsBox = tk.Listbox(statsFrame)
    optionsBox.place(relx=1/2, rely=1/6, anchor="n", relwidth=2/3, relheight=1/2)

    statsLabel = tk.Label(statsFrame, text="STATS", bg=FRAME_BG_COLOR, fg="white", font=(FONT, 28))
    statsLabel.place(relx=1/2, rely=1/36, anchor="n")

    seeButton = tk.Button(statsFrame, bg=GREEN, text="SEE", font=(FONT, 16), fg="white",
    relief="flat", command= lambda : stats.see())
    seeButton.place(relx=1/2, rely=3/4, relwidth=0.8, anchor="n")

    optionsBox.bind('<<ListboxSelect>>', stats.select)

    index = 0
    for item in stats.items:
        optionsBox.insert(index, item)
        index += 1



def all_update():
    allFrame.tkraise()
    #   Done today table.
    dataTable = tk.Frame(allFrame, bg=FRAME_BG_COLOR)
    dataTable.place(relx=1/2, rely=1/20, width=43/60 * WIDTH, relheight=1/2, anchor="n")

    titles = ("dummy","Total", "Hours", "Like", "Average", "Days ago")

    index = 1
    for i in gd.getInfo()[:-1]:
        label1 = tk.Label(dataTable, text=titles[index]+":", bg=FRAME_BG_COLOR, font=(FONT, 16), fg="white")
        label1.grid(row=index, column=0, sticky="W")

        label2 = tk.Label(dataTable, text=i, bg=FRAME_BG_COLOR, font=(FONT, 16), fg="white")
        label2.grid(row=index, column=1, sticky="E")

        label1.grid_columnconfigure(0, weight=10)
        label2.grid_columnconfigure(1, weight=10)

        index += 1


    #   "Start New" button.
    more = tk.Button(allFrame, bg=GREEN, font=(FONT, 16), fg="white",
    relief="flat", text= "MORE", command= lambda : stats_frame())
    more.place(relx=0.25, rely=3/5, relwidth=0.5, relheight=1/5)




def today_update():

    #Second page 'today'.
    todayFrame = pageFrame(master)

    #   Done today table.
    doneToday = tk.Frame(todayFrame, bg=FRAME_BG_COLOR)
    doneToday.place(relx=1/2, rely=1/20, width=3/4 * WIDTH, relheight=1/2, anchor="n")

    codel = tk.Label(doneToday, text="CODE", bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
    codel.grid(row=0, column=0, sticky="W")

    minutesl = tk.Label(doneToday, text="MINUTES", bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
    minutesl.grid(row=0, column=1)

    poms = gd.pomsToday()

    index = 1
    for key in poms:
        label1 = tk.Label(doneToday, text=key, bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
        label1.grid(row=index, column=0, sticky="W")

        label2 = tk.Label(doneToday, text=str(poms[key]), bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
        label2.grid(row=index, column=1)

        label1.grid_columnconfigure(0, weight=10)
        label2.grid_columnconfigure(1, weight=10)

        index += 1


    #   "Start New" button.
    new = tk.Button(todayFrame, bg=GREEN, font=(FONT, 16), fg="white",
    relief="flat", text= "NEW", command=lambda :new_pom())
    new.place(relx=0.25, rely=3/5, relwidth=0.5, relheight=1/5)




def searchPoms():
    #Called from searchButton's command. Searches for pomodoros that match entry and updates listbox.
    pomsList.delete(0, pomsList.size() - 1)
    poms = tr.match(searchEntry.get())

    if(searchEntry.get() == ""):
        index = 0
        for pom in tr.getPoms()[::-1]:
            pomsList.insert(index, str(index) + " - " + str(pom))
            index += 1
    else:
        index = 0
        for pom in poms:
            pomsList.insert(index, str(index) + " - " + str(pom))
            index += 1
    
    return poms



class PomEdit:
    def __init___(self):
        self.pom = None

    def asignPom(self, evt):

        w = evt.widget
        index = int(w.curselection()[0])
        poms = tr.match(searchEntry.get())
        print(index, poms[index])
        self.pom = poms[index]
        
        
    def editPom(self):
        #Edits selected pom.
        try:
            edit_pom(self.pom)
        except:
            pass

#Pom edit object, to store data on selected pom and wait until button is pressed.
pomEdit = PomEdit()

#Tomato history frame.
recordFrame = pageFrame(master)

pomsList = tk.Listbox(recordFrame)

scrollbar = tk.Scrollbar(recordFrame, orient="vertical")
scrollbar.config(command=pomsList.yview)

searchEntry = tk.Entry(recordFrame)

searchButton = tk.Button(recordFrame, bg=GREEN, text="SEARCH", font=(FONT, 16), fg="white",
relief="flat", command=lambda: searchPoms())

tomatoLabel = tk.Label(recordFrame, text="Tomato History", bg=FRAME_BG_COLOR, font=(FONT, 28), fg="white")

editButton = tk.Button(recordFrame, bg=GREEN, text="EDIT", font=(FONT, 16), fg="white",
relief="flat", command=lambda: pomEdit.editPom())



def record_update():
    #Third page 'record'.
    recordFrame.tkraise()
    searchPoms()
    pomsList.place(relx=1/2, rely=1/3, relwidth=4/5, relheight=41/90, anchor="n")
    scrollbar.place(relx=(9/10), rely=1/3, relheight=41/90, anchor="ne")
    searchEntry.place(relx=1/2, rely=31/180, relwidth=4/5, anchor="n")
    tomatoLabel.place(relx=1/2, rely=1/45, relwidth=1, anchor="n")
    searchButton.place(relx=0.5, rely=(1/5)+(1/25), relwidth=0.8, relheight = 3/40, anchor="n")

    
    editButton.place(relx=0.5, rely=(4/5), relwidth=0.8, relheight = 3/40, anchor="n")

    pomsList.bind('<<ListboxSelect>>', pomEdit.asignPom)



#Edit pom frame.
editFrame = pageFrame(master)



def edit_pom(pom):
    #Edit frame set up.
    editFrame.tkraise()
    IdLabel = tk.Label(editFrame, text=str("Editing "+str(pom[-1])), bg=FRAME_BG_COLOR, font=(FONT, 28), fg="white")
    IdLabel.place(relx=1/2, rely=1/45, relwidth=1, anchor="n")

    dataFrame = tk.Frame(editFrame, bg=FRAME_BG_COLOR)
    dataFrame.place(relx=1/2, rely=(1/20)+(1/6), width=WIDTH, relheight=1/2, anchor="n")

    titles = ["Time","Date","Description","Code","Minutes"]


    backButton = tk.Button(editFrame, bg=RED, text="Delete", font=(FONT, 12), fg="white", relief="flat", command=lambda: tr.deleteById(pom[-1]))
    backButton.place(relx=1/2, rely=1/7, relwidth=3/10, anchor="n", relheight = 1/20)


    descriptionEntry = tk.Entry(dataFrame)
    descriptionEntry.grid(row=2, column=1, sticky="E")
    descriptionEntry.insert(0, pom[2])

    codeEntry = tk.Entry(dataFrame)
    codeEntry.grid(row=3, column=1, sticky="E")
    codeEntry.insert(0, pom[3])

    index = 0
    for i in pom:
        if index == 5:
            break

        label1 = tk.Label(dataFrame, text=titles[index]+":", bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
        label1.grid(row=index, column=0, sticky="W")

        if not (titles[index] == "Code" or titles[index] == "Description"):
            label2 = tk.Label(dataFrame, text=i, bg=FRAME_BG_COLOR, font=(FONT, 18), fg="white")
            label2.grid(row=index, column=1, sticky="E")
        
        index += 1

    def savePom():
        # Update pom information.
        code = "'"+codeEntry.get()+"'"
        description = "'"+descriptionEntry.get()+"'"
        
        tr.updateById(pom[-1], "code", code)
        tr.updateById(pom[-1], "description", description)

    saveButton = tk.Button(editFrame, text="SAVE", command=lambda : savePom(), bg=GREEN, font=(FONT, 16), fg="white", relief="flat")
    saveButton.place(relx=0.5, rely=2/3, relwidth=1/2, relheight=1/5, anchor="n")


def new_pom():
    #Organizes new pom frames in original order.
    pomFrame.tkraise()
    selectionFrame.tkraise()
    menuFrame.tkraise()

#Fourth page, called from todayframe, here starts new pom procedure.
pomFrame = pageFrame(master)


#   Frame for setting up new pomodoro.
newPom_setup = pageFrame(pomFrame)

descriptionLabel = tk.Label(newPom_setup, text="Description:", bg=FRAME_BG_COLOR, font=(FONT, 16))
descriptionLabel.place(relx=0.5, relwidth=1/2, relheight=1/10, anchor="n")


descriptionEntry = tk.Entry(newPom_setup, width=50)
descriptionEntry.insert(0, "")
descriptionEntry.place(relx=0.5, rely=1/10, relwidth=0.8, anchor="n")




#Countdown timer's page.
timerFrame = pageFrame(master)


class Timer():
    def __init__(self):
        self.on = False
        self.seconds = 99999
        self.Label = tk.Label(timerFrame, bg=FRAME_BG_COLOR, fg="white", font=("Consolas 64"))
        self.Label.place(relx=1/2, rely=0, relwidth=1, relheight=1/2, anchor="n")
        self.job = None
        self.extra = None
        self.code = None
        self.description = None
        self.veryfier = []

    def refresh_label(self):
        """ refresh the content of the label every second """
        if(not self.on):
            try:
                self.Label.after_cancel(self.job)
            except:
                pass

        elif(self.seconds > 0):
            self.seconds -= 1
            self.Label.configure(text=timeFormat(self.seconds)[-5:])
            self.veryfier.append(1)
            self.job = self.Label.after(1000, self.refresh_label)
        else:
            alarmSong.play()
            self.stop()

    def start(self, seconds):
        timerFrame.tkraise()
        if(not self.on):
            alarmSong.stop()
            timerFrame.tkraise()
            self.seconds = seconds
            self.on = True
            self.refresh_label()

    def stop(self):
        self.on = False
        time.sleep(1/2)
        new_pom()

        if(self.extra != None):
            self.extra.place_forget()

            if(sum(self.veryfier) >= 20*60):#Checks if every minute was passed through.
                tr.recordPom(self.description, self.code)

            self.__init__()
        
        
timer = Timer()

stop = tk.Button(timerFrame, bg=RED, font=(FONT, 16), fg="white",
relief="flat", text= "STOP", command=lambda :timer.stop())
stop.place(relx=0.25, rely=1/2, relwidth=0.5, relheight=1/5)


#When pressed "New code" on new pom frame.
newCodeFrame = pageFrame(newPom_setup)
newCodeFrame.place(relx=0.25, rely=7/20, relwidth=0.5, relheight=7/20)

newCodeEntry = tk.Entry(newCodeFrame, width=10)
newCodeEntry.place(relx=0.5, rely=3/10, relwidth=0.8, anchor="n")


#Regular code frame.
codeFrame = pageFrame(newPom_setup)
codeFrame.place(relx=0.25, rely=17/60, relwidth=0.5, relheight=0.5)

#   Code Label
codeLabel = tk.Label(codeFrame, text="Code:", bg=FRAME_BG_COLOR, font=(FONT, 16))
codeLabel.place(relx=0.5, rely=0, relwidth=1/2, relheight=1/10, anchor="n")



def startWithNewCode():
    if(len(descriptionEntry.get()) < 10):
        descriptionLabel.configure(fg="red")
        return
    if(len(newCodeEntry.get()) < 4):
        codeLabel.configure(fg="red")
        return

        
    prompt = tk.Label(timerFrame, text="First time working on {}".format(newCodeEntry.get()), font=(FONT, 12),
    bg=FRAME_BG_COLOR, wraplength=WIDTH, fg="white")

    timer.code = newCodeEntry.get()
    timer.description = descriptionEntry.get()
    timerFrame.tkraise()
    prompt.place(relx=1/2, rely=2/5, relwidth=1, relheight=1/3, anchor="n")
    timer.extra = prompt
    timer.start(1201)

def back():
    #Restorer new pom frame start status.
    newCodeFrame.place_forget()


startButton = tk.Button(newCodeFrame, bg=GREEN, text="START", font=(FONT, 16), fg="white",
relief="flat", command=lambda: startWithNewCode())
startButton.place(relx=0.5, rely=5/10, relwidth=0.8, anchor="n")

#For turning back from new code "entry" setup.
backButton = tk.Button(newCodeFrame, bg=RED, text="BACK", font=(FONT, 12), fg="white",
relief="flat", command=lambda: back())
backButton.place(relx=1/2, rely=49/60, relwidth=3/10, anchor="n", relheight = 3/20)



#   List of code options.
codeOptions = tk.Listbox(codeFrame)
codeOptions.place(relx=0.5, rely=1/5, relwidth=0.8, relheight=3/5, anchor="n")

codeOptions.insert(0, "NEW CODE")

index = 1
for code in gd.getAllCodes():
    codeOptions.insert(index, code)
    index += 1


def codeSelection(evt):
    #When code gets selecten on listbox.
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    if(value == "NEW CODE"):
        newCodeFrame.place(relx=0.25, rely=7/20, relwidth=0.5, relheight=7/20)
        newCodeEntry.place(relx=0.5, rely=3/10, relwidth=0.8, anchor="n")
        newCodeFrame.tkraise()
        return
    else:
        if(len(descriptionEntry.get()) < 10):
            descriptionLabel.configure(fg="red")
            return

        prompt = tk.Label(timerFrame, text=gd.codeMessage(value), font=(FONT, 12),
        bg=FRAME_BG_COLOR, wraplength=WIDTH, fg="white")
        timer.code = value
        timer.description = descriptionEntry.get()
        timerFrame.tkraise()
        prompt.place(relx=1/2, rely=2/5, relwidth=1, relheight=1/3, anchor="n")
        timer.extra = prompt
        timer.start(1201)
        

codeOptions.bind('<<ListboxSelect>>', codeSelection)


#   Selection frame, from where three buttons would lead to further actions.
selectionFrame = pageFrame(pomFrame)


def newPomButtonEvent():
    timer.stop()
    newPom_setup.tkraise()
    alarmSong.stop()


#   Three buttons:
newPomButton = tk.Button(selectionFrame, text="POMODORO", command=lambda : newPomButtonEvent(),
bg=GREEN, font=(FONT, 16), fg="white", relief="flat")
newPomButton.place(relx=0.5, rely=1/5, relwidth=1/2, relheight=1/10, anchor="n")

break1Button = tk.Button(selectionFrame, text="BREAK", command=lambda :timer.start(301),
bg=GREEN, font=(FONT, 16), fg="white", relief="flat")
break1Button.place(relx=0.5, rely=7/20, relwidth=1/2, relheight=1/10, anchor="n")

break2Button = tk.Button(selectionFrame, text="LONG BREAK", command=lambda :timer.start(601),
bg=GREEN, font=(FONT, 16), fg="white", relief="flat")
break2Button.place(relx=0.5, rely=1/2, relwidth=1/2, relheight=1/10, anchor="n")


new_pom()

master.mainloop()