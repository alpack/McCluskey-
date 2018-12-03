"""
CESAR School
Computer Science 2018.1/2
Course: Computational Logic
Professor: Ricardo
Group: Arthur Reis, Pedro Henrique, Leonardo Melo

This program implements Quine-McCluskey method
to decode boolean expressions.
"""

from tkinter import *
import Quine_McCluskey as qm

minterms = []
dontcare = []
varNum = 0

offsets = (
    (0, 0, 1, 0),  # top
    (1, 0, 1, 1),  # upper right
    (1, 1, 1, 2),  # lower right
    (0, 2, 1, 2),  # bottom
    (0, 1, 0, 2),  # lower left
    (0, 0, 0, 1),  # upper left
    (0, 1, 1, 1),  # middle
)

####################################################################################
#                            7-SEGMENT DISPLAY TRUTH TABLE                         #
####################################################################################
digits = (                  # digit |  b3 b2 b1 b0 | a   b   c   d   e   f   g     #
    (1, 1, 1, 1, 1, 1, 0),  # 0   |  0  0  0  0  |  1   1   1   1   1   1   0    #
    (0, 1, 1, 0, 0, 0, 0),  # 1   |  0  0  0  1  |  0   1   1   0   0   0   0    #
    (1, 1, 0, 1, 1, 0, 1),  # 2   |  0  0  1  0  |  1   1   0   1   1   0   1    #
    (1, 1, 1, 1, 0, 0, 1),  # 3   |  0  0  1  1  |  1   1   1   1   0   0   1    #
    (0, 1, 1, 0, 0, 1, 1),  # 4   |  0  1  0  0  |  0   1   1   0   0   1   1    #
    (1, 0, 1, 1, 0, 1, 1),  # 5   |  0  1  0  1  |  1   0   1   1   0   1   1    #
    (1, 0, 1, 1, 1, 1, 1),  # 6   |  0  1  1  0  |  1   0   1   1   1   1   1    #
    (1, 1, 1, 0, 0, 0, 0),  # 7   |  0  1  1  1  |  1   1   1   0   0   0   0    #
    (1, 1, 1, 1, 1, 1, 1),  # 8   |  1  0  0  0  |  1   1   1   1   1   1   1    #
    (1, 1, 1, 0, 0, 1, 1),  # 9   |  1  0  0  1  |  1   1   1   1   0   1   1    #
    (1, 1, 1, 0, 1, 1, 1),  # A   |  1  0  1  0  |  1   1   1   0   1   1   1    #
    (0, 0, 1, 1, 1, 1, 1),  # b   |  1  0  1  1  |  0   0   1   1   1   1   1    #
    (1, 0, 0, 1, 1, 1, 0),  # C   |  1  1  0  0  |  1   0   0   1   1   1   0    #
    (0, 1, 1, 1, 1, 0, 1),  # d   |  1  1  0  1  |  0   1   1   1   1   0   1    #
    (1, 0, 0, 1, 1, 1, 1),  # E   |  1  1  1  0  |  1   0   0   1   1   1   1    #
    (1, 0, 0, 0, 1, 1, 1),  # F   |  1  1  1  1  |  1   0   0   0   1   1   1    #
    (1, 0, 1, 1, 1, 1, 0),  # G
    (0, 1, 1, 0, 1, 1, 1),  # H
    (0, 1, 1, 0, 0, 0, 0),  # I
    (0, 1, 1, 1, 1, 0, 0),  # J
    (0, 0, 0, 0, 1, 1, 1),  # K
    (0, 0, 0, 1, 1, 1, 0),  # L
    (1, 0, 1, 0, 1, 0, 1),  # M
    (0, 0, 1, 0, 1, 0, 1),  # N
    (1, 1, 1, 1, 1, 1, 0),  # O
    (1, 1, 0, 0, 1, 1, 1),  # P
    (1, 1, 1, 0, 0, 1, 1),  # Q
    (0, 0, 0, 0, 1, 0, 1),  # R
    (1, 0, 1, 1, 0, 1, 1),  # S
    (0, 0, 0, 1, 1, 1, 1),  # T
    (0, 1, 1, 1, 1, 1, 0),  # U
    (0, 1, 0, 0, 0, 1, 1),  # V
    (0, 1, 0, 1, 0, 1, 1),  # X
    (0, 1, 0, 0, 1, 0, 1),  # Z
    (0, 1, 1, 1, 0, 1, 1),  # Y
    (1, 1, 0, 1, 1, 0, 1),  # W
    (0, 0, 0, 0, 0, 0, 0)   # space
)
####################################################################################


class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Decodificador Quine-McCluskey")
        self.root.geometry("800x600")
        self.root.configure(background="black")

        self.frame = Frame(background="white")
        self.frame.pack(side=TOP, fill="both", expand=True)

        self.createWidgets()

    def createWidgets(self):
        Label(self.frame, text="Minterms: ").grid(row=0, column=0, sticky=W)
        self.minterms = Entry(self.frame, bg="white", width=35)
        self.minterms.grid(row=0, column=1, sticky=W)
        self.minterms.insert(0, "1 5 6 12 13 14")

        Label(self.frame, text="Don't cares: ").grid(row=1, column=0, sticky=W)
        self.dontcare = Entry(self.frame, bg="white", width=35)
        self.dontcare.grid(row=1, column=1, sticky=W)
        self.dontcare.insert(0, "2 4")

        Label(self.frame, text="Variables: ").grid(row=2, column=0, sticky=W)
        self.varNum = Entry(self.frame, bg="white")
        self.varNum.grid(row=2, column=1, sticky=W+E)
        self.varNum.insert(0, "4")

        Label(self.frame, text="### Prime Implicants ###").grid(
            row=3, column=0, sticky=W+E)
        self.primeImpsTxtBox = Text(self.frame, bg="white", height=8, width=4)
        self.primeImpsTxtBox.grid(row=4, column=0, sticky=W+E)

        Label(self.frame, text="### Essential Implicants ###").grid(
            row=3, column=2, sticky=W+E)
        self.essentialImpsTxtBox = Text(
            self.frame, bg="white", height=8, width=4)
        self.essentialImpsTxtBox.grid(row=4, column=2, sticky=W+E)

        Label(self.frame, text="### Solutions ###").grid(
            row=5, columnspan=3, sticky=W+E)
        self.solutionTxtBox = Text(self.frame, height=2, width=30)
        self.solutionTxtBox.grid(row=6, columnspan=3, sticky=W+E)

        self.solveButton = Button(self.frame, text="Solve", command=solve)
        self.solveButton.grid(row=7, columnspan=3, sticky=W+E)

        self.quitButton = Button(
            self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.quitButton.grid(row=8, columnspan=3, sticky=W+E)


class SevenSegments:
    def __init__(self, canvas, *, x=10, y=10, length=20, width=3):
        size = length
        self.canvas = canvas
        self.segment = []

        for x0, y0, x1, y1 in offsets:
            self.segment.append(canvas.create_line(
                x + x0*size, y + y0*size, x + x1*size, y + y1*size,
                width=width, state='hidden'))

    def display(self, num):
        for iid, on in zip(self.segment, digits[num]):
            self.canvas.itemconfigure(iid, state='normal' if on else 'hidden')

def get_char_ord(mychar):
    if mychar.isdigit():
        return int(mychar)
    if mychar == ' ':
        return 36
    else:
        return (ord(mychar.lower())-ord('a')+10)

def solve():
    strMinterms = app.minterms.get()
    strDontCare = app.dontcare.get()
    strVarNum = app.varNum.get()

    validEntry = qm.validate(strMinterms, strDontCare, strVarNum)

    if validEntry:
        app.primeImpsTxtBox.delete('0.0', END)
        app.essentialImpsTxtBox.delete('0.0', END)
        app.solutionTxtBox.delete('0.0', END)

        primes = qm.solve(validEntry[0], int(strVarNum), 1)
        essential = qm.solve(validEntry[0], int(strVarNum), 2)
        solution = qm.solve(validEntry[0], int(strVarNum), 0)

        for i in primes:
            app.primeImpsTxtBox.insert(END, i)
        for i in essential:
            app.essentialImpsTxtBox.insert(END, i)
        for i in solution:
            app.solutionTxtBox.insert(END, i)


app = App()
app.createWidgets()

root = Tk()
screen = Canvas(root)
screen.grid()

user_input = input("Type the phrase to show in the display: ")
segments = SevenSegments(screen)


count = 0


def update():
    global count
    my_dig = get_char_ord(user_input[count])
    segments.display(my_dig)
    count = (count+1) % len(user_input)
    root.after(1000, update)


root.after(1000, update)

app.root.mainloop()
