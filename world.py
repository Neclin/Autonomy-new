import pygame

from settings import CHUNK_SIZE

class Chunk:
    def __init__(self, position):
        self.position = position
        self.gameObject = []
        self.chunkData = {}
        self.size = pygame.Vector2(CHUNK_SIZE, CHUNK_SIZE)
    
    def draw(self, win):
        for gameObject in self.gameObject:
            gameObject.draw(win)

    def addBuilding(self, building):
        if self.chunkData.get(str(building.position)) != None:
            return
        self.gameObject.append(building)
        self.chunkData[str(building.position)] = building

class World:
    worldData = {}

    def addChunk(position):
        World.worldData[str(position)] = Chunk(position)

    def addBuilding(building):
        chunkPosition = building.position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        World.worldData[str(chunkPosition)].addBuilding(building)
