import pygame
import time
import math

from renderer import Renderer 
from world import World
from path import Path
from settings import FPS, CHUNK_SIZE

from Buildings.building import Building
from Buildings.belt import Belt

activePlaceable = Building

def checkEvents():
    global activePlaceable
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                for chunk in World.worldData.values():
                    chunk.save()
                pygame.quit()
                quit()

            if event.key == pygame.K_UP:
                Renderer.mainCamera.speed += 3
            if event.key == pygame.K_DOWN:
                Renderer.mainCamera.speed -= 3

            if event.key == pygame.K_1:
                activePlaceable = Building
            if event.key == pygame.K_2:
                activePlaceable = Belt
                    
        if event.type == pygame.MOUSEWHEEL:
            Renderer.mainCamera.changeZoom(event.y*0.1)
            Belt.scaleSprite(Renderer)
        
            

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
            newBuilding = activePlaceable(intWorldMousePos, pygame.Vector2(1, 1))
            newBuilding.place()
        if mousePressed[2]:
            World.removeBuilding(intWorldMousePos)
    
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

Buildings = {"Building": Building,
             "Belt": Belt}

startLoading = time.time()
World.loadAllChunks(Buildings)
print(f"Loading took {time.time() - startLoading} seconds")

frame1 = time.time()
tick = 0
animationFrame = 0
deltaTime = 0
while True:
    # Constantly executing code goes here
    checkEvents()
    checkMousePresses()

    frame2 = time.time()
    if frame2 - frame1 >= 1/FPS:
        #print("FPS: ", 1/deltaTime) if deltaTime != 0 else None
        #print(len(World.worldData))
        deltaTime = frame2 - frame1
        frame1 = frame2
        # Frame based code goes here  
        checkKeys(deltaTime)
        newPath.updateItems(deltaTime)
        Renderer.drawToScreen()

        tick += 1

        if tick % 2 == 0:
            animationFrame += 1
            animationFrame %= 8

            for building in Buildings.values():
                building.scaleSprite(Renderer, animationFrame)
    
