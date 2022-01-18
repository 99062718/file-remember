import random, json
from datetime import datetime

choice = "ja"
namen = []
namen2 = []
filename = "Data/{}.json".format(datetime.timestamp(datetime.now()))

with open(filename, "x"):
    pass

def printToJson(text):
    with open(filename, "a") as file:
        file.write(text)

while choice != "nee":
    naam = input("Vul hier een unieke naam in:\n").lower()
    if naam not in namen:
        namen.append(naam)
        namen2.append(naam)
    else:
        print("Deze naam heeft u al gebruikt!")

    if len(namen) > 2:
        choice = input("Wilt u nog een naam invullen (ja/nee)?\n").lower()

while namen:
    naam1 = namen[random.randint(0, len(namen) - 1)]
    naam2 = namen2[random.randint(0, len(namen2) - 1)]

    if naam1 == naam2:
        if len(namen) == 1:
            printToJson(naam1 + " is alleen :(\n")
            print(naam1 + " is alleen :(")
            exit()
    else:
        printToJson(naam1 + " heeft " + naam2 + " als lootje!\n")
        print(naam1 + " heeft " + naam2 + " als lootje!")
        namen.remove(naam1)
        namen2.remove(naam2)