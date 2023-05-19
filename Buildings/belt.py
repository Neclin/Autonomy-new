import pygame
import math

from settings import TILE_SIZE

from Buildings.building import Building

spriteSheet = pygame.image.load("Assets/sprites.png")
beltSpriteSheetStraight = [spriteSheet.subsurface((i*32, 0, 32, 32)) for i in range(8)]
beltSpriteSheetStraight90 = [pygame.transform.rotate(beltSpriteSheetStraight[i], 90) for i in range(8)]
beltSpriteSheetStraight180 = [pygame.transform.rotate(beltSpriteSheetStraight[i], 180) for i in range(8)]
beltSpriteSheetStraight270 = [pygame.transform.rotate(beltSpriteSheetStraight[i], 270) for i in range(8)]


class Belt(Building):
    straightSpriteSheets = [beltSpriteSheetStraight, beltSpriteSheetStraight90, beltSpriteSheetStraight180, beltSpriteSheetStraight270]

    def __init__(self, position, size, startDirection, endDirection):
        super().__init__(position, size)
        self.startDirection = startDirection
        self.endDirection = endDirection
        angle = self.startDirection.angle_to(pygame.Vector2(1, 0))
        angle += 360
        angle %= 360
        self.spriteSheet = Belt.straightSpriteSheets[int(angle//90)]
        self.sprite = self.spriteSheet[0].subsurface(0, 0, 32, 32)
        self.linkedPath = None
    
    def updateSprite(self, renderer):
        self.sprite = self.spriteSheet[renderer.animationFrame].subsurface(0, 0, 32, 32)
        self.sprite = pygame.transform.scale(self.sprite, (math.ceil(TILE_SIZE*renderer.mainCamera.zoom), math.ceil(TILE_SIZE*renderer.mainCamera.zoom)))

    def draw(self, renderer):
        self.updateSprite(renderer)
        super().draw(renderer)
    
    def saveString(self):
        return f"Belt, {self.position.x}, {self.position.y}, {self.size.x}, {self.size.y}, {self.startDirection.x}, {self.startDirection.y}, {self.endDirection.x}, {self.endDirection.y}"

    def loadString(string):
        string = string.split(", ")
        position = pygame.Vector2(float(string[1]), float(string[2]))
        size = pygame.Vector2(float(string[3]), float(string[4]))
        startDirection = pygame.Vector2(float(string[5]), float(string[6]))
        endDirection = pygame.Vector2(float(string[7]), float(string[8]))
        return Belt(position, size, startDirection, endDirection)

    def place(self):
        if super().place():
            print("Belt placed")
            print("start direction: ", self.startDirection)
            print("end direction: ", self.endDirection)

    def getPaths(self):
        pass