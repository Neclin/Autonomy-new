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
            
            if event.key == pygame.K_z:
                mousePosition = pygame.mouse.get_pos()
                mousePosition = Renderer.mainCamera.convertScreenToWorld(pygame.Vector2(mousePosition[0], mousePosition[1]))
                buildingPosition = mousePosition//1
                mouseChunk = mousePosition//CHUNK_SIZE
                chunk = World.worldData.get(str(mouseChunk))
                if chunk != None:
                    building = chunk.chunkData.get(str(buildingPosition))
                    if type(building) == Belt:
                        building.linkedPath.addItem(0)

        if event.type == pygame.MOUSEWHEEL:
            Renderer.mainCamera.changeZoom(event.y*0.1)
        
        if event.type == pygame.MOUSEMOTION:
            relativeMouseVector = pygame.Vector2(event.rel[0], event.rel[1])
            if abs(relativeMouseVector.x) > abs(relativeMouseVector.y):
                relativeMouseVector.y = 0
            else:
                relativeMouseVector.x = 0
            if relativeMouseVector.length() != 0:
                relativeMouseVector = relativeMouseVector.normalize()
            Renderer.mainCamera.mouseDirection = relativeMouseVector

            

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

directionVector = pygame.Vector2(1, 0)

def checkMousePresses():
    mousePressed = pygame.mouse.get_pressed(3)
    if mousePressed:
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])
        worldMousePos = Renderer.mainCamera.convertScreenToWorld(mousePos)
        intWorldMousePos = pygame.Vector2(math.floor(worldMousePos.x), math.floor(worldMousePos.y))
        if mousePressed[0]:
            if activePlaceable == Building:
                newBuilding = activePlaceable(intWorldMousePos, pygame.Vector2(1, 1))
            elif activePlaceable == Belt:
                # newBuilding = activePlaceable(intWorldMousePos, pygame.Vector2(1, 1), Renderer.mainCamera.mouseDirection, Renderer.mainCamera.mouseDirection)
                newBuilding = activePlaceable(intWorldMousePos, pygame.Vector2(1, 1), directionVector, directionVector)
            newBuilding.place()
        if mousePressed[2]:
            World.removeBuilding(intWorldMousePos)
    
def quadraticBezier(p0, p1, p2, t):
    return (1-t)**2 * p0 + 2*(1-t)*t*p1 + t**2 * p2

Buildings = {"Building": Building,
             "Belt": Belt}

startLoading = time.time()
World.loadAllChunks(Buildings)
print(f"Loading took {time.time() - startLoading} seconds")

newPath = Path()
newPath.addPoint(pygame.Vector2(1, 1))
newPath.addPoint(pygame.Vector2(2, 1))
newPath.addPoint(pygame.Vector2(3, 1))
newPath.addPoint(pygame.Vector2(4, 2))
newPath.addPoint(pygame.Vector2(3, 2))
newPath.addPoint(pygame.Vector2(2, 6))
World.addPath(newPath)
newPath.addItem(0.3)
newPath.addItem(0.5)
newPath.addItem(0.3)

# newPath.printPathPoints()

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

        Renderer.drawToScreen(deltaTime)

        tick += 1

        if tick % 2 == 0:
            Renderer.animationFrame += 1
            Renderer.animationFrame %= 8    
