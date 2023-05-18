import pygame
import os

from settings import CHUNK_SIZE, DEBUG_COLOUR

class Chunk:
    def __init__(self, position):
        self.position = position
        self.gameObject = []
        self.chunkData = {}
        self.size = pygame.Vector2(CHUNK_SIZE, CHUNK_SIZE)
    
    def draw(self, renderer):
        for gameObject in self.gameObject:
            gameObject.draw(renderer)
        self.drawChunk(renderer)    

    def addBuilding(self, building):
        if self.chunkData.get(str(building.position)) != None:
            return
        self.gameObject.append(building)
        self.chunkData[str(building.position)] = building
    
    def drawChunk(self, renderer):
        rect = renderer.mainCamera.convertWorldRectToScreen(self.position * CHUNK_SIZE, self.size)
        pygame.draw.rect(renderer.win, DEBUG_COLOUR, rect, 1)
    
    def save(self):
        if self.gameObject == []:
            os.remove("Chunks/"+str(self.position)+".txt")
            return
        with open("Chunks/"+str(self.position)+".txt", "w") as file:
            for building in self.gameObject:
                file.write(building.saveString()+"\n")

class World:
    worldData = {}

    def addChunk(position):
        World.worldData[str(position)] = Chunk(position)

    def loadAllChunks(Buildings):
        chunkDirectory = os.listdir("Chunks")
        for chunk in chunkDirectory:
            try:
                chunk = chunk.removeprefix("[")
                chunk = chunk.removesuffix("].txt")
            except:
                chunk = chunk.lstrip("[")
                chunk = chunk.rstrip("].txt")
            chunk = chunk.split(",")
            chunk = pygame.Vector2(int(chunk[0]), int(chunk[1]))
            World.loadChunk(Buildings, chunk)

    def loadChunk(Buildings, position):
        try:
            with open("Chunks/"+str(position)+".txt", "r") as file:
                chunk = Chunk(position)
                for line in file:
                    line = line.strip()
                    firstWorld = line.split(",")[0]
                    chunk.addBuilding(Buildings[firstWorld].loadString(line))
                World.worldData[str(position)] = chunk
        except FileNotFoundError:
            pass

    def addBuilding(building):
        chunkPosition = building.position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        World.worldData[str(chunkPosition)].addBuilding(building)
    
    def removeBuilding(position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            return
        chunk = World.worldData[str(chunkPosition)]
        for building in chunk.gameObject:
            if building.position == position:
                chunk.gameObject.remove(building)
                del chunk.chunkData[str(position)]
                break
