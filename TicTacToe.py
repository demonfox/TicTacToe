from tkinter import *
#import configparser
#from PIL import Image, ImageTk
import threading
import tkinter.messagebox as messagebox

class Application(Frame):

  def __init__(self, master=None):
      Frame.__init__(self, master)

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

  def drawCross(self, x, y):
    x0 = (int)(x / 100) * 100
    y0 = (int)(y / 100) * 100
    coordinates = x0, y0, x0 + 100, y0 + 100
    self.canvas1.create_line(coordinates, fill="blue")
    coordinates = x0, y0+100, x0+100, y0
    self.canvas1.create_line(coordinates, fill="blue")

    #coordinates = 100, 0, 200, 100
    #self.canvas1.create_line(coordinates, fill="blue")
    #coordinates = 200, 0, 100, 100
    #self.canvas1.create_line(coordinates, fill="blue")

    #coordinates = 200, 200, 300, 300
    #self.canvas1.create_oval(coordinates, outline="red")
  
  def canvasClicked(self, event):
    #messagebox.showinfo("Coord", "Clicked at: %d, %d" % (event.x, event.y))
    self.drawCross(event.x, event.y)

  def start(self):
    messagebox.showinfo('Hint', '%s moves first' % (str(self.firstMoveVar.get())))
  
app = Application()
app.mainloop()
