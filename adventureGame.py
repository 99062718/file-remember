import tkinter, random, json, os
from tkinter import ttk, IntVar, StringVar, messagebox
from tkinter.constants import OUTSIDE
from os.path import exists

mainWindow = tkinter.Tk()
mainWindow.configure(pady=30, padx=50)

damageMultiplier = 1
content = [[],[]]
isMath = False
currentBoss = []
save = False

# todo: expand on options menu with current region, cheatcodes and some other stuff (font size and font customization if able to),
# support for items (maybe)

# dicts for game data have been moved to json. look inside the adventureData folder to find it

#----------------------------------------------------------------------------------Functions game needs to work properly at the core

#-------------------------------------------Functions that create the visuals on screen

def theContentDestroyer9000(removeAll=False): # theContentDestroyer9000 is back in stock yet again. Now for 30% off for you and your family to destroy content with during the holidays!
    global content
    for box in content[0]:
        box.destroy()
    content[0] = []
    if removeAll:
        for box in content[1]:
            box.destroy()
        content[1] = []

def contentCreator(newContent=[]): # the only reason theContentDestroyer9000 still sells
    global content, playerInput, isMath
    num = [0, 0]

    theContentDestroyer9000()

    for info in newContent:

        if "currentDiff" in globals(): # checks if a save has been used
            saveGame()

        if info[0] in ("radio", "spinbox"):
            playerInput = StringVar() if info[0] == "radio" else IntVar()
        elif info[0] == "gameEnd":
            os.remove("adventureData/save.json")
            return

        for value in info[1]:
            if value == "mathActive": # checks if the math question has already been generated
                isMath = True
                continue

            gridOrPlace = "place" if value == "Options" else "grid"

            if value == "mathQuestion": # detects when to generate a math question
                value = rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["content"][newContent.index(info)][1][info[1].index("mathQuestion")] = mathQuestionCreator()
                rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["content"][newContent.index(info)][1].append("mathActive")

            if info[0] == "label": # creates label
                content[0].append(tkinter.Label(text=value))
            elif info[0] == "spinbox": # creates spinbox
                playerInput = IntVar()
                content[0].append(ttk.Spinbox(
                    from_=float("-inf"),
                    to=float("inf"),
                    textvariable=playerInput
                ))
            elif info[0] == "radio": # creates radiobutton
                content[0].append(ttk.Radiobutton(
                    text=value,
                    value=value,
                    variable=playerInput
                ))
            elif info[0] == "button": # creates button
                functionToUse = value

                content[1 if gridOrPlace == "place" else 0].append(tkinter.Button(
                    text=value,
                    command = lambda toUse = functionToUse : funcExecute(toUse)
                ))
            else: # throws exception if given widget type is not supported by the program
                raise Exception("{} is not a valid widget type".format(info[0]))

            if gridOrPlace == "place":
                content[1][num[1]].place(bordermode=OUTSIDE, anchor="nw")
                num[1] += 1
            else:
                content[0][num[0]].grid(row=num[0])
                num[0] += 1

#-------------------------------------------Room creation

def nextRoom(): # calculates what the next room and its properties are
    global currentRegion, isMath, currentBoss
    goto = False
    
    playerAnswer = mathAnswerCheck(playerInput.get()) if isMath else playerInput.get()

    if playerAnswer == "":
        messagebox.showerror(message="Please enter something here")
        return

    if "optional" in list(rooms[currentCharacter][currentRegion[0]][currentRegion[1]].keys()):
        if "doDamageWhen" in list(rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"].keys()):
            if playerAnswer in rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"]["doDamageWhen"]:
                healthCheck(rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"]["deathMessage"])
                if health <= 0:
                    return

        if "boss" in list(rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"].keys()):
            currentBoss = rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"]["boss"]
            currentBoss.append(True)

    try:
        if currentBoss[3]:
            if playerAnswer in rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["optional"]["doDamageToBossWhen"]:
                currentBoss[2] -= playerAttack * damageMultiplier

            if currentBoss[2] <= 0:
                currentRegion = [currentBoss[0], currentBoss[1]]
                currentBoss[3] = False
                return roomGen()
    except:
        pass


    if "goTo" in list(rooms[currentCharacter][currentRegion[0]][currentRegion[1]].keys()):
        for currentGoTo in rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["goTo"]:
            if playerAnswer in currentGoTo or len(currentGoTo) == 2:
                currentRegion = [currentGoTo[0], currentGoTo[1]]
                goto = True
                break
    if goto == False:
        currentRegion[1] += 1

    isMath = False
    return roomGen()

def roomGen():
    contentCreator(rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["content"])

#-------------------------------------------Save data

def pastSaveDetected(): # loads save if player chooses to
    global currentCharacter, currentRegion, currentBoss, health, playerAttack, damageMultiplier, save

    if playerInput.get() == "Yes":
        with open("adventureData/save.json", "r") as file:
            saveData = json.load(file)

            currentCharacter = saveData["currentCharacter"]
            currentRegion = saveData["currentRegion"]
            currentBoss = saveData["currentBoss"]
            health = saveData["health"]
            playerAttack = saveData["playerAttack"]
            damageMultiplier = saveData["damageMultiplier"]
            save = True
            diffSubmit(saveData["currentDiff"])
    elif playerInput.get() == "No":
        chooseCharacter()

def saveGame(): # saves game
    with open("adventureData/save.json", "w") as file:
        saveData = {
            "currentCharacter":currentCharacter,
            "currentRegion":currentRegion,
            "currentBoss":currentBoss,
            "health":health,
            "playerAttack":playerAttack,
            "damageMultiplier":damageMultiplier,
            "save": True,
            "currentDiff":currentDiff
        }
        json.dump(saveData, file)

#-------------------------------------------Battle system related

def mathQuestionCreator(): #makes math questions by choosing an operator based on a random number
    global isAlternate, currentAnswer, higherOrLower, isMath
    randomNumber = random.randint(1, numberOfOperators)
    isAlternate = True
    isMath = True

    if randomNumber not in [3, 4]:
        isAlternate = False
    
    if randomNumber == 1 or randomNumber == 2: # +-
        randomNumber2 = random.randint(1, additionSubtractionNumber)
        randomNumber3 = random.randint(1, additionSubtractionNumber)
        currentAnswer = randomNumber2 + randomNumber3 if randomNumber == 1 else randomNumber2 - randomNumber3
        return "What is {} + {}?".format(randomNumber2, randomNumber3) if randomNumber == 1 else "What is {} - {}?".format(randomNumber2, randomNumber3)
    elif randomNumber == 3 or randomNumber == 4: # ><
        randomNumber2 = random.randint(1, additionSubtractionNumber)
        currentAnswer = randomNumber2
        higherOrLower = "higher" if randomNumber == 3 else "lower"
        return "Name a number higher than {}".format(randomNumber2) if randomNumber == 3 else "Name a number lower than {}".format(randomNumber2)
    elif randomNumber == 5: # *
        randomNumber2 = random.randint(1, multiplicationNumber)
        randomNumber3 = random.randint(1, multiplicationNumber)
        currentAnswer = randomNumber2 * randomNumber3
        return "What is {} * {}?".format(randomNumber2, randomNumber3)

def mathAnswerCheck(input): # returns true or false based on if the math question is correct or not

    if isAlternate == False and currentAnswer == input:
        return "True"
    elif isAlternate == True:
        if input > currentAnswer and higherOrLower == "higher":
            return "True"
        elif input < currentAnswer and higherOrLower == "lower":
            return "True"
    return "False"

def healthCheck(deathMessage=""): # if player get hit. player get hurt. if player doesnt have health left. player die
    global health

    health -= damageToPlayer

    if health <= 0: # displays death message
        theContentDestroyer9000(True)
        contentCreator([["label", [deathMessage, "Game over!"]]])

#----------------------------------------------------------------------------------Extra functions

#-------------------------------------------Character and difficulty selects

def characterSubmit(): #sets all stats for character once chosen and sends them to first room of their respective story
    global currentCharacter, currentRegion, health, playerAttack
    currentCharacter = playerInput.get()

    if currentCharacter in list(characters.keys()):
        health = characters[currentCharacter]["maxHealth"]
        playerAttack = characters[currentCharacter]["attack"]
        currentRegion = [list(rooms[currentCharacter].keys())[0], 0]

        contentCreator([["label", ["Select a difficulty"]], ["radio", list(difficulties.keys())], ["button", ["Choose difficulty"]]])
    else:
        messagebox.showerror(message="Please select a character!")

def chooseCharacter(): # creates GUI for characterSubmit
    contentCreator([["label", ["Choose a character"]], ["radio", list(characters.keys())], ["button", ["Choose character"]]])

def diffSubmit(diffDefined=False): # selects a difficulty. if a save has been found the function will automatically use that diff
    global numberOfOperators, additionSubtractionNumber, multiplicationNumber, damageToPlayer, currentDiff

    if diffDefined == False:
        currentDiff = playerInput.get()
    else:
        currentDiff = diffDefined

    if currentDiff in list(difficulties.keys()):
        numberOfOperators = difficulties[currentDiff][0]
        additionSubtractionNumber = difficulties[currentDiff][1]
        multiplicationNumber = difficulties[currentDiff][2]
        damageToPlayer = difficulties[currentDiff][3] if difficulties[currentDiff][3] != "max" else health

        contentCreator([["button", ["Options"]]])
        if save == False:
            contentCreator(rooms[currentCharacter][list(rooms[currentCharacter].keys())[0]][0]["content"])
        else:
            roomGen()

#-------------------------------------------Button functionality and options menu

def funcExecute(functionToUse): #executes whatever function we put into it. useful for dynamically creating buttons
    if functionToUse in list(functionList.keys()):
        functionList[functionToUse]()

class optionMenu: #everything related to the options menu
    def options():
        theContentDestroyer9000(True)
        contentCreator([["button", ["Region", "Cheatcodes", "Exit"]]])

    def showRegion():
        messagebox.showinfo(message="Your current region is: {}".format(currentRegion[0]))

    def exitMenu():
        contentCreator([["button", ["Options"]]])
        contentCreator(rooms[currentCharacter][currentRegion[0]][currentRegion[1]]["content"])

functionList = {
    "Options": optionMenu.options,
    "Region": optionMenu.showRegion,
    "Exit": optionMenu.exitMenu,
    "Choose character": characterSubmit,
    "Choose difficulty": diffSubmit,
    "Submit": nextRoom,
    "Start game": pastSaveDetected
}

#----------------------------------------------------------------------------------Start of game

with open("adventureData/gameData.json", "r") as file:
    gameData = json.load(file)

    rooms = gameData["rooms"]
    characters = gameData["characters"]
    difficulties = gameData["difficulties"]

if exists("adventureData/save.json"):
    contentCreator([["label", ["A past save has been detected!", "Would you like to continue this save?"]], ["radio", ["Yes", "No"]], ["button", ["Start game"]]])
else:
    chooseCharacter()

mainWindow.mainloop()