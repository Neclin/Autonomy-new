import pygame

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
        with open("Chunks/"+str(self.position)+".txt", "w") as file:
            for building in self.gameObject:
                file.write(building.saveString()+"\n")

class World:
    worldData = {}

    def addChunk(position):
        World.worldData[str(position)] = Chunk(position)

    def loadChunk(Building, position):
        try:
            with open("Chunks/"+str(position)+".txt", "r") as file:
                chunk = Chunk(position)
                for line in file:
                    line = line.strip()
                    if line.startswith("Building"):
                        chunk.addBuilding(Building.loadString(line))
                World.worldData[str(position)] = chunk
        except FileNotFoundError:
            pass

    def addBuilding(building):
        chunkPosition = building.position//CHUNK_SIZE
        if World.worldData.get(str(chunkPosition)) == None:
            World.addChunk(chunkPosition)
        World.worldData[str(chunkPosition)].addBuilding(building)
