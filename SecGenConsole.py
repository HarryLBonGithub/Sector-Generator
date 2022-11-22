from tkinter import *
from tkinter import messagebox
import SecGenFunctions
import os
import functools #for .partial(command, arg)
import sqlite3

#variables
selectedRow = "0"
selectedColumn = "0"

currentSector = ""
currentSystem = ""

#root window setup
rootWindow = Tk()
rootWindow.title("SecGen")

#preload images
starFieldIcon = PhotoImage(file=r'images\Stars64.png')
smallStarIcon = PhotoImage(file=r'images\Star_Small_64.png')
midStarIcon = PhotoImage(file=r'images\Star_Mid_64.png')
largeStarIcon =PhotoImage(file=r'images\Star_Large_64.png')

systemStarIcon = PhotoImage(file=r'images\Planet_Star_64.png')
smallPlanetIcon = PhotoImage(file=r'images\Planet_Small_64.png')
midPlanetIcon = PhotoImage(file=r'images\Planet_Mid_64.png')
largePlanetIcon =PhotoImage(file=r'images\Planet_Large_64.png')

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
        
        currentSector = str(newSecNameInput.get() + ".db")
        sectorMapFrame.config(text="Sector Map: " + currentSector[:-3])
        newSectorCreator.destroy()
        createSectorMap()

        newSectorCreator.grab_release()
        
    newSectorCreator = Toplevel()
    newNamePrompt = Label(newSectorCreator, text="Sector Name: ")
    newSecNameInput = Entry(newSectorCreator,width=20)
    newSecConfirmButton = Button(newSectorCreator,text="Confirm", command=createSector)

    newSectorCreator.grab_set()

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
        global currentSector

        currentSector = sectorSelection.get()
        sectorMapFrame.config(text="Sector Map: " + currentSector[:-3])
        loadSectorWindow.destroy()

        createSectorMap()

        for previousItems in systemMapFrame.winfo_children():
            previousItems.destroy()
        
        planetInfoLabel.config(text="NO PLANET LOADED")
        starInfoLabel.config(text="NO SYSTEM LOADED")

        loadSectorWindow.grab_release()

    def deleteSector():
        os.remove('sectors/' + str(sectorSelection.get()))
        sectorMapFrame.config(text="Sector Map: ")
        loadSectorWindow.destroy()

        loadSectorWindow.grab_release()
        #needs a way to update the options menu without the deleted sector

    loadSectorWindow = Toplevel()

    loadSectorWindow.grab_set()

    sectorsList = os.listdir('sectors')

    if len(sectorsList) > 0:

        sectorSelection = StringVar()
        sectorSelection.set(sectorsList[0])
        sectorOptions = OptionMenu(loadSectorWindow, sectorSelection, *sectorsList)

        loadSectorButton = Button(loadSectorWindow,text="Load",command=loadSector)
        deleteSectorButton = Button(loadSectorWindow,text="Delete",command=deleteSector)

        sectorOptions.grid(row=0, column=0)
        loadSectorButton.grid(row=0, column=1)
        deleteSectorButton.grid(row=0,column=2)
    
    else:
        loadSectorWindow.destroy()
        messagebox.showerror(title="NO SECTORS", message="No Sector Databases to Load")

def editStar():
    pass

def editPlanet():
    pass

def createSectorMap():

    for previousItems in sectorMapFrame.winfo_children():
        previousItems.destroy()

    sector = sqlite3.connect('sectors/' + currentSector)
    cursor = sector.cursor()
    cursor.execute('SELECT * FROM stars')
    sectorStars = cursor.fetchall()

    numberOfStars = len(sectorStars)

    sectorMapButtons = []
    buttonCounter = 0

    for r in range(numberOfStars):
        for c in range(numberOfStars):
            
            icon = starFieldIcon
            starName = 'NA'
            starSize = 'NA'

            for star in sectorStars:
                if str(r + 1) == star[2] and str(c + 1) == star[3]:
                    
                    if star[1]=='small':
                        icon = smallStarIcon
                    elif star[1] == 'mid':
                        icon = midStarIcon
                    elif star[1] == 'large':
                        icon = largeStarIcon
                    
                    starName = star[0]
                    starSize = star[1]
                        
            newSectorButton = Button(sectorMapFrame, image=icon, bg='black', command=functools.partial(createSystemMap,starName,starSize,str(r+1),str(c+1)))
            sectorMapButtons.append(newSectorButton)
            sectorMapButtons[buttonCounter].grid(row=r, column=c)
            buttonCounter += 1

    sector.close()

def createSystemMap(systemName, starSize, systemRow, systemColumn):

    planetInfoLabel.config(text="NO PLANET LOADED")

    starInfoLabel.config(text="NAME: " + systemName + "\n" + "SIZE: " + starSize + "\n" + "ROW: " + systemRow + "\n" + "COLUMN: " + systemColumn)

    for previousItems in systemMapFrame.winfo_children():
        previousItems.destroy()

    global selectedRow
    global selectedColumn
    selectedRow = systemRow
    selectedColumn = systemColumn

    sector = sqlite3.connect('sectors/' + currentSector)
    cursor = sector.cursor()
    cursor.execute('SELECT * FROM planets WHERE star=?;', [systemName])
    systemPlanets = cursor.fetchall()

    planetButtons = []

    newPlanetButton = Button(systemMapFrame, image=systemStarIcon, bg='black')

    planetButtons.append(newPlanetButton)

    planetButtons[0].grid(row=0, column = 0)

    icon = midStarIcon

    counter = 1

    for planet in systemPlanets:
        if planet[2] == 'small':
            icon = smallPlanetIcon
        elif planet[2] == 'mid':
            icon = midPlanetIcon
        elif planet[2] == 'large':
            icon = largePlanetIcon
        
        newPlanetButton = Button(systemMapFrame, image = icon, bg = 'black', command = functools.partial(planetInfo, planet[1],planet[3],planet[4],planet[5], planet[6]))

        planetButtons.append(newPlanetButton)

        planetButtons[counter].grid(row=0,column=counter)

        counter += 1


    sector.close()

def planetInfo(name, temperature, humidity, life, note):
    formattedInfo ="NAME: " + name + "\n" + "TEMPERATURE: " + temperature + "\n" + "HUMIDITY: " + humidity +"\n" + "LIFE SIGNS: " + life + "\n" + "NOTE: " + note
    planetInfoLabel.config(text=formattedInfo)

#console object creation
sectorMapFrame = LabelFrame(rootWindow, text="Sector Map: " + currentSector, labelanchor=N,padx=5, pady=5)
initialSectorLabel = Label(sectorMapFrame, text = "NO SECTOR LOADED")

starInfoFrame = LabelFrame(rootWindow,text="Star Info", labelanchor=N)
starInfoLabel = Label(starInfoFrame,text="NO STAR LOADED")

editStarButton = Button(rootWindow, text="Edit Star", command=editStar)

systemMapFrame = LabelFrame(rootWindow, text="System Map", labelanchor=N)
initialSystemLabel = Label(systemMapFrame,text="NO SYSTEM LOADED")

planetInfoFrame = LabelFrame(rootWindow,text="Planet Info", labelanchor=N)
planetInfoLabel = Label(planetInfoFrame,text="NO PLANET LOADED")

editPlanetButton = Button(rootWindow, text="Edit Planet", command=editPlanet)

#console object display
sectorMapFrame.grid(row=0, column=0,padx=10,pady=10, rowspan=2)
initialSectorLabel.grid(row=0, column=0)

starInfoFrame.grid(row=0, column=1,padx=10,pady=10)
starInfoLabel.pack()

editStarButton.grid(row=1,column=1,padx=10,pady=10)

systemMapFrame.grid(row=2, column=0,padx=10,pady=10)
initialSystemLabel.grid(row=0,column=0)

planetInfoFrame.grid(row=3, column=0,padx=10,pady=10)
planetInfoLabel.pack()

editPlanetButton.grid(row=3,column=1,padx=10,pady=10)

#console menu bar
menuBar = Menu(rootWindow)
rootWindow.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=False)

fileMenu.add_command(label='New', command=newSectorWindow)
fileMenu.add_command(label='Open', command=openSectorWindow)
fileMenu.add_command(label='Exit',command=rootWindow.destroy)


menuBar.add_cascade(label="File",menu=fileMenu)

rootWindow.mainloop()