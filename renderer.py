import pygame
import math

from settings import *
from world import World
from Buildings.building import Building

class Camera:
    def __init__(self, x, y, width, height, speed=15):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.speed = speed
        self.zoom = 1

        self.mouseDirection = pygame.Vector2(0,0)
    
    def convertWorldToScreen(self, worldVector):
        return (worldVector - self.position) * TILE_SIZE * self.zoom + pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    def convertScreenToWorld(self, screenVector):
        return (screenVector - pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) / (TILE_SIZE * self.zoom) + self.position

    def convertWorldRectToScreen(self, position, size):
        dimensions = size * TILE_SIZE * self.zoom
        dimensions.x, dimensions.y = math.ceil(dimensions.x), math.ceil(dimensions.y)
        return pygame.Rect(self.convertWorldToScreen(position), dimensions)

    def drawGrid(self):
        # Draw Grid
        halfNumberOfTilesHeight = int(self.size.y / self.zoom // 2) + 2
        halfNumberOfTilesWidth = int(self.size.x  / self.zoom // 2) + 2

        for LineX in range(-halfNumberOfTilesHeight, halfNumberOfTilesHeight+1, 1):
            topPoint = pygame.Vector2(LineX, -halfNumberOfTilesHeight) + self.position//1
            bottomPoint = pygame.Vector2(LineX, halfNumberOfTilesHeight) + self.position//1
            topPoint = self.convertWorldToScreen(topPoint)
            bottomPoint = self.convertWorldToScreen(bottomPoint)
            pygame.draw.line(Renderer.win, GRID_COLOUR, topPoint, bottomPoint, 1)

        for lineY in range(-halfNumberOfTilesWidth, halfNumberOfTilesWidth+1, 1):
            leftPoint = pygame.Vector2(-halfNumberOfTilesWidth, lineY) + self.position//1
            rightPoint = pygame.Vector2(halfNumberOfTilesWidth, lineY) + self.position//1
            leftPoint = self.convertWorldToScreen(leftPoint)
            rightPoint = self.convertWorldToScreen(rightPoint)
            pygame.draw.line(Renderer.win, GRID_COLOUR, leftPoint, rightPoint, 1)
    
    def drawCursor(self):
        mousePos = pygame.mouse.get_pos()
        mousePos = self.convertScreenToWorld(pygame.Vector2(mousePos[0], mousePos[1]))
        mousePos = mousePos//1
        cursorRect = self.convertWorldRectToScreen(mousePos, pygame.Vector2(1,1))
        pygame.draw.rect(Renderer.win, (255,255,255), cursorRect, 1, border_radius=int(5*self.zoom))

        # draw line pointing in mouse direction
        pygame.draw.line(Renderer.win, (255,255,255), cursorRect.center, cursorRect.center + self.mouseDirection*TILE_SIZE//2, 1)

    def move(self, direction):
        self.position += direction * self.speed / self.zoom
    
    def changeZoom(self, amount):
        self.zoom += amount
        if self.zoom < 0.5:
            self.zoom = 0.5
        if self.zoom > 2:
            self.zoom = 2


class Renderer:
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    mainCamera = Camera(0, 0, SCREEN_WIDTH/TILE_SIZE, SCREEN_HEIGHT/TILE_SIZE, 15)


    def drawToScreen():
        Renderer.win.fill((51,51,51))
        
        Renderer.mainCamera.drawGrid()

        Renderer.mainCamera.drawCursor()
       
        Renderer.drawChunks()

        pygame.display.update()

    def drawChunks():
        centerChunkPosition = Renderer.mainCamera.position//CHUNK_SIZE
        numberOfChunksWidth = int(Renderer.mainCamera.size.x / Renderer.mainCamera.zoom // CHUNK_SIZE // 2) +  1
        numberOfChunksHeight = int(Renderer.mainCamera.size.y / Renderer.mainCamera.zoom // CHUNK_SIZE // 2) + 1
        for chunkX in range(-numberOfChunksWidth, numberOfChunksWidth+1, 1):
            for chunkY in range(-numberOfChunksHeight, numberOfChunksHeight+1, 1):
                chunkPosition = pygame.Vector2(chunkX, chunkY) + centerChunkPosition
                if World.worldData.get(str(chunkPosition)) != None:
                    chunk = World.worldData[str(chunkPosition)]
                    chunk.draw(Renderer)  

                # For loading chunks when they are visible to the player  
                # else:
                #     World.loadChunk(Building, chunkPosition)

