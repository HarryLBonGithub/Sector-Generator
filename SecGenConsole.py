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
currentPlanetOrbital = ""

#root window setup
rootWindow = Tk()
rootWindow.title("SecGen")
rootWindow.minsize(width=620, height=500)

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

addIcon =PhotoImage(file=r'images\Button_Add_64.png')

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

def openEditStarWindow():

    def createStarCommand():
        nameEntry = nameEntryField.get().strip()
        
        if SecGenFunctions.nameIsValid(currentSector,nameEntry) and numberIsValid():

            SecGenFunctions.generateStarSystem(currentSector,nameEntry,sizeSelection.get(),planetCountEntryField.get(),selectedRow,selectedColumn)

            editCleanup()
            createStarWindow.grab_release()
            createStarWindow.destroy()
        else:
            messagebox.showerror(title="INVALID NAME", message="Name must be unique and have at least 1 character. Number of planets must be an integer ranging from 0 - 10.")

    def editStarNameCommand():
        nameEntry = nameEntryField.get().strip()

        if SecGenFunctions.nameIsValid(currentSector,nameEntry):

            SecGenFunctions.editStarName(currentSector,currentSystem,nameEntry)

            editCleanup()
            editStarWindow.grab_release()
            editStarWindow.destroy()
        else:
            messagebox.showerror(title="INVALID NAME", message="Name must be unique and have at least 1 character.")

    def editStarSizeCommand():

        SecGenFunctions.editStarSize(currentSector,currentSystem,sizeSelection.get())

        editCleanup()
        editStarWindow.grab_release()
        editStarWindow.destroy()

    def deleteStarSystemCommand():
        
        global currentSystem
        global currentSector

        confirmed = messagebox.askyesno(title="DELETE SECTOR", message="Are you sure you want to delete this star system? This action cannot be undone.")

        if confirmed:
            SecGenFunctions.deleteStarSystem(currentSector, currentSystem)
            editCleanup()
            editStarWindow.grab_release()
            editStarWindow.destroy()

    def numberIsValid():
        if planetCountEntryField.get().isnumeric() and int(planetCountEntryField.get()) >= 0 and int(planetCountEntryField.get()) < 11:
            return True
        else:
            return False  
    
    if currentSystem == "NA": #If editing empty space, opens a 'create system' window
        createStarWindow = Toplevel()
        createStarWindow.title("Create Star")

        createStarWindow.grab_set()

        #object creation
        instructionLabel = Label(createStarWindow,text="CREATE STAR AT COORDINATES [R:"+selectedRow+"/C:"+selectedColumn+"]")

        nameEntryFrame = LabelFrame(createStarWindow, text="Name", padx=5, pady=5, labelanchor=N)
        nameEntryField = Entry(nameEntryFrame, width=20)

        planetCountFrame = LabelFrame(createStarWindow, text="Number of Planets", padx=5, pady=5, labelanchor=N)
        planetCountEntryField = Entry(planetCountFrame, width=20)

        sizeFrame = LabelFrame(createStarWindow, text="Size", padx=5,pady=5, labelanchor=N)
        sizeSelection = StringVar()
        sizeSelection.set("mid")
        newStarSize = OptionMenu(sizeFrame, sizeSelection, "small", "mid", "large")

        createButton = Button(createStarWindow, text="CREATE", command=createStarCommand)

        #object display
        instructionLabel.grid(row=0,column=0,padx=5,pady=5)

        nameEntryFrame.grid(row=1,column=0,padx=5,pady=5)
        nameEntryField.grid(row=0,column=0)
        
        planetCountFrame.grid(row=2,column=0,padx=5,pady=5)
        planetCountEntryField.grid(row=0,column=0)

        sizeFrame.grid(row=3,column=0,padx=5,pady=5)
        newStarSize.grid(row=0,column=0)

        createButton.grid(row=4,column=0,padx=5,pady=5)
 
    elif currentSystem == "": #If no sector is open, does nothing
        return

    else: #If editing an existing star, opens an 'edit star' window
        
        editStarWindow = Toplevel()
        editStarWindow.title("Edit Star")

        editStarWindow.grab_set()
        
        #object creation
        instructionLabel = Label(editStarWindow,text="EDIT STAR AT COORDINATES [R:"+selectedRow+"/C:"+selectedColumn+"]")

        nameEntryFrame = LabelFrame(editStarWindow, text="Edit Name", padx=5,pady=5, labelanchor=N)
        nameEntryField = Entry(nameEntryFrame, width=15)
        nameCommitButton = Button(nameEntryFrame, text="Commit", command=editStarNameCommand)

        sizeEditFrame = LabelFrame(editStarWindow,text="Edit Size", padx=5,pady=5, labelanchor=N)
        sizeSelection = StringVar()
        sizeSelection.set("mid")
        newStarSize = OptionMenu(sizeEditFrame, sizeSelection, "small", "mid", "large")
        sizeCommitButton = Button(sizeEditFrame, text="Commit", command=editStarSizeCommand, anchor=E)

        deleteSystemButton = Button(editStarWindow, text="DELETE SYSTEM", bg='red', command=deleteStarSystemCommand)

        #object display
        instructionLabel.grid(row=0, column=0, columnspan=3,pady=(0,5),padx=5)

        nameEntryFrame.grid(row=1,column=0,pady=5,padx=5, sticky=W+E)
        nameEntryField.grid(row=0,column=0, padx=(0,33))
        nameCommitButton.grid(row=0,column=1)

        sizeEditFrame.grid(row=2,column=0,pady=5,padx=5, sticky=W+E)
        newStarSize.grid(row=0,column=0)
        sizeCommitButton.grid(row=0,column=1, padx=(60,0))

        deleteSystemButton.grid(row=3,column=0,columnspan=3, pady=(5,10))

def openEditPlanetWindow():
    global currentPlanet
    global currentSector

    def editPlanetCommand(attribute, value):
        
        newValue = value.strip()

        if attribute == "name" and SecGenFunctions.planetNameIsValid(currentSector,newValue) == False:
            messagebox.showerror(title="NAME INVALID", message="Planet names must be unique and at least 1 character long.")
        elif newValue == "":
            messagebox.showerror(title="ENTRY INVALID", message="Entry must be at least 1 character long.")
        else:
            SecGenFunctions.editPlanetValues(currentSector, attribute,currentPlanet,newValue)

            editCleanup()
            editPlanetWindow.grab_release()
            editPlanetWindow.destroy()
    
    def editOrbitalCommand(value):

        numberOfPlanets = SecGenFunctions.systemPlanetCount(currentSector,currentSystem)

        if int(value) == currentPlanetOrbital:
            return

        elif int(value) > numberOfPlanets or int(value) < 1:
            messagebox.showerror(title="ORBIT INVALID", message="Orbial distance cannot be less than 1 or exceed number of planets in the system.")

        else:
            SecGenFunctions.editPlanetOrbial(currentSector, currentPlanet, currentSystem,int(currentPlanetOrbital),int(value))
            editCleanup()
            editPlanetWindow.grab_release()
            editPlanetWindow.destroy()

    def deletePlanetCommand():
        confirmed = messagebox.askyesno(title="DELETE PLANET", message="Are you sure you want to delete this planet? This action cannot be undone.")

        if confirmed:
            SecGenFunctions.deletePlanet(currentSector,currentPlanet)
            editCleanup()
            editPlanetWindow.grab_release()
            editPlanetWindow.destroy()

    #don't open if there is no planet selected
    if currentPlanet == "":
        return

    #create edit planet window
    editPlanetWindow = Toplevel()
    editPlanetWindow.title("Edit Planet")

    editPlanetWindow.grab_set()

    #object creation and display
    instructionLabel = Label(editPlanetWindow,text="EDIT PLANET: " + currentPlanet)
    instructionLabel.grid(row=0,column=0,padx=5,pady=5)
    #-------------------1
    nameEntryFrame = LabelFrame(editPlanetWindow, text="Name", labelanchor=N, padx=5, pady=5) 
    nameEntryFrame.grid(row=1,column=0,padx=5,pady=5, sticky=W+E)

    nameEntryField = Entry(nameEntryFrame, width=15)
    nameEntryField.grid(row=0, column=0, padx=(0,33))
    nameEditButton = Button(nameEntryFrame, text="Commit", command=lambda: editPlanetCommand("name", nameEntryField.get())).grid(row=0,column=1)
    #-------------------2
    sizeFrame = LabelFrame(editPlanetWindow, text="Size", labelanchor=N, padx=5, pady=5)
    sizeFrame.grid(row=2,column=0,pady=5,padx=5, sticky=W+E)

    sizeSelection = StringVar()
    sizeSelection.set("mid")
    newPlanetSize = OptionMenu(sizeFrame, sizeSelection, "small", "mid", "large").grid(row=0,column=0)
    sizeCommitButton = Button(sizeFrame, text="Commit", anchor=E, command=lambda: editPlanetCommand("size", sizeSelection.get())).grid(row=0,column=1, padx=(60,0))
    #-------------------3
    tempEntryFrame = LabelFrame(editPlanetWindow, text="Average Temperature", labelanchor=N, padx=5, pady=5) 
    tempEntryFrame.grid(row=3,column=0,padx=5,pady=5, sticky=W+E)

    tempEntryField = Entry(tempEntryFrame, width=15)
    tempEntryField.grid(row=0, column=0, padx=(0,33))
    tempEditButton = Button(tempEntryFrame, text="Commit", command=lambda: editPlanetCommand("temp", tempEntryField.get())).grid(row=0,column=1)
    #-------------------4
    humidityEntryFrame = LabelFrame(editPlanetWindow, text="Humidity", labelanchor=N, padx=5, pady=5) 
    humidityEntryFrame.grid(row=4,column=0,padx=5,pady=5, sticky=W+E)

    humidityEntryField = Entry(humidityEntryFrame, width=15)
    humidityEntryField.grid(row=0, column=0, padx=(0,33))
    humidityEditButton = Button(humidityEntryFrame, text="Commit", command=lambda: editPlanetCommand("humidity", humidityEntryField.get())).grid(row=0,column=1)
    #-------------------5
    lifeEntryFrame = LabelFrame(editPlanetWindow, text="Life Signs", labelanchor=N, padx=5, pady=5) 
    lifeEntryFrame.grid(row=5,column=0,padx=5,pady=5, sticky=W+E)

    lifeEntryField = Entry(lifeEntryFrame, width=15)
    lifeEntryField.grid(row=0, column=0, padx=(0,33))
    lifeEditButton = Button(lifeEntryFrame, text="Commit", command=lambda: editPlanetCommand("life", lifeEntryField.get())).grid(row=0,column=1)
    #-------------------6
    noteEntryFrame = LabelFrame(editPlanetWindow, text="Note", labelanchor=N, padx=5, pady=5) 
    noteEntryFrame.grid(row=6,column=0,padx=5,pady=5, sticky=W+E)

    noteEntryField = Entry(noteEntryFrame, width=15)
    noteEntryField.grid(row=0, column=0, padx=(0,33))
    noteEditButton = Button(noteEntryFrame, text="Commit", command=lambda: editPlanetCommand("note", noteEntryField.get())).grid(row=0,column=1)
    #-------------------7
    orbitEntryFrame = LabelFrame(editPlanetWindow, text="Orbital Distance", labelanchor=N, padx=5, pady=5) 
    orbitEntryFrame.grid(row=7,column=0,padx=5,pady=5, sticky=W+E)

    orbitEntryField = Entry(orbitEntryFrame, width=15)
    orbitEntryField.grid(row=0, column=0, padx=(0,33))
    orbitEditButton = Button(orbitEntryFrame, text="Commit", command=lambda: editOrbitalCommand(orbitEntryField.get())).grid(row=0,column=1)
    #-------------------8
    deletePlanetButton = Button(editPlanetWindow, text="DELETE PLANET", bg='red', command=deletePlanetCommand).grid(row=8,column=0,pady=5)

def openCreatePlanetWindow():
    global currentSector
    global currentSystem

    def createPlanetCommand():
        if SecGenFunctions.planetNameIsValid(currentSector, nameEntryField.get().strip()) == False:
            messagebox.showerror(title="NAME INVALID", message="Planet names must be unique and at least 1 character long.")
        elif tempEntryField.get().strip() == "":
            messagebox.showerror(title="TEMP INVALID", message="Temperature entry cannot be blank.")
        elif humidityEntryField.get().strip() == "":
            messagebox.showerror(title="HUMIDITY INVALID", message="Humidity entry cannot be blank.")
        elif lifeEntryField.get().strip() == "":
            messagebox.showerror(title="LIFE SIGNS INVALID", message="Life Signs entry cannot be blank.")
        elif noteEntryField.get().strip() == "":
            messagebox.showerror(title="NOTE INVALID", message="Note entry cannot be blank.")
        elif orbitEntryField.get().isnumeric() == False:
            messagebox.showerror(title="ORBIT INVALID", message="Orbial distance must be an integer.")
        elif orbitEntryField.get().strip() == "":
            messagebox.showerror(title="ORBIT INVALID", message="Orbital distance entry cannot be blank.")
        elif int(orbitEntryField.get()) > SecGenFunctions.systemPlanetCount(currentSector,currentSystem)+1 or int(orbitEntryField.get()) < 1:
            messagebox.showerror(title="ORBIT INVALID", message="Orbial distance cannot be less than 1 or exceed number of planets in the system.")
        else:
            SecGenFunctions.createPlanet(currentSector,currentSystem,nameEntryField.get(),sizeSelection.get(),tempEntryField.get(),humidityEntryField.get(),lifeEntryField.get(),noteEntryField.get(),int(orbitEntryField.get()))

            editCleanup()
            createPlanetWindow.grab_release()
            createPlanetWindow.destroy()

    #create edit planet window
    createPlanetWindow = Toplevel()
    createPlanetWindow.title("Create Planet")

    createPlanetWindow.grab_set()

    #object creation and display
    instructionLabel = Label(createPlanetWindow,text="ADD PLANET TO SECTOR " + currentSystem)
    instructionLabel.grid(row=0,column=0,padx=5,pady=5)
    #-------------------1
    nameEntryFrame = LabelFrame(createPlanetWindow, text="Name", labelanchor=N, padx=5, pady=5) 
    nameEntryFrame.grid(row=1,column=0,padx=5,pady=5, sticky=W+E)

    nameEntryField = Entry(nameEntryFrame, width=25)
    nameEntryField.insert(0,currentSystem + "-Neo")
    nameEntryField.grid(row=0, column=0)
    #-------------------2
    sizeFrame = LabelFrame(createPlanetWindow, text="Size", labelanchor=N, padx=5, pady=5)
    sizeFrame.grid(row=2,column=0,pady=5,padx=5, sticky=W+E)

    sizeSelection = StringVar()
    sizeSelection.set("mid")
    newPlanetSize = OptionMenu(sizeFrame, sizeSelection, "small", "mid", "large").grid(row=0,column=0)
    #-------------------3
    tempEntryFrame = LabelFrame(createPlanetWindow, text="Average Temperature", labelanchor=N, padx=5, pady=5) 
    tempEntryFrame.grid(row=3,column=0,padx=5,pady=5, sticky=W+E)

    tempEntryField = Entry(tempEntryFrame, width=25)
    tempEntryField.insert(0,"frozen")
    tempEntryField.grid(row=0, column=0)
    #-------------------4
    humidityEntryFrame = LabelFrame(createPlanetWindow, text="Humidity", labelanchor=N, padx=5, pady=5) 
    humidityEntryFrame.grid(row=4,column=0,padx=5,pady=5, sticky=W+E)

    humidityEntryField = Entry(humidityEntryFrame, width=25)
    humidityEntryField.insert(0,"dry")
    humidityEntryField.grid(row=0, column=0)
    #-------------------5
    lifeEntryFrame = LabelFrame(createPlanetWindow, text="Life Signs", labelanchor=N, padx=5, pady=5) 
    lifeEntryFrame.grid(row=5,column=0,padx=5,pady=5, sticky=W+E)

    lifeEntryField = Entry(lifeEntryFrame, width=25)
    lifeEntryField.insert(0,"lifeless")
    lifeEntryField.grid(row=0, column=0)
    #-------------------6
    noteEntryFrame = LabelFrame(createPlanetWindow, text="Note", labelanchor=N, padx=5, pady=5) 
    noteEntryFrame.grid(row=6,column=0,padx=5,pady=5, sticky=W+E)

    noteEntryField = Entry(noteEntryFrame, width=25)
    noteEntryField.insert(0,"NA")
    noteEntryField.grid(row=0, column=0)
    #-------------------7
    orbitEntryFrame = LabelFrame(createPlanetWindow, text="Orbital Distance", labelanchor=N, padx=5, pady=5) 
    orbitEntryFrame.grid(row=7,column=0,padx=5,pady=5, sticky=W+E)

    orbitEntryField = Entry(orbitEntryFrame, width=15)
    orbitEntryField.insert(0, str(SecGenFunctions.systemPlanetCount(currentSector,currentSystem)+1))
    orbitEntryField.grid(row=0, column=0, padx=(0,33))
    #-------------------8
    createPlanetButton = Button(createPlanetWindow, text="Create", command=createPlanetCommand).grid(row=8, column=0,padx=5,pady=5,sticky=W+E)

def createSectorMap():

    for previousItems in sectorMapFrame.winfo_children():
        previousItems.destroy()

    sector = sqlite3.connect('sectors/' + currentSector)
    cursor = sector.cursor()

    cursor.execute('SELECT * FROM stars')
    sectorStars = cursor.fetchall()

    cursor.execute('SELECT rows FROM sector_data')
    numberOfRows = cursor.fetchone()[0]
    
    cursor.execute('SELECT columns FROM sector_data')
    numberOfColumns = cursor.fetchone()[0]

    sectorMapButtons = []
    buttonCounter = 0

    for r in range(numberOfRows):
        for c in range(numberOfColumns):
            
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
    
    resetCurrents()

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
    cursor.execute('SELECT * FROM planets WHERE star=? ORDER BY orbit', [systemName])
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
        
        newPlanetButton = Button(systemMapFrame, image = icon, bg = 'black', command = functools.partial(planetInfo, planet[1],planet[3],planet[4],planet[5], planet[6], planet[7]))

        planetButtons.append(newPlanetButton)

        planetButtons[counter].grid(row=0,column=counter)

        counter += 1


    createPlanetButton = Button(systemMapFrame, image=addIcon, bg='black', command=openCreatePlanetWindow)
    createPlanetButton.grid(row=0,column=counter+1, padx=10)

    statusUpdate()

    sector.close()

def planetInfo(name, temperature, humidity, life, note, orbit):
    global currentPlanet
    global currentPlanetOrbital

    currentPlanet = name

    currentPlanetOrbital = str(orbit)

    formattedInfo ="NAME: " + name + "\n" + "TEMPERATURE: " + temperature + "\n" + "HUMIDITY: " + humidity +"\n" + "LIFE SIGNS: " + life + "\n" + "NOTE: " + note
    planetInfoLabel.config(text=formattedInfo)

    statusUpdate()

def statusUpdate():
    status.config(text="Sec: " + currentSector + "/Sys: " + currentSystem + "/Pln: " + currentPlanet + "[R:" + selectedRow + "/C:" + selectedColumn + "]" + " POD: " + currentPlanetOrbital, relief=SUNKEN, anchor=E)

def resetCurrents():
    global currentPlanet
    global currentSystem
    global selectedColumn
    global selectedRow
    global currentPlanetOrbital

    currentPlanet = ""
    currentSystem = ""
    selectedColumn = "0"
    selectedRow = "0"
    currentPlanetOrbital = ""

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

def editCleanup():
        clearMaps()
        createSectorMap()
        resetCurrents()
        statusUpdate()

#console object creation
sectorMapFrame = LabelFrame(rootWindow, text="Sector Map: " + currentSector, labelanchor=N,padx=5, pady=5)
welcomeLabel = Label(sectorMapFrame, image=welcomeImage)

starInfoFrame = LabelFrame(rootWindow,text="Star Info", labelanchor=N)
starInfoLabel = Label(starInfoFrame,text="NO STAR LOADED", justify=LEFT)
editStarButton = Button(starInfoFrame, text="Edit Star", command=openEditStarWindow, height=4)

systemMapFrame = LabelFrame(rootWindow, text="System Map", labelanchor=N, padx=5, pady=5)
systemMapFillerImage = Label(systemMapFrame, image=systemMapFiller)

planetInfoFrame = LabelFrame(rootWindow,text="Planet Info", labelanchor=N)
planetInfoLabel = Label(planetInfoFrame,text="NO PLANET LOADED", justify=LEFT)
editPlanetButton = Button(planetInfoFrame, text="Edit Planet", command=openEditPlanetWindow, height=5)

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