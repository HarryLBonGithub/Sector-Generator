from tkinter import *
from tkinter import messagebox

#variables
selectedRow = "0"
selectedColumn = "0"

currentSector = ""

#root window setup
rootWindow = Tk()
rootWindow.title("SecGen")

#functions
def editStar():
    pass

def editPlanet():
    pass

def openSector():
    pass

#console object creation
sectorMapFrame = LabelFrame(rootWindow, text="Sector Map", labelanchor=N)
fillerLabel = Label(sectorMapFrame,text="Hello!")

systemMapFrame = LabelFrame(rootWindow, text="System Map", labelanchor=N)
fillerLabel2 = Label(systemMapFrame,text="Hello!")

starInfoFrame = LabelFrame(rootWindow,text="Star Info", labelanchor=N)
fillerLabel3 = Label(starInfoFrame,text="Hello!")

editStarButton = Button(rootWindow, text="Edit Star", command=editStar)

planetInfoFrame = LabelFrame(rootWindow,text="Planet Info", labelanchor=N)
fillerLabel4 = Label(planetInfoFrame,text="Hello!")

editPlanetButton = Button(rootWindow, text="Edit Planet", command=editPlanet)

openSectorButton = Button(rootWindow, text="OPEN SECTOR", command=openSector)

#console object display
sectorMapFrame.grid(row=0, column=0,padx=10,pady=10, columnspan=2)
fillerLabel.pack()

systemMapFrame.grid(row=0, column=2,padx=10,pady=10, columnspan=2)
fillerLabel2.pack()

starInfoFrame.grid(row=1, column=0,padx=10,pady=10)
fillerLabel3.pack()

editStarButton.grid(row=1,column=1,padx=10,pady=10)

planetInfoFrame.grid(row=1, column=2,padx=10,pady=10)
fillerLabel4.pack()

editPlanetButton.grid(row=1,column=3,padx=10,pady=10)

openSectorButton.grid(row=2,column=0, pady = 10, columnspan=4)

rootWindow.mainloop()