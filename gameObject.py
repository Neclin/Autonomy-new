import pygame
import random

from settings import TILE_SIZE, COPPER_ORE

spriteSheet = pygame.image.load("Assets/Copper Ore.png")
spriteSize = 1024
spriteSheetWidth = 8
spriteSheetHeight = 5

class GameObject():
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.colour = None
        self.sprite = None
        self.index = random.randint(0, 39)

        # row = self.index // spriteSheetWidth
        # column = self.index % spriteSheetWidth

        # self.sprite = spriteSheet.subsurface(column * spriteSize, row * spriteSize, spriteSize, spriteSize)
        # self.scaledSprite = pygame.transform.scale(self.sprite, self.size * TILE_SIZE)


    def draw(self, renderer):
        rect = renderer.mainCamera.convertWorldRectToScreen(self.position, self.size)
        if self.sprite != None and renderer.mainCamera.zoom > 0.3:
            self.scaledSprite = pygame.transform.scale(self.sprite, self.size * TILE_SIZE*renderer.mainCamera.zoom)
            renderer.win.blit(self.scaledSprite, rect)
            return
        elif self.colour != None:
            pygame.draw.rect(renderer.win, self.colour, rect)
        else:
            pygame.draw.rect(renderer.win, (255, 255, 255), rect, 1)
    
    def saveString(self):
        return f"GameObject(pygame.Vector2({self.position.x}, {self.position.y}), pygame.Vector2({self.size.x}, {self.size.y}))"
