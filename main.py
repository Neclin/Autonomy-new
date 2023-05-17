import pygame
import time
import math

from renderer import Renderer 
from world import World
from path import Path
from settings import FPS

from Buildings.building import Building

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.key == pygame.K_UP:
                Renderer.mainCamera.speed += 3
            if event.key == pygame.K_DOWN:
                Renderer.mainCamera.speed -= 3
                    
        if event.type == pygame.MOUSEWHEEL:
            Renderer.mainCamera.changeZoom(event.y*0.2)
        
            

def checkKeys(deltaTime):
    heldKeys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)
    if heldKeys[pygame.K_w]:
        direction.y = -1
    if heldKeys[pygame.K_s]:
        direction.y = 1
    if heldKeys[pygame.K_a]:
        direction.x = -1
    if heldKeys[pygame.K_d]:
        direction.x = 1
    
    Renderer.mainCamera.move(direction * deltaTime)

def checkMousePresses():
    mousePressed = pygame.mouse.get_pressed(3)
    if mousePressed:
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])
        worldMousePos = Renderer.mainCamera.convertScreenToWorld(mousePos)
        intWorldMousePos = pygame.Vector2(math.floor(worldMousePos.x), math.floor(worldMousePos.y))
        if mousePressed[0]:
            # newPath.addPoint(worldMousePos.x, worldMousePos.y)
            newBuilding = Building(intWorldMousePos, pygame.Vector2(1, 1))
            newBuilding.place()
        if mousePressed[2]:
            newPath.addItem(0)
    
def quadraticBezier(p0, p1, p2, t):
    return (1-t)**2 * p0 + 2*(1-t)*t*p1 + t**2 * p2

newPath = Path()
newPath.addPoint(0, 0)
newPath.addPoint(0, 4)
newPath.addPoint(4, 4)
newPath.addPoint(4, 0)
# newPath.addItem(0.50)
# newPath.addItem(0.75)
# newPath.addItem(0.50)
# newPath.addItem(0.33)
# newPath.addItem(0)

World.addChunk(pygame.Vector2(0, 0))
World.addBuilding(Building(pygame.Vector2(0, 0), pygame.Vector2(1, 1)))

frame1 = time.time()
deltaTime = 0
while True:
    # Constantly executing code goes here
    checkEvents()
    checkMousePresses()

    frame2 = time.time()
    if frame2 - frame1 >= 1/FPS:
        deltaTime = frame2 - frame1
        frame1 = frame2
        # Frame based code goes here  
        checkKeys(deltaTime)
        newPath.updateItems(deltaTime)
        Renderer.drawToScreen()
    
