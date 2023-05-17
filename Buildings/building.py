import pygame

from world import World

from renderer import Renderer
from settings import TILE_SIZE

class Building():
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.sprite = None
    
    def draw(self, win):
        if self.sprite != None:
            pass
        rect = Renderer.mainCamera.convertWorldRectToScreen(self.position, self.size)
        pygame.draw.rect(win, (255,255,255), rect, 1)
    
    def place(self):
        World.addBuilding(self)