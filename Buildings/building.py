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
        topLeft = self.position // TILE_SIZE
        bottomRight = (self.position + self.size) // TILE_SIZE
        for x in range(int(topLeft.x), int(bottomRight.x)+1):
            for y in range(int(topLeft.y), int(bottomRight.y)+1):
                if x == topLeft.x and y == topLeft.y:
                    World.addBuilding(self, pygame.Vector2(x,y))
                else:
                    World.addBuilding("Filled", pygame.Vector2(x,y))
    
    def whenPlaced(self):
        pass

    def remove(self):
        chunkPosition = self.position // TILE_SIZE
        chunk = World.worldData.get(str(chunkPosition))
        if chunk == None:
            return False
        del chunk.chunkData[str(self.position)]
        return True