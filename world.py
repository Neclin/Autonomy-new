import pygame
import os

from settings import CHUNK_SIZE, DEBUG_COLOUR

from gameObject import GameObject

class Chunk:
    def __init__(self, position):
        self.position = position
        self.paths = []
        self.chunkData = {}
        self.size = pygame.Vector2(CHUNK_SIZE, CHUNK_SIZE)
    
    def draw(self, renderer):
        self.drawChunk(renderer)   
        for gameObject in self.chunkData.values():
            if type(gameObject) == str:
                continue
            gameObject.draw(renderer)

    def addGameObject(self, gameObject):
        if self.chunkData.get(str(gameObject.position)) != None:
            return False
        self.chunkData[str(gameObject.position)] = gameObject
        return True

    def addBuilding(self, building, position):
        if self.chunkData.get(str(position)) != None:
            return False
        self.chunkData[str(position)] = building
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
    paths = {}

    cursorSize = 1

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
                World.worldData[str(chunk.position)] = chunk
                for line in file:
                    building = eval(line)
                    chunk.addBuilding(building, building.position)
        except FileNotFoundError:
            pass

    def addGameObject(gameObject):
        for cellY in range(int(gameObject.position.y), int(gameObject.position.y + gameObject.size.y)):
            for cellX in range(int(gameObject.position.x), int(gameObject.position.x + gameObject.size.x)):
                # print(cellX, cellY, gameObject.position, gameObject.size)
                if World.addGameObjectAtPosition(gameObject, pygame.Vector2(cellX, cellY)) == False:
                    return False

    def addGameObjectAtPosition(gameObject, position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        return World.worldData[str(chunkPosition)].addGameObject(gameObject)

    def removeGameObject(position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            return False
        chunk = World.worldData[str(chunkPosition)]
        if chunk.chunkData.get(str(position)) == None:
            return False
        del (chunk.chunkData[str(position)])
        return True

    def addBuilding(building, position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        return World.worldData[str(chunkPosition)].addBuilding(building, position)
    
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
        pathPoint = path.firstPathPoint.position
        if World.paths.get(str(pathPoint)) != None:
            print("Path already exists")
            return False
        World.paths[str(pathPoint)] = path
    
    def getBuildingAtPosition(position):
        chunkPosition = position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            return None
        return World.worldData[str(chunkPosition)].chunkData.get(str(position))
