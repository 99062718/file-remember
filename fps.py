from audioop import reverse
import tkinter, random, json
from tkinter import messagebox, StringVar

mainWindow = tkinter.Tk()
mainWindow.geometry("900x600")

time = 20
timeText = tkinter.StringVar(mainWindow, "Time remaining: {}".format(time))
score = 0
scoreText = tkinter.StringVar(mainWindow, "Score: {}".format(score))

#---------Frames and labels

textFrame = tkinter.Frame(
    mainWindow,
    height=20,
    bg="black"
)
textFrame.pack(
    fill="x",
    side="top"
)

timeLabel = tkinter.Label(
    textFrame,
    textvariable=timeText,
    bg="black",
    anchor=tkinter.W
)
timeLabel.pack(
    fill='x', 
    side='left'
)

scoreLabel = tkinter.Label(
    textFrame,
    textvariable=scoreText,
    bg="black",
    anchor=tkinter.E
)
scoreLabel.pack(
    fill='x', 
    side='right'
)

playWindow = tkinter.Frame(
    mainWindow,
    bg="white"
)
playWindow.pack(
    expand=True,
    fill="both",
    side="top"
)

#---------Functions
def createNewBtn():
    global toPress, randNum1, randNum2, choices
    choices = [["<space>", "<w>", "<a>", "<s>", "<d>"],["<Button>", "<Double-Button>", "<Triple-Button>"]]
    randNum1 = random.randint(0, 1)
    randNum2 = random.randint(0, len(choices[randNum1]) - 1)

    toPress = tkinter.Label(
        playWindow,
        height=2,
        width=20,
        text=choices[randNum1][randNum2],
        fg="white",
        bg="red"
    )
    toPress.place(
        x=random.randint(1, 700),
        y=random.randint(1, 500)
    )

    if randNum1 == 0:
        mainWindow.bind(choices[randNum1][randNum2], destroyBtn)
    else:
        toPress.bind(choices[randNum1][randNum2], destroyBtn)

def destroyBtn(self, endOfGame="no"):
    global score
    toPress.destroy()
    if randNum1 == 0:
        mainWindow.unbind(choices[randNum1][randNum2])
        score += 1
    else:
        score += 2
    scoreText.set("Score: {}".format(score))
    if endOfGame != "yes":
        createNewBtn()

def startGame():
    createNewBtn()
    mainWindow.after(1000, timer)

def timer():
    global time
    time -= 1
    timeText.set("Time remaining: {}".format(time))
    if time != 0:
        mainWindow.after(1000, timer)
    else:
        endScreen()

def endScreen():
    global nameEntry, gameLeaderboard, btn, inLeaderBoard
    inLeaderBoard = False


    destroyBtn("", "yes")

    with open("fpsLeaderboard.json", "r") as file:
        gameLeaderboard = json.load(file)
    
    for key, value in gameLeaderboard.items():
        if value < score:
            answer = messagebox.askyesno(message="You have entered the top 10 with a score of {}! Would you like to put your score on the leaderboard?".format(score))
            if answer:
                messagebox.showinfo(message="Enter a name that will show on the leaderboard")
                answer = StringVar()
                nameEntry = tkinter.Entry(
                    playWindow,
                    textvariable=answer
                )

                nameEntry.pack(pady=150)

                btn = tkinter.Button(
                    playWindow,
                    command=lambda: validateName(answer.get())
                )

                btn.pack(pady=10)

                inLeaderBoard = True
                return
            

def playAgain():
    global btn, nameEntry
    answer = messagebox.askyesno("play again?", "Your final score is {}! \nWould you like to play again?".format(score) if score not in list(gameLeaderboard.values()) else "Play again?")
    if answer:
        if inLeaderBoard:
            btn.destroy()
            nameEntry.destroy()
        createStartButton()
    else:
        mainWindow.destroy()

def validateName(name):
    global gameLeaderboard
    if name in list(gameLeaderboard.keys()):
        messagebox.showerror(message="This name is already in use on the leaderboard!")
    else:
        gameLeaderboard[name] = score
        temp = list(gameLeaderboard.items())
        temp.sort(key=lambda a: a[1], reverse=True)
        temp.pop(10)
        temp = dict(temp)
        gameLeaderboard = temp
        with open("fpsLeaderboard.json", "w") as file:
            json.dump(gameLeaderboard, file)
        playAgain()

def deleteStartBtn():
    btn.destroy()
    startGame()

def createStartButton():
    global btn
    global score
    global time
    score = 0
    time = 20
    btn = tkinter.Button(
        playWindow,
        bg="white",
        fg="black",
        text="Click to start game",
        command=deleteStartBtn,
        height=10,
        width=30,
        justify="center"
    )
    btn.pack(
        pady=150
    )

#---------Start of program

createStartButton()

mainWindow.mainloop()