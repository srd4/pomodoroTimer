import auxiliarFunctions as aux
import sqlite3
import time

def getPoms():
    # Retrieves all pom information from database.
    # Returns list of tuples.
    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from poms")
    poms = cursor.fetchall()
    connection.close()

    return poms


def getEvery(column):
    # Returns whole column data.
    poms = getPoms()
    d = dict({"time":0,"date":1,"description":2,"code":3,"duration":4,"id":5})
    return [pom[d[column]] for pom in poms]


def getPomsBy(column, cell):
    # Retrieves poms, filters by column and cell content.
    d = dict({"time":0,"date":1,"description":2,"code":3,"duration":4,"id":5})
    poms = getPoms()
    return [pom for pom in poms if pom[d[column]] == cell]


def recordPom(description,code):
    # Inserts new pomodoro into database.
    pomData = (time.strftime("%H:%M:%S"),time.strftime("%d/%m/%Y"),description,code,"20",len(getPoms()))

    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO poms VALUES (?,?,?,?,?,?)",pomData)

    connection.commit()
    connection.close()

    return True


def deleteById(id):
    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()

    sql_command = "DELETE FROM poms WHERE id = ?"
    
    print("You are about to delete", getPomsBy("id",id)[0])
    
    if input("\nAre you sure?\n> ") == "yes":
        print("Row is about to be deleted: ")
        aux.printCountDown(7)
        cursor.execute(sql_command,(id,))
        print("Done!")

    connection.commit()
    connection.close()

    return True


def updateById(id, column, value):
    # Updates row information where id is found.
    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()
    sql_command = "UPDATE poms SET {} = {} WHERE id = {}".format(column, value, id)

    cursor.execute(sql_command)

    connection.commit()
    connection.close()

    return True


def find(inTable, column, cell):
    # Finds rows inTable' with matching cell' on a column'. Returns list.
    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()
    sql_command = "SELECT * FROM {} WHERE  {} = {}".format(inTable, column, cell)

    cursor.execute(sql_command)

    poms = cursor.fetchall()
    connection.close()

    return poms


def match(string):
    # Returns list of pomodoros that on some column match string.
    return [pom for pom in getPoms()[::-1] if string in str(pom)]


def initiateTomatoBase():
    # Creates tomatoBase.db file and poms table.
    connection = sqlite3.connect("tomatoBase.db")
    cursor = connection.cursor()

    sql_command = "CREATE TABLE poms (time text, date text, description text, code text, duration INT, id INT);"

    cursor.execute(sql_command)

    connection.commit()
    connection.close()

    return True