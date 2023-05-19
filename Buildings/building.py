import pygame

from world import World

from settings import TILE_SIZE

class Building():
    sprite = None

    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.sprite == None
    
    def draw(self, renderer):
        rect = renderer.mainCamera.convertWorldRectToScreen(self.position, self.size)
        if self.sprite != None:
            renderer.win.blit(self.sprite, rect)
            return
        pygame.draw.rect(renderer.win, (255,255,255), rect, 1)
    
    def saveString(self):
        return f"Building, {self.position.x}, {self.position.y}, {self.size.x}, {self.size.y}"

    def loadString(string):
        string = string.split(", ")
        position = pygame.Vector2(float(string[1]), float(string[2]))
        size = pygame.Vector2(float(string[3]), float(string[4]))
        return Building(position, size)
    
    def place(self):
        return World.addBuilding(self)
    
    def whenPlaced(self):
        pass

    def remove(self):
        chunkPosition = self.position // TILE_SIZE
        chunk = World.worldData.get(str(chunkPosition))
        if chunk == None:
            return False
        del chunk.chunkData[str(self.position)]
        return True