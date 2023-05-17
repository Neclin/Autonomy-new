import pygame
import math

from settings import TILE_SIZE

from Buildings.building import Building

spriteSheet = pygame.image.load("Assets/sprites.png")

class Belt(Building):
    beltSpriteSheet = [spriteSheet.subsurface((i*32, 0, 32, 32)) for i in range(8)]
    sprite = beltSpriteSheet[0].subsurface(0, 0, 32, 32)

    def scaleSprite(renderer, animationFrame=0):
        Belt.sprite = Belt.beltSpriteSheet[animationFrame].subsurface(0, 0, 32, 32)
        Belt.sprite = pygame.transform.scale(Belt.sprite, (math.ceil(TILE_SIZE*renderer.mainCamera.zoom), math.ceil(TILE_SIZE*renderer.mainCamera.zoom)))

    def __init__(self, position, size, direction="right"):
        super().__init__(position, size)
        self.direction = direction
    
    def draw(self, renderer):
        super().draw(renderer)
    
    def saveString(self):
        return f"Belt, {self.position.x}, {self.position.y}, {self.size.x}, {self.size.y}, {self.direction}"

    def loadString(string):
        string = string.split(", ")
        position = pygame.Vector2(float(string[1]), float(string[2]))
        size = pygame.Vector2(float(string[3]), float(string[4]))
        direction = string[5]
        return Belt(position, size, direction)