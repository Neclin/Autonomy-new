import pygame

from settings import *

class Camera:
    def __init__(self, x, y, width, height, speed=15):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.speed = speed
        self.zoom = 1
    
    def convertWorldToScreen(self, worldVector):
        return (worldVector - self.position) * TILE_SIZE * self.zoom + pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    def convertScreenToWorld(self, screenVector):
        return (screenVector - pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) / (TILE_SIZE * self.zoom) + self.position

    def convertWorldRectToScreen(self, positon, size):
        return pygame.Rect(self.convertWorldToScreen(positon), size * TILE_SIZE * self.zoom)

    def drawGrid(self, win):
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
    
    def drawCursor(self, win):
        mousePos = pygame.mouse.get_pos()
        mousePos = self.convertScreenToWorld(pygame.Vector2(mousePos[0], mousePos[1]))
        mousePos = mousePos//1
        cursorRect = self.convertWorldRectToScreen(mousePos, pygame.Vector2(1,1))
        pygame.draw.rect(win, (255,255,255), cursorRect, 1, border_radius=int(5*self.zoom))

    def move(self, direction):
        self.position += direction * self.speed / self.zoom
    
    def changeZoom(self, amount):
        self.zoom += amount
        if self.zoom < 0.25:
            self.zoom = 0.25
        if self.zoom > 3:
            self.zoom = 3


class Renderer:
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    mainCamera = Camera(0, 0, SCREEN_WIDTH/TILE_SIZE, SCREEN_HEIGHT/TILE_SIZE, 15)

    objectToDraw = []

    def drawToScreen():
        Renderer.win.fill((51,51,51))

        screenTileHeight = int(SCREEN_HEIGHT // (TILE_SIZE * Renderer.mainCamera.zoom))
        screenTileWidth = int(SCREEN_WIDTH // (TILE_SIZE * Renderer.mainCamera.zoom))
        halfScreenTileHeight = screenTileHeight // 2 + 2
        halfScreenTileWidth = screenTileWidth // 2 + 2
        
        Renderer.mainCamera.drawGrid(Renderer.win)

        Renderer.mainCamera.drawCursor(Renderer.win)
       

        for obj in Renderer.objectToDraw:
            obj.draw(Renderer.win)

        pygame.display.update()
