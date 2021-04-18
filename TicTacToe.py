from tkinter import *
#import configparser
#from PIL import Image, ImageTk
import threading
import tkinter.messagebox as messagebox

class Application(Frame):

  def __init__(self, master=None):
      Frame.__init__(self, master)
      self.maxPlayerToMove = True
      # Note: you cannot do: self.gridClicked = [[0] * 3]*3
      # for more reason, refer to: https://stackoverflow.com/questions/21036140/python-two-dimensional-array-changing-an-element
      self.gridClicked = [[0] * 3 for _ in range(3)]
      self.gridClickedCount = 0

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
    
    self.drawBoard()

    self.canvas1.bind("<Button-1>", self.canvasClicked)
    self.canvas1.pack(expand = True, fill = BOTH)

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
    self.nodeSearchedEntry.insert(0, "123456")
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
    if self.isEndState():
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

    self.isEndState()

  def isEndState(self):
    rowSum = [ sum(x) for x in self.gridClicked ]
    colSum = [ sum(x) for x in zip(*self.gridClicked) ]
    for s in rowSum:
      if s == 3:
        messagebox.showinfo("Winner!", "Max player has won!")
        return True
      elif s == -3:
        messagebox.showinfo("Winner!", "Min player has won!")
        return True
    for s in colSum:
      if s == 3:
        messagebox.showinfo("Winner!", "Max player has won!")
        return True
      elif s == -3:
        messagebox.showinfo("Winner!", "Min player has won!")
        return True
    s = sum(self.gridClicked[i][i] for i in range(3))
    if s == 3:
      messagebox.showinfo("Winner!", "Max player has won!")
      return True
    elif s == -3:
      messagebox.showinfo("Winner!", "Min player has won!")
      return True
    s = sum(self.gridClicked[i][3-i-1] for i in range(3))
    if s == 3:
      messagebox.showinfo("Winner!", "Max player has won!")
      return True
    elif s == -3:
      messagebox.showinfo("Winner!", "Min player has won!")
      return True
    if self.gridClickedCount == 9:
      messagebox.showinfo("Tie Game", "We tied!")
      return True
      
    return False

  def start(self):
    #messagebox.showinfo('Hint', '%s moves first' % (str(self.firstMoveVar.get())))
    self.gridClicked = [[0] * 3 for _ in range(3)]
    self.gridClickedCount = 0
    self.maxPlayerToMove = True
    self.canvas1.delete("all")
    self.drawBoard()

app = Application()
app.mainloop()
