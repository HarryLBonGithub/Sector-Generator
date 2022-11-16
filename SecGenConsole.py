from tkinter import *
from tkinter import messagebox
import SecGenFunctions
import os

#variables
selectedRow = "0"
selectedColumn = "0"

currentSector = ""

#root window setup
rootWindow = Tk()
rootWindow.title("SecGen")

#functions
def newSectorWindow():

    def createSector():
        global currentSector

        if sizeSelection.get() == "Small":
            gridNumber = 5
            starNumber = 5
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber)
        elif sizeSelection.get() == "Medium":
            gridNumber = 10
            starNumber = 10
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber)
        elif sizeSelection.get() == "Large":
            gridNumber = 15
            starNumber = 15
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber)
        
        currentSector = newSecNameInput.get()
        sectorMapFrame.config(text="Sector Map: " + currentSector)
        newSectorCreator.destroy()
        
    newSectorCreator = Toplevel()
    newNamePrompt = Label(newSectorCreator, text="Sector Name: ")
    newSecNameInput = Entry(newSectorCreator,width=20)
    newSecConfirmButton = Button(newSectorCreator,text="Confirm", command=createSector)

    sizeSelectionPrompt = Label(newSectorCreator, text="Size: ")
    sizeSelection = StringVar()
    sizeSelection.set("Medium")
    newSecSize = OptionMenu(newSectorCreator, sizeSelection, "Small", "Medium", "Large")

    newNamePrompt.grid(row=0, column=0, padx=10, pady=10)
    newSecNameInput.grid(row=0, column=1, padx=10,pady=10)
    sizeSelectionPrompt.grid(row=0,column=2)
    newSecSize.grid(row=0, column=3, padx=10)
    newSecConfirmButton.grid(row=1)

def openSectorWindow():

    def loadSector():
        currentSector = sectorSelection.get()
        sectorMapFrame.config(text="Sector Map: " + currentSector)
        loadSectorWindow.destroy()

    def deleteSector():
        os.remove('sectors/' + sectorSelection.get())
        sectorMapFrame.config(text="Sector Map: ")
        loadSectorWindow.destroy()
        #needs a way to update the options menu without the deleted sector

    loadSectorWindow = Toplevel()

    sectorsList = os.listdir('sectors')

    sectorSelection = StringVar()
    sectorSelection.set(sectorsList[0])
    sectorOptions = OptionMenu(loadSectorWindow, sectorSelection, *sectorsList)

    loadSectorButton = Button(loadSectorWindow,text="Load",command=loadSector)
    deleteSectorButton = Button(loadSectorWindow,text="Delete",command=deleteSector)

    sectorOptions.grid(row=0, column=0)
    loadSectorButton.grid(row=0, column=1)
    deleteSectorButton.grid(row=0,column=2)

def editStar():
    pass

def editPlanet():
    pass

def openSector():
    pass

#console object creation
sectorMapFrame = LabelFrame(rootWindow, text="Sector Map: " + currentSector, labelanchor=N)
fillerLabel = Label(sectorMapFrame,text="Hello!")

systemMapFrame = LabelFrame(rootWindow, text="System Map", labelanchor=N)
fillerLabel2 = Label(systemMapFrame,text="Hello!")

starInfoFrame = LabelFrame(rootWindow,text="Star Info", labelanchor=N)
fillerLabel3 = Label(starInfoFrame,text="Hello!")

editStarButton = Button(rootWindow, text="Edit Star", command=editStar)

planetInfoFrame = LabelFrame(rootWindow,text="Planet Info", labelanchor=N)
fillerLabel4 = Label(planetInfoFrame,text="Hello!")

editPlanetButton = Button(rootWindow, text="Edit Planet", command=editPlanet)

openSectorWindowButton = Button(rootWindow, text="OPEN SECTOR", command=openSectorWindow)
newSectorWindowButton = Button(rootWindow, text="NEW SECTOR",command=newSectorWindow)

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

openSectorWindowButton.grid(row=2,column=0, pady = 10, columnspan=2)
newSectorWindowButton.grid(row=2, column=2,pady=10, columnspan=2)

rootWindow.mainloop()