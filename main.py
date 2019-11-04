import auxiliarFunctions as aux
import tomatoRecord as tr
import threading
import winsound
import getData
import vlc
import os

currentPath = os.getcwd()+"\\"
alarmSong = vlc.MediaPlayer(currentPath+"song.mp3")

def main():
    while True:
        print(getData.infoMessage())
        print("So, what the hell you want to do now, buddy?")

        response = input("1. Pomodoro. \n2. Short Break. \n3. Long Break.\n4. Quit.\n\n> ")

        alarmSong.stop()

        if response == "1":
            description = input("Describe what you are about to do mate:\n> ")
            code = input("What's the code of this activity?\n> ")

            if getData.getPomTime(code) != 0:
                #Message with info with respect to 'code' pomodoros.
                print(getData.codeMessage(code))

            else:
                print("This is your first time working on",code)

            if aux.printCountDown(1200):
                alarmSong.play()
                tr.recordPom(description,code)
            continue

        if response == "2":
            aux.printCountDown(300)
            alarmSong.play()
            continue

        if response == "3":
            aux.printCountDown(600)
            alarmSong.play()
            continue

        if response == "4":
            quit()

        if response == "plotWeek":
            aux.plotBar(getData.getWeekPoms())
            continue

        if response == "plotToday":
            aux.plotIt(getData.pomsToday())
            continue



if __name__ == "__main__":
    if not os.path.exists(os.getcwd()+"\\tomatoBase.db"):
        tr.initiateTomatoBase()
    main()


