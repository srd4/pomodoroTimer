import tomatoRecord as tr
import getData as gd
import matplotlib.pyplot as plt
from random import randint
from datetime import datetime
import numpy as np

POMS = tr.getPoms()
FIRSTDATE = datetime.strptime(POMS[0][1], "%d/%m/%Y")

def pom_reg():
    # Creates a tuple of information about pom (coordinates) to know where to place them on array.
    reg = []

    for pom in POMS:
        hours, minutes, seconds = pom[0].split(":")
        reg.append(((int(hours) * 60) + int(minutes),
        (datetime.strptime(pom[1], "%d/%m/%Y") - FIRSTDATE).days,
        pom[-3]))
    
    return reg

colors = {
"python": [40, 91, 17],
"calculo1": [22, 33, 49],
"discretas":[221, 61, 135],
"calculo2":[230, 171, 13],
"read":[229, 115, 29],
"ipoo":[194, 50, 42],
"precalculo":[234, 67, 53]
}

def plot_image():
    image = [[[125, 125, 125] for i in range((datetime.today() - FIRSTDATE).days + 1)] for e in range(1,1441)]
    pomRegister = pom_reg()

    for reg in pomRegister:
        index = 20
        while index > -1:
            x = reg[1]
            y = reg[0] - index
            if (reg[0] - index) < 0:
                x = reg[1] - 1
                y = reg[0] - index
                
            image[y][x] = colors[reg[2]] if reg[2] in colors else [256,256,256]
            index -= 1
    
    plt.imshow(image, aspect='auto')


plot_image()
plt.show()




# Generate touple of coordinates for each pomodoro: (row/minute , column/day, color)
# row/minute = on time.
# day = total days from FIRSTDAY
# color = Acording to me.
