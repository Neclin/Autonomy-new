import pygame

from world import World

from settings import TILE_SIZE

class Building():
    sprite = None

    def scaleSprite(renderer, animationFrame=0):
        pass

    def __init__(self, position, size):
        self.position = position
        self.size = size
    
    def draw(self, renderer):
        rect = renderer.mainCamera.convertWorldRectToScreen(self.position, self.size)
        if type(self).sprite != None:
            renderer.win.blit(self.sprite, rect)
            return
        pygame.draw.rect(renderer.win, (255,255,255), rect, 1)
    
    def place(self):
        World.addBuilding(self)
    
    def saveString(self):
        return f"Building, {self.position.x}, {self.position.y}, {self.size.x}, {self.size.y}"

    def loadString(string):
        string = string.split(", ")
        position = pygame.Vector2(float(string[1]), float(string[2]))
        size = pygame.Vector2(float(string[3]), float(string[4]))
        return Building(position, size)