import SecGenSources
import sqlite3
import random

tempDBName = "default"
tempStarNumber = 5
tempGridSize = 5

def generateSector(sectorName, numberOfStars, gridSize):

    usedStarNames = []
    usedSectorCoordinates = []

    #create database/sector
    sector = sqlite3.connect('sectors/' + sectorName +'.db')
    cursor = sector.cursor()

    #create stars table
    cursor.execute("CREATE TABLE stars (name text,size text,row text,column text)")

    #populate stars table
    for _ in range(numberOfStars):
        newStarName = random.choice(SecGenSources.starNames)
        newStarSize = random.choice(SecGenSources.starSizes)

    #create planets table
    cursor.execute("""
        CREATE TABLE planets (
            name text,
            size text,
            average_temp text,
            humidity text,
            life text,
            note text)
        """)

    sector.commit()
    sector.close()


generateSector(tempDBName, tempStarNumber, tempGridSize)