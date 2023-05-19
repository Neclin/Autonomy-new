import pygame
import os

from settings import CHUNK_SIZE, DEBUG_COLOUR

class Chunk:
    def __init__(self, position):
        self.position = position
        self.paths = []
        self.chunkData = {}
        self.size = pygame.Vector2(CHUNK_SIZE, CHUNK_SIZE)
    
    def draw(self, renderer):
        self.drawChunk(renderer)   
        for building in self.chunkData.values():
            building.draw(renderer)
        for path in self.paths:
            path.draw(renderer)

    def addBuilding(self, building):
        if self.chunkData.get(str(building.position)) != None:
            return False
        self.chunkData[str(building.position)] = building
        building.whenPlaced()
        return True
    
    def addPath(self, path):
        self.paths.append(path)
    
    def drawChunk(self, renderer):
        rect = renderer.mainCamera.convertWorldRectToScreen(self.position * CHUNK_SIZE, self.size)
        pygame.draw.rect(renderer.win, DEBUG_COLOUR, rect, 1)
    
    def save(self):
        if self.chunkData == {}:
            if os.path.isfile("Chunks/"+str(self.position)+".txt"):
                os.remove("Chunks/"+str(self.position)+".txt")
            return
        with open("Chunks/"+str(self.position)+".txt", "w") as file:
            for building in self.chunkData.values():
                file.write(building.saveString()+"\n")

class World:
    worldData = {}

    def addChunk(position):
        World.worldData[str(position)] = Chunk(position)

    def loadAllChunks(Buildings):
        chunkDirectory = os.listdir("Chunks")
        for filePath in chunkDirectory:
            World.loadChunk(Buildings, filePath)

    def loadChunk(Buildings, fileName):
        try:
            with open("Chunks/"+fileName, "r") as file:
                try:
                    chunk = fileName.removeprefix("[")
                    chunk = chunk.removesuffix("].txt")
                except:
                    chunk = fileName.lstrip("[")
                    chunk = chunk.rstrip("].txt")
                chunk = chunk.split(",")
                chunk = pygame.Vector2(int(chunk[0]), int(chunk[1]))
                chunk = Chunk(chunk)
                print(chunk.paths)
                World.worldData[str(chunk.position)] = chunk
                for line in file:
                    line = line.strip()
                    firstWorld = line.split(",")[0]
                    building = Buildings[firstWorld].loadString(line)
                    chunk.addBuilding(building)
                print(chunk.paths)
        except FileNotFoundError:
            pass

    def addBuilding(building):
        chunkPosition = building.position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        return World.worldData[str(chunkPosition)].addBuilding(building)
    
    def removeBuilding(position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            return False
        chunk = World.worldData[str(chunkPosition)]
        building = chunk.chunkData.get(str(position))
        if building == None:
            return False
        building.remove()
        return True
        

    def addPath(path):
        chunkPosition = path.pointsHead.position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        World.worldData[str(chunkPosition)].addPath(path)
    
    def getBuildingAtPosition(position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            return None
        return World.worldData[str(chunkPosition)].chunkData.get(str(position))
