from tkinter import *
#import configparser
#from PIL import Image, ImageTk
import math
from random import *
import threading
import tkinter.messagebox as messagebox

class Application(Frame):

  def __init__(self, master=None):
      Frame.__init__(self, master)
      self.gameInProgress = False

      #self.config = configparser.ConfigParser()
      #self.config.read('config.ini')
      #self.inputStart = int(self.config['General']['InputRangeStart'])
      #self.inputEnd = int(self.config['General']['InputRangeEnd'])

      self.createWidgets()

  def createWidgets(self):
    self.master.title("TicTacToe")
    self.pack(fill=BOTH, expand=True)

    firstFrame = Frame(self, width=300, height=300)
    firstFrame.pack(fill=BOTH, expand=True)

    self.canvas1 = Canvas(firstFrame, bg='grey', width=300, height=300)
    #circle = PhotoImage(file = "circle.gif")    
    #image = canvas1.create_image(0, 0, anchor='n', image=circle)
    self.canvas1.bind("<Button-1>", self.canvasClicked)
    self.canvas1.pack(expand = True, fill = BOTH)
    self.drawBoard()
    
    secondFrame = Frame(self)
    secondFrame.pack(fill=X, expand=True)

    firstMoveFrame = LabelFrame(secondFrame, text="First Move:")
    firstMoveFrame.pack(padx=10, pady=5, side=LEFT)

    self.firstMoveVar = IntVar()
    self.firstMoveR1 = Radiobutton(firstMoveFrame, text="Human", variable=self.firstMoveVar, value=1)
    self.firstMoveR1.pack(side=LEFT)
    self.firstMoveR1.select()
    self.firstMoveR1 = Radiobutton(firstMoveFrame, text="AI Master", variable=self.firstMoveVar, value=2)
    self.firstMoveR1.pack(side=LEFT)

    self.startButton = Button(secondFrame, text='Start', command=self.start, width=9)
    self.startButton.pack(pady=8, side=TOP)

    thirdFrame = Frame(self)
    thirdFrame.pack(fill=X, expand=True)
    nodeSearchedFrame = LabelFrame(thirdFrame, text="Node Searched:")
    nodeSearchedFrame.pack(padx=10, pady=10, side=LEFT, fill=X, expand=True)
    self.nodeSearchedEntry = Entry(nodeSearchedFrame, bd=3)
    self.nodeSearchedEntry.pack(side=LEFT, fill=X, expand=True)
    self.nodeSearchedEntry.insert(0, "0")
    self.nodeSearchedEntry.configure(state=DISABLED)

  def drawBoard(self):
    coordinates = 0, 3, 302, 3
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 0, 100, 302, 100
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 0, 200, 302, 200
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 0, 302, 302, 302
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 3, 0, 3, 302
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 100, 0, 100, 302
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 200, 0, 200, 302
    self.canvas1.create_line(coordinates, fill="black")
    coordinates = 302, 0, 302, 302
    self.canvas1.create_line(coordinates, fill="black")

  def drawCross(self, x0, y0):
    coordinates = x0, y0, x0 + 100, y0 + 100
    self.canvas1.create_line(coordinates, fill="blue")
    coordinates = x0, y0+100, x0+100, y0
    self.canvas1.create_line(coordinates, fill="blue")

  def drawCircle(self, x0, y0):
    coordinates = x0, y0, x0+100, y0+100
    self.canvas1.create_oval(coordinates, outline="red")

  def canvasClicked(self, event):
    #messagebox.showinfo("Coord", "Clicked at: %d, %d" % (event.x, event.y))
    if not self.gameInProgress:
      return

    #print(event.x, event.y)
    x0 = (int)(event.x / 100)
    y0 = (int)(event.y / 100)
    if self.gridClicked[x0][y0] != 0:
      return
    self.gridClicked[x0][y0] = 1 if self.maxPlayerToMove else -1
    self.gridClickedCount += 1
    #print(self.gridClicked)

    x0, y0 = x0*100, y0*100

    if self.maxPlayerToMove:
      self.drawCross(x0, y0)
    else:
      self.drawCircle(x0, y0)

    self.maxPlayerToMove = not self.maxPlayerToMove
    self.humanPlayerToMove = False
    finalScore = self.isEndState()
    self.gameInProgress = True if finalScore == -1 else False
    if not self.gameInProgress:
      self.displayFinalMessage(finalScore)
      return
    self.nextAIMove()

  def displayFinalMessage(self, finalScore):
    maxPlayer = "Human" if self.firstMoveVar.get() == 1 else "AI"
    minPlayer = "AI" if self.firstMoveVar.get() == 1 else "Human"
    if finalScore == 3:
      messagebox.showinfo("Winner!", "%s player has won!" % maxPlayer)
    elif finalScore == -3:
      messagebox.showinfo("Winner!", "%s player has won!" % minPlayer)
    else:
      messagebox.showinfo("Tie Game", "We tied!")

  def isEndState(self):
    rowSum = [ sum(x) for x in self.gridClicked ]
    colSum = [ sum(x) for x in zip(*self.gridClicked) ]
    for s in rowSum:
      if s == 3 or s == -3:
        return s
    for s in colSum:
      if s == 3 or s == -3:
        return s
    s = sum(self.gridClicked[i][i] for i in range(3))
    if s == 3 or s == -3:
      return s
    s = sum(self.gridClicked[i][3-i-1] for i in range(3))
    if s == 3 or s == -3:
      return s
    if self.gridClickedCount == 9:
      return 0
    return -1 # return -1 to indicate a non-terminal state

  def start(self):
    #messagebox.showinfo('Hint', '%s moves first' % (str(self.firstMoveVar.get())))
    # Note: you cannot do: self.gridClicked = [[0] * 3]*3
    # for more reason, refer to: https://stackoverflow.com/questions/21036140/python-two-dimensional-array-changing-an-element
    self.gridClicked = [[0] * 3 for _ in range(3)]
    self.gridClickedCount = 0
    self.nodeCount = 0
    self.maxPlayerToMove = True
    self.humanPlayerToMove = True if self.firstMoveVar.get() == 1 else False
    self.canvas1.delete("all")
    self.drawBoard()
    self.gameInProgress = True
    if not self.humanPlayerToMove:
      self.nextAIMove()
  
  def nextAIMove(self):
    # x0 = randint(0, 2)
    # y0 = randint(0, 2)
    # while self.gridClicked[x0][y0] != 0:
    #   x0 = randint(0, 2)
    #   y0 = randint(0, 2)
    #bestScore = -math.inf if self.maxPlayerToMove else math.inf
    x0, y0 = -1, -1
    if self.maxPlayerToMove:
      nextMove = self.findMaxMove(0, -math.inf, math.inf)
    else:
      nextMove = self.findMinMove(0, -math.inf, math.inf)
    x0 = nextMove[1]
    y0 = nextMove[2]
    self.gridClicked[x0][y0] = 1 if self.maxPlayerToMove else -1
    self.gridClickedCount += 1
    
    x0, y0 = x0*100, y0*100
    if self.maxPlayerToMove:
      self.drawCross(x0, y0)
    else:
      self.drawCircle(x0, y0)
    
    self.nodeSearchedEntry.configure(state=NORMAL)
    self.nodeSearchedEntry.delete(0, END)
    self.nodeSearchedEntry.insert(0, self.nodeCount)
    self.nodeSearchedEntry.configure(state=DISABLED)

    self.maxPlayerToMove = not self.maxPlayerToMove
    self.humanPlayerToMove = True
    finalScore = self.isEndState()
    self.gameInProgress = True if finalScore == -1 else False
    if not self.gameInProgress:
      self.displayFinalMessage(finalScore)

  def findMaxMove(self, depth, alpha, beta):
    score = self.isEndState()
    if score != -1: # -1 indicating it's a non-terminal state
      return [score, -1, -1]
  
    maxScore = -math.inf
    x0, y0 = -1, -1
    for i in range(3):
      for j in range(3):
        if (self.gridClicked[i][j]) == 0:
          self.gridClicked[i][j] = 1
          self.gridClickedCount += 1
          self.nodeCount += 1
          nextMove = self.findMinMove(depth+1, alpha, beta)
          if (nextMove[0] > maxScore):
            maxScore = nextMove[0]
            x0, y0 = i, j
          self.gridClicked[i][j] = 0
          self.gridClickedCount -= 1
          alpha = max(alpha, nextMove[0])
          if (beta <= alpha): # meaning the minplayer had a better move earlier on, so no need to continue, we prune
            return [maxScore, x0, y0]
    return [maxScore, x0, y0]

  def findMinMove(self, depth, alpha, beta):
    score = self.isEndState()
    if score != -1: # -1 indicating it's a non-terminal state
      return [score, -1, -1]
    
    minScore = math.inf
    x0, y0 = -1, -1
    for i in range(3):
      for j in range(3):
        if (self.gridClicked[i][j] == 0):
          self.gridClicked[i][j] = -1
          self.gridClickedCount += 1
          self.nodeCount += 1
          nextMove  = self.findMaxMove(depth+1, alpha, beta)
          if (nextMove[0] < minScore):
            minScore = nextMove[0]
            x0, y0 = i, j
          self.gridClicked[i][j] = 0
          self.gridClickedCount -= 1
          beta = min(beta, nextMove[0])
          if (beta <= alpha):
            return [minScore, x0, y0]
    return [minScore, x0, y0]

app = Application()
app.mainloop()
