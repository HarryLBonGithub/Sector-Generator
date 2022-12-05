import SecGenSources
import sqlite3
import random

tempStarNumber = 5
tempGridSize = 10

def generateSector(sectorName, numberOfStars, rowSize, columnSize):
    
    usedStarNames = []
    usedSectorCoordinates = []

    #create database/sector
    sector = sqlite3.connect('sectors/' + sectorName +'.db')
    cursor = sector.cursor()

    #create and populate sector_data table

    cursor.execute("CREATE TABLE sector_data (name text, rows integer, columns integer)")
    sector.commit()

    cursor.execute("INSERT INTO sector_data VALUES (?,?,?)", (sectorName, rowSize, columnSize))
    sector.commit()

    #create stars table
    cursor.execute("CREATE TABLE stars (name text,size text,row text,column text)")

    #populate stars table
    for _ in range(numberOfStars):

        newStarName = random.choice(SecGenSources.starNames)

        while newStarName in usedStarNames:
            newStarName = random.choice(SecGenSources.starNames)
        
        usedStarNames.append(newStarName)

        newStarSize = random.choice(SecGenSources.starSizes)

        newRow = str(random.randrange(1, rowSize+1))
        newColumn = str(random.randrange(1, columnSize+1))
        newCoordinates = newRow + newColumn

        while newCoordinates in usedSectorCoordinates:
            newRow = str(random.randrange(1, rowSize+1))
            newColumn = str(random.randrange(1, columnSize+1))
            newCoordinates = newRow + newColumn
        
        #print("Star: " + newStarName +" Size: " + newStarSize + " Sec X: " + newColumn + " Sec Y: " + newRow)

        cursor.execute("INSERT INTO stars VALUES (?,?,?,?)", (newStarName, newStarSize, newRow, newColumn))
        sector.commit()

    #create planets table
    cursor.execute("""
        CREATE TABLE planets (
            star text,
            name text,
            size text,
            average_temp text,
            humidity text,
            life text,
            note text,
            orbit integer)
        """)
    
    #populate planets table

    #Create a list of stars
    cursor.execute("SELECT name FROM stars")
    sectorStars = [i[0] for i in cursor.fetchall()]

    #create planets for each star
    for star in sectorStars:
        numberOfPlanets = random.randrange(1,11)
        orbitalDistance = 1
        for planet in range(0, numberOfPlanets):
            
            newPlanetStar = star

            newPlanetName = star +"-"+SecGenSources.planetSuffixes[planet]

            newPlanetSize = random.choice(SecGenSources.planetSizes)
            newPlanetTemp = random.choice(SecGenSources.planetTemp)
            newPlanetHumidity = random.choice(SecGenSources.planetHumidity)
            newPlanetLife = random.choice(SecGenSources.planetLifeSigns)
            newPlanetNote = random.choice(SecGenSources.planetNote)

            cursor.execute("INSERT INTO planets VALUES (?,?,?,?,?,?,?,?)", 
            (newPlanetStar, newPlanetName, newPlanetSize, newPlanetTemp, newPlanetHumidity,newPlanetLife,newPlanetNote,orbitalDistance))
            sector.commit()
            orbitalDistance +=1

    sector.commit()
    sector.close()

def generateStarSystem(sectorName, starName, size, numberOfPlanets, row, column):
    #connect to sector database

    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    cursor.execute("INSERT INTO stars VALUES (?,?,?,?)", (starName, size, row, column))
    sector.commit()

    orbitalDistance = 1

    for planet in range(0, int(numberOfPlanets)):
            
            newPlanetStar = starName

            newPlanetName = starName +"-"+SecGenSources.planetSuffixes[planet]

            newPlanetSize = random.choice(SecGenSources.planetSizes)
            newPlanetTemp = random.choice(SecGenSources.planetTemp)
            newPlanetHumidity = random.choice(SecGenSources.planetHumidity)
            newPlanetLife = random.choice(SecGenSources.planetLifeSigns)
            newPlanetNote = random.choice(SecGenSources.planetNote)

            cursor.execute("INSERT INTO planets VALUES (?,?,?,?,?,?,?,?)", 
            (newPlanetStar, newPlanetName, newPlanetSize, newPlanetTemp, newPlanetHumidity,newPlanetLife,newPlanetNote,orbitalDistance))
            sector.commit()
            orbitalDistance +=1
    
    sector.close()

def deleteStarSystem(sectorName, starName):
    #connect to sector database

    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    cursor.execute("DELETE FROM stars WHERE name = ? ", [starName])
    sector.commit()

    cursor.execute("DELETE FROM planets WHERE star = ?", [starName])
    sector.commit()

    sector.close()

def editStarName(sectorName, originalName, newName):
    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    cursor.execute("UPDATE planets SET star = ? WHERE star = ?", (newName, originalName))
    sector.commit()

    cursor.execute("UPDATE stars SET name = ? WHERE name = ?", (newName, originalName))
    sector.commit()
    sector.close()

def editStarSize(sectorName, starName, size):

    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    cursor.execute("UPDATE stars SET size = ? WHERE name = ?", (size, starName))

    sector.commit()
    sector.close()

def editPlanetValues(sectorName, attribute, planet, value):
    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()
    
    if attribute == "name":
        cursor.execute("UPDATE planets SET name = ? WHERE name = ?", (value,planet))
    elif attribute == "size":
        cursor.execute("UPDATE planets SET size = ? WHERE name = ?", (value,planet))
    elif attribute == "temp":
        cursor.execute("UPDATE planets SET average_temp = ? WHERE name = ?", (value,planet))
    elif attribute == "humidity":
        cursor.execute("UPDATE planets SET humidity = ? WHERE name = ?", (value,planet))
    elif attribute == "life":
        cursor.execute("UPDATE planets SET life = ? WHERE name = ?", (value,planet))
    elif attribute == "note":
        cursor.execute("UPDATE planets SET note = ? WHERE name = ?", (value,planet))
    sector.commit()
    sector.close()

def editPlanetOrbial(sectorName, planet, system, startingOrbit, newOrbit):
    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    if startingOrbit < newOrbit:
        cursor.execute('UPDATE planets SET orbit = orbit - 1 WHERE (star = ? AND orbit > ? and orbit <= ?)',
        (system,startingOrbit,newOrbit))
        sector.commit()

        cursor.execute('UPDATE planets SET orbit = ? WHERE name = ?',
        (newOrbit, planet))
        sector.commit()
        sector.close()

    if startingOrbit > newOrbit:
        cursor.execute('UPDATE planets SET orbit = orbit + 1 WHERE (star = ? AND orbit < ? and orbit >= ?)',
        (system,startingOrbit,newOrbit))
        sector.commit()

        cursor.execute('UPDATE planets SET orbit = ? WHERE name = ?',
        (newOrbit, planet))
        sector.commit()
        sector.close()

def nameIsValid(sectorName, newName):

        sector = sqlite3.connect('sectors/' + sectorName)
        cursor = sector.cursor()

        cursor.execute('SELECT * FROM stars')
        sectorStars = cursor.fetchall()

        for star in sectorStars:
            if newName == star[0]:
                return False
        if newName == "" or newName == "NA":
            return False

        sector.close()

        return True

def planetNameIsValid(sectorName, newName):

        sector = sqlite3.connect('sectors/' + sectorName)
        cursor = sector.cursor()

        cursor.execute('SELECT * FROM planets')
        sectorPlanets = cursor.fetchall()

        for planet in sectorPlanets:
            if newName == planet[1]:
                return False
        if newName == "" or newName == "NA":
            return False

        sector.close()

        return True

def systemPlanetCount(sectorName, system):
    sector = sqlite3.connect('sectors/' + sectorName)
    cursor = sector.cursor()

    cursor.execute('SELECT * FROM planets WHERE star = ?', [system])
    sectorPlanets = cursor.fetchall()

    return len(sectorPlanets)