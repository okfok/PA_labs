from tkinter import *
import ai
import game

boardWidth = 400
boardHeight = 400
ncols = 5
nrows = 5
cellWidth = boardWidth / ncols
cellHeight = boardHeight / nrows

COLOR = 'grey'
COLOR1 = 'blue'
COLOR2 = 'red'
BGCOLOR = 'dark grey'

depth = 3

state = game.boardGame([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
], 1, 8)

ai = ai.TeekoAI(state, -1)


class Interface():
    def __init__(self):

        # Game parameters
        self.mode = 0
        self.difficulty = 1

        # Main UI
        self.window = Tk()
        self.window.title("Teeko Game")

        self.frame = Frame(self.window)
        self.frame.config(background=BGCOLOR)

        self.playButton = Button(self.frame, text="Play", font=("Courrier", 25), bg=BGCOLOR,
                                 command=lambda: [self.window.withdraw(), self.openPlayConfig()])
        self.playButton.pack(pady=20, fill=X)

        self.quitButton = Button(self.frame, text="Quit", font=("Courrier", 25), bg=BGCOLOR, command=self.window.quit)
        self.quitButton.pack(pady=20, fill=X)

        self.frame.pack(expand=YES)

        self.window.geometry('600x400')
        self.window.minsize(600, 400)
        self.window.config(background=BGCOLOR)
        self.center_window(self.window, 600, 400)

        self.window.mainloop()

    def center_window(self, wind, w, h):
        ws = wind.winfo_screenwidth()
        hs = wind.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        wind.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def changeMode(self, i):
        self.mode = 1 if i == 1 else 0
        modeText = "PvP" if self.mode == 0 else "PvE"
        self.modeLabel.config(text="Mode selected : " + modeText)

    def changeDifficulty(self, i):
        self.difficulty = i

    def drawCell(self, canvas, x, y, s):
        x1 = cellWidth * x
        y1 = cellHeight * y
        x2 = x1 + cellWidth
        y2 = y1 + cellHeight

        if (s == 1):
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR1, activefill=COLOR)
        elif (s == -1):
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR2, activefill=COLOR)
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', activefill=COLOR)

        self.canvas.bind('<Button-1>', self.onClick)

    def drawBoard(self, canvas, state):

        for i in range(5):
            for j in range(5):
                s = state.board[i][j]
                self.drawCell(self.canvas, j, i, s)

    def openPlayConfig(self):
        self.playConfig = Tk()
        self.playConfig.title("Game configuration")

        frame = Frame(self.playConfig)
        frame.config(background=BGCOLOR)

        # Difficulty slider
        difficultyLabel = Label(frame, text="Choose your difficulty level:", font=("Courrier", 15), bg=BGCOLOR,
                                fg="White")
        difficultyLabel.pack()
        self.selector = Scale(frame, from_=1, to=3, orient=HORIZONTAL, bg=BGCOLOR, fg="White")
        self.selector.pack(expand=YES, pady=10, fill=X)

        # Mode buttons
        pvpButton = Button(frame, text="PvP", bg=BGCOLOR, command=lambda: self.changeMode(0))
        pvaiButton = Button(frame, text="PvE", bg=BGCOLOR, command=lambda: self.changeMode(1))
        pvpButton.pack(expand=YES, side='left', pady=20, fill=X)
        pvaiButton.pack(expand=YES, side='left', pady=20, fill=X)

        frame.pack(expand=YES)

        self.modeLabel = Label(self.playConfig, text="Mode selected : PvP", font=("Courrier, 20"), fg="White",
                               bg=BGCOLOR)
        self.modeLabel.pack(expand=YES)

        # Back button
        popupButton = Button(self.playConfig, text="Back", font=("Courrier, 20"),
                             command=lambda: [self.playConfig.withdraw(), self.window.deiconify()], bg=BGCOLOR)
        popupButton.pack(side="bottom", pady=20)

        # Launch game button
        launchGameButton = Button(self.playConfig, text='Launch Game', font=("Courrier, 20"),
                                  command=lambda: [self.playConfig.withdraw(), self.openGameWindow(),
                                                   self.changeDifficulty(self.selector.get())], bg=BGCOLOR)
        launchGameButton.pack(side="bottom", pady=20)

        # Window parameters
        self.playConfig.minsize(1200, 400)
        self.playConfig.configure(bg=BGCOLOR)
        self.center_window(self.playConfig, 1200, 300)

    def openGameWindow(self):
        self.gameWindow = Tk()
        self.gameWindow.title("Playing game...")

        self.gameFinished = False

        board = Frame(self.gameWindow)
        board.config(background=BGCOLOR)

        # Previously selected pawn
        self.selectedPawnX = None
        self.selectedPawnY = None

        # Game Label
        playerValue = 1 if state.playerPlaying == 1 else 2
        self.gameLabel = Label(self.gameWindow, text="Player " + str(playerValue) + "'s turn:", font=("Courrier", 40),
                               bg=BGCOLOR, fg="White")
        self.gameLabel.pack(pady=(100, 20))

        self.canvas = Canvas(board, width=boardWidth, height=boardHeight, bd=1, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        board.pack(expand=YES)

        # initialize the game board
        self.drawBoard(self.canvas, state)

        # Quit game button
        quitButton = Button(self.gameWindow, text="Quit game", bg=BGCOLOR,
                            command=lambda: [self.gameWindow.withdraw(), self.window.deiconify(), state.initialize()])
        quitButton.pack(side="bottom", pady=20)

        # Window parameters
        self.gameWindow.minsize(800, 800)
        self.gameWindow.config(background=BGCOLOR)
        self.center_window(self.gameWindow, 800, 800)

    def onClick(self, event):

        y = int(event.x // cellWidth)
        x = int(event.y // cellHeight)

        global state

        if state.board[x][y] != 0 and state.remainingPawns == 0:
            self.selectedPawnX = x
            self.selectedPawnY = y

        if not self.gameFinished:

            if state.remainingPawns != 0:

                if state.place(x, y, True):

                    if self.mode == 1:
                        if self.difficulty == 1:
                            ai.playEasy()  # Easy
                        elif self.difficulty == 2:
                            state = ai.playMediumOrHard(depth, 0)  # Medium
                        elif self.difficulty == 3:
                            state = ai.playMediumOrHard(depth, 1)  # Hard
                        else:
                            print("Error\n")

            else:
                try:
                    if self.selectedPawnX is not None and self.selectedPawnY is not None:
                        if state.move(self.selectedPawnX, self.selectedPawnY, x, y, True):

                            self.selectedPawnX = None
                            self.selectedPawnY = None

                            if self.mode == 1:

                                if self.difficulty == 1:
                                    ai.playEasy()  # Easy
                                elif self.difficulty == 2:
                                    state = ai.playMediumOrHard(depth, 0)  # Medium
                                elif self.difficulty == 3:
                                    state = ai.playMediumOrHard(depth, 1)  # Hard
                                else:
                                    print("Error\n")
                except:
                    print("Fail")

        self.drawBoard(self.canvas, state)
        playerValue = 1 if state.playerPlaying == 1 else 2
        self.gameLabel.config(text="Player " + str(playerValue) + "'s turn:")

        if state.winner() != 0:
            if (state.winner() == 1):
                self.gameLabel.config(text="you've won!")
            else:
                self.gameLabel.config(text="you lost")
            self.gameFinished = True



app = Interface()
