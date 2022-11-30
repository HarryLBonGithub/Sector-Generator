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
            note text)
        """)
    
    #populate planets table

    #Create a list of stars
    cursor.execute("SELECT name FROM stars")
    sectorStars = [i[0] for i in cursor.fetchall()]

    #create planets for each star
    for star in sectorStars:
        numberOfPlanets = random.randrange(1,11)
        for planet in range(0, numberOfPlanets):
            
            newPlanetStar = star

            newPlanetName = star +"-"+SecGenSources.planetSuffixes[planet]

            newPlanetSize = random.choice(SecGenSources.planetSizes)
            newPlanetTemp = random.choice(SecGenSources.planetTemp)
            newPlanetHumidity = random.choice(SecGenSources.planetHumidity)
            newPlanetLife = random.choice(SecGenSources.planetLifeSigns)
            newPlanetNote = random.choice(SecGenSources.planetNote)

            cursor.execute("INSERT INTO planets VALUES (?,?,?,?,?,?,?)", 
            (newPlanetStar, newPlanetName, newPlanetSize, newPlanetTemp, newPlanetHumidity,newPlanetLife,newPlanetNote))
            sector.commit()

    sector.commit()
    sector.close()