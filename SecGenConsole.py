from tkinter import *
from tkinter import messagebox
import SecGenFunctions
import os
import functools #for .partial(command, arg)
import sqlite3

#variables
currentSector = ""

selectedRow = "0"
selectedColumn = "0"
currentSystem = ""
currentPlanet = ""

#root window setup
rootWindow = Tk()
rootWindow.title("SecGen")
rootWindow.minsize(width=580, height=500)

#preload images
welcomeImage = PhotoImage(file=r'images\Sec-Gen Filler.png')
systemMapFiller = PhotoImage(file=r'images\Sec-Gen Long Filler.png')

starFieldIcon = PhotoImage(file=r'images\Stars64.png')
smallStarIcon = PhotoImage(file=r'images\Star_Small_64.png')
midStarIcon = PhotoImage(file=r'images\Star_Mid_64.png')
largeStarIcon =PhotoImage(file=r'images\Star_Large_64.png')

systemStarIcon = PhotoImage(file=r'images\Planet_Star_64.png')
smallPlanetIcon = PhotoImage(file=r'images\Planet_Small_64.png')
midPlanetIcon = PhotoImage(file=r'images\Planet_Mid_64.png')
largePlanetIcon =PhotoImage(file=r'images\Planet_Large_64.png')

rootWindow.iconphoto(False,starFieldIcon)

#functions
def newSectorWindow():

    def createSector():
        global currentSector

        sectorsList = os.listdir('sectors')

        if str(newSecNameInput.get() + ".db") in sectorsList:
            messagebox.showerror(title="BAD NAME", message="Sector already exists. Choose a different name.")
            return

        if sizeSelection.get() == "Small":
            gridNumber = 5
            starNumber = 5
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber, gridNumber)
        elif sizeSelection.get() == "Medium":
            gridNumber = 10
            starNumber = 10
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber, gridNumber)
        elif sizeSelection.get() == "Large":
            gridNumber = 15
            starNumber = 15
            SecGenFunctions.generateSector(newSecNameInput.get(), starNumber, gridNumber, gridNumber)
        
        clearMaps()

        currentSector = str(newSecNameInput.get() + ".db")
        sectorMapFrame.config(text="Sector Map: " + currentSector[:-3])
        newSectorCreator.destroy()
        createSectorMap()

        newSectorCreator.grab_release()
        resetCurrents()
        statusUpdate()
        
    newSectorCreator = Toplevel()
    newNamePrompt = Label(newSectorCreator, text="Sector Name: ")
    newSecNameInput = Entry(newSectorCreator,width=20)
    newSecConfirmButton = Button(newSectorCreator,text="Confirm", command=createSector)

    newSectorCreator.grab_set()

    sizeSelectionPrompt = Label(newSectorCreator, text="Size: ")
    sizeSelection = StringVar()
    sizeSelection.set("Medium")
    newSecSize = OptionMenu(newSectorCreator, sizeSelection, "Small", "Medium", "Large")

    newNamePrompt.grid(row=0, column=0, padx=(5,0), pady=10)
    newSecNameInput.grid(row=0, column=1, padx=(0,5),pady=10)
    sizeSelectionPrompt.grid(row=0,column=2)
    newSecSize.grid(row=0, column=3, padx=(0,5))
    newSecConfirmButton.grid(row=1, columnspan=4, pady=5)

def openSectorWindow():

    def loadSector():
        global currentSector

        currentSector = sectorSelection.get()
        sectorMapFrame.config(text="Sector Map: " + currentSector[:-3])
        loadSectorWindow.destroy()

        clearMaps()

        createSectorMap()

        loadSectorWindow.grab_release()

        resetCurrents()
        statusUpdate()

    def deleteSector():

        global currentSector

        confirmed = messagebox.askyesno(title="DELETE SECTOR", message="Are you sure you want to delete this sector? This action cannot be undone.")

        if confirmed:

            if str(sectorSelection.get()) == currentSector:

                clearMaps()

                resetCurrents()

            os.remove('sectors/' + str(sectorSelection.get()))
            sectorMapFrame.config(text="Sector Map: ")
            loadSectorWindow.destroy()

            loadSectorWindow.grab_release()

            statusUpdate()

    loadSectorWindow = Toplevel()

    loadSectorWindow.grab_set()

    sectorsList = os.listdir('sectors')

    if len(sectorsList) > 0:

        sectorSelection = StringVar()
        sectorSelection.set(sectorsList[0])
        sectorOptions = OptionMenu(loadSectorWindow, sectorSelection, *sectorsList)

        loadSectorButton = Button(loadSectorWindow,text="Load",command=loadSector)
        deleteSectorButton = Button(loadSectorWindow,text="Delete",command=deleteSector)

        sectorOptions.grid(row=0, column=0, padx=5, pady=5)
        loadSectorButton.grid(row=0, column=1)
        deleteSectorButton.grid(row=0,column=2, padx=(0,5))
    
    else:
        loadSectorWindow.destroy()
        messagebox.showerror(title="NO SECTORS", message="No Sector Databases to Load")

def editStarWindow():
    #BEFORE EDITING/ADDING STARS
    #create a new table for sectors which includeds name and grid sizes
    #current method for creating the sector map is based on the number of planets in a sector
    #this will be thrown off if a user can add stars
    #new map generation needs to be based off either a "ROW" and "COLUM" in a new table or a set "SIZE" parameter
    pass

def editPlanetWindow():
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

    statusUpdate()

    sector.close()

def createSystemMap(systemName, starSize, systemRow, systemColumn):

    global currentSystem
    currentSystem = systemName

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

    statusUpdate()

    sector.close()

def planetInfo(name, temperature, humidity, life, note):
    global currentPlanet
    currentPlanet = name

    formattedInfo ="NAME: " + name + "\n" + "TEMPERATURE: " + temperature + "\n" + "HUMIDITY: " + humidity +"\n" + "LIFE SIGNS: " + life + "\n" + "NOTE: " + note
    planetInfoLabel.config(text=formattedInfo)

    statusUpdate()

def statusUpdate():
    status.config(text="Sec: " + currentSector + "/Sys: " + currentSystem + "/Pln: " + currentPlanet + "[R:" + selectedRow + "/C:" + selectedColumn + "]", relief=SUNKEN, anchor=E)

def resetCurrents():
    global currentPlanet
    global currentSystem
    global selectedColumn
    global selectedRow

    currentPlanet = ""
    currentSystem = ""
    selectedColumn = "0"
    selectedRow = "0"

def clearMaps():
    for previousItems in sectorMapFrame.winfo_children():
        previousItems.destroy()
                
    for previousItems in systemMapFrame.winfo_children():
        previousItems.destroy()

    planetInfoLabel.config(text="NO PLANET LOADED")
    starInfoLabel.config(text="NO SYSTEM LOADED")
    welcomeLabel = Label(sectorMapFrame, image=welcomeImage)
    welcomeLabel.grid(row=0, column=0)
    systemMapFillerImage = Label(systemMapFrame, image=systemMapFiller)
    systemMapFillerImage.grid(row=0,column=0)

#console object creation
sectorMapFrame = LabelFrame(rootWindow, text="Sector Map: " + currentSector, labelanchor=N,padx=5, pady=5)
welcomeLabel = Label(sectorMapFrame, image=welcomeImage)

starInfoFrame = LabelFrame(rootWindow,text="Star Info", labelanchor=N)
starInfoLabel = Label(starInfoFrame,text="NO STAR LOADED", justify=LEFT)
editStarButton = Button(starInfoFrame, text="Edit Star", command=editStarWindow, height=4)

systemMapFrame = LabelFrame(rootWindow, text="System Map", labelanchor=N)
systemMapFillerImage = Label(systemMapFrame, image=systemMapFiller)

planetInfoFrame = LabelFrame(rootWindow,text="Planet Info", labelanchor=N)
planetInfoLabel = Label(planetInfoFrame,text="NO PLANET LOADED", justify=LEFT)
editPlanetButton = Button(planetInfoFrame, text="Edit Planet", command=editPlanetWindow, height=5)

status = Label(rootWindow, text="Sec: " + currentSector + "/Sys: " + currentSystem + "/Pln: " + currentPlanet + "[R:" + selectedRow + "/C:" + selectedColumn + "]", relief=SUNKEN, anchor=E)

#console object display
sectorMapFrame.grid(row=0, column=0,padx=10,pady=10, rowspan=2, sticky=NW)
welcomeLabel.grid(row=0, column=0)

starInfoFrame.grid(row=0, column=1,padx=10,pady=10,sticky=SW)
starInfoLabel.grid(row=0, column=0)
editStarButton.grid(row=0,column=1,padx=10,pady=10)

planetInfoFrame.grid(row=1, column=1,padx=10,pady=10, sticky=NW)
planetInfoLabel.grid(row = 0, column=0)
editPlanetButton.grid(row=0,column=1,padx=10,pady=10)

systemMapFrame.grid(row=2, column=0,padx=10,pady=10, sticky=W, columnspan=2)
systemMapFillerImage.grid(row=0,column=0)

status.grid(row=3, column=0, columnspan=2, sticky=W+E)

#console menu bar
menuBar = Menu(rootWindow)
rootWindow.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=False)

fileMenu.add_command(label='New', command=newSectorWindow)
fileMenu.add_command(label='Open', command=openSectorWindow)
fileMenu.add_command(label='Exit',command=rootWindow.destroy)

menuBar.add_cascade(label="File",menu=fileMenu)

rootWindow.mainloop()