from chess import Game
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import time


# icons by Freepik


class App:
    IMAGESWHITE = {"Pawn": "Icons/WhitePawn.png", "Rook": "Icons/WhiteRook.png",
                   "Bishop": "Icons/WhiteBishop.png", "King": "Icons/WhiteKing.png",
                   "Knight": "Icons/WhiteKnight.png", "Queen": "Icons/WhiteQueen.png"}

    IMAGESBLACK = {"Pawn": "Icons/BlackPawn.png", "Rook": "Icons/BlackRook.png",
                   "Bishop": "Icons/BlackBishop.png", "King": "Icons/BlackKing.png",
                   "Knight": "Icons/BlackKnight.png", "Queen": "Icons/BlackQueen.png"}

    def __init__(self):
        self.chess = Game.Chess()
        self.root = Tk()
        self.root.geometry("920x750")
        self.root.iconbitmap('icon.ico')
        self.root.resizable(0, 0)
        self.root.title("Classic Chess")

        self.left = Frame(self.root)
        self.bottom = Frame(self.root)
        self.right = Frame(self.root)
        self.game = Frame(self.root)
        self.lastmovements = []

        self.table()
        mainloop()

    def start(self):
        self.startbutton.config(state=DISABLED, text="The game Started!")
        self.pieces()
        self.visualizepieces()
        self.chess.starttime()
        while not self.chess.finish:
            if self.chess.shift == "White":
                while self.chess.shift == "White":
                    self.time()
                    self.root.update()
            else:
                while self.chess.shift == "Black":
                    self.time()
                    self.root.update()
            self.chess.checkwinner()
            self.visualizepieces()
        messagebox.showinfo("Classic Chess", "Game Finished, the winner is " + self.chess.winner[0])

    def time(self):
        self.label3.config(text="Time: " + str(int(time.time() - self.chess.gettime())) + "s")

    def pieces(self):
        self.piecesposition = {}
        for j in self.chess.table.getpieces():
            self.piecesposition[j.getid()] = Button(self.game, text=j.getcolor(), relief=FLAT,
                                                    command=lambda piece=j: self.movements(piece))

    def movements(self, piece):
        self.clearmovements()
        self.lastmovements.clear()
        print(piece.getid(), piece.getcolor())
        print(self.chess.checkmovements(piece))
        for i in self.chess.checkmovements(piece):
            self.lastmovements.append(Button(self.game, text="Move Here", command=lambda x=i[0], y=i[1]: self.move(piece, x, y), relief=FLAT))
            self.lastmovements[-1].grid(row=9 - i[1] - 2, column=i[0])

    def clearmovements(self):
        for l in self.lastmovements:
            l.destroy()

    def move(self, piece, x, y):
        if piece.getfirstmove():
            piece.setfirstmove()
        s = self.chess.movepiece(piece, x, y)
        self.clearmovements()
        self.chess.changecolor()
        if s:
            if self.chess.shift == "White":
                for i in self.chess.table.getwhitedeadpieces():
                    if i.getx() == x and i.gety() == y:
                        self.piecesposition[i.getid()].destroy()
            else:
                for i in self.chess.table.getblackdeadpieces():
                    if i.getx() == x and i.gety() == y:
                        self.piecesposition[i.getid()].destroy()
        print(self.chess.table.getpieces())
        print("")
        print(self.chess.table.getdeadpieces())

    def visualizepieces(self):
        for r in self.chess.table.getpieces():
            if self.chess.shift != r.getcolor():
                self.piecesposition[r.getid()].config(state=DISABLED)
            else:
                self.piecesposition[r.getid()].config(state=NORMAL)
            self.piecesposition[r.getid()].grid(row=9 - r.gety() - 2, column=r.getx())

    def gametable(self):
        for i in range(0, 8):
            if i % 2 == 0:
                colors = ("white", "black")
            else:
                colors = ("black", "white")
            for j in range(0, 8):
                if j % 2 != 0:
                    color = colors[0]
                else:
                    color = colors[1]
                Canvas(self.game, width=80, height=80, bg=color).grid(row=i, column=j)
        self.game.grid(row=0, column=1)

    def table(self):
        letters = "ABCDEFGH"
        font1 = Font(family="Times New Roman", size=20)
        font2 = Font(family="Times New Roman", size=36)

        for i in range(0, 8):
            j = 9 - i - 1
            label = ttk.Label(self.left, text=str(j))
            label.config(font=font2)
            label.grid(row=i, column=0, ipady=12)
        for i in range(0, len(letters)):
            label = ttk.Label(self.bottom, text=str(letters[i]))
            label.config(font=font2)
            label.grid(row=0, column=i, padx=24)
        self.left.grid(row=0, column=0, sticky=N)
        self.bottom.grid(row=1, column=1)

        self.gametable()

        self.startbutton = Button(self.right, text="Start", command=self.start, width=20, height=4)
        self.startbutton.grid(row=0, column=0)

        self.label3 = ttk.Label(self.right, text="")
        self.label3.grid(row=1, column=0)

        label = ttk.Label(self.right, text="Dead White Pieces", font=font1)
        label.grid(row=2, column=0)

        self.deadwhite = Frame(self.right)
        self.deadwhite.grid(row=3, column=0)

        self.deadblack = Frame(self.right)
        self.deadblack.grid(row=4, column=0)

        label2 = ttk.Label(self.right, text="Dead Black Pieces", font=font1)
        label2.grid(row=5, column=0)

        self.right.grid(row=0, column=2, sticky=(N, S), pady=25)


a = App()
