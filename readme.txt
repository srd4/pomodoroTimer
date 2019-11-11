This is a quick start guide for tomatotimer.

I created a function that recognizes if the directory of our database "tomatoBase.db" already exists on current working dir. In case it doesn't, executes your first pomodoro where yo have to write a brief description of what you are going to do and give it a code. Be careful, it is not yet very easy to modify information that the program wrote on database so you better think your code names right in order to have good measurement of your activities later on (although database is always updated after countdowns, so you have a few minutes to re-think your life decisions).

After the first pomdoro's countdown finishes you'll be able to see the normal main menu with information about the time you've spent on your activities (codes). There you'll give as input one of 4 numbers choosing on what to do next: if another pomodor, a short break, a long one, or quit the script.

How to change music:

You just need to get a .mp3 version of the song you want and change its name to "song" (so you have a "\song.mp3" path) and put it on this script's source code, replacing the one existing. Careful, because again, the script is not at all prepared to deal with things disappearing.

Dependencies:

Most of the code could be writen with python's standard library except for the single one that is used to reproduce the alarm song the countdown blasts when finished. You'll have to install it by yourself using pip on cmd with the comman "pip install vlc", this will probably help: https://packaging.python.org/tutorials/installing-packages/

Apart from this one, there is no other dependency that you need for running this script. So you are pretty much set up. If you want to play with the code do it carefully, make a copy of your database (you can get the code back from github, but not your information) and then proceed. I'm currently working on some implementations of datavisualization that are most likely going to be included soon. Code has plenty of commentary and I try to make use of the right words to describe functioning, in case you don't feel so, the ask.

Modules:

As you probably noticed the program is separated on different .py files. The ones that runs the script is called main.py and is the one we should run to execute our app normally. With respect to the rest, you have:

- auxiliarFunctions.py which has a few simple functions that implement things like making a coutdown iterator and printing it, or getting whitespace out of a string data type.
- tomatoRecord.py which basically handles the database, retrieving and writting information from and on it. This is the one you should be careful when playing with. From here you can delete information and access it all (knowing a couple basic sql commands).
- getdata.py which has functions for interpreting, rearranging and filtering data we get from tomatoRecord.py.
- seeData.py which for now (08/11/2019) is not in anyway combined with main.py, so in order to use its functionalities you'll have to run them by yourself on a python ide. Has functions for visualizing data.









