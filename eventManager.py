import pygame
import math

from renderer import Renderer
from world import World
from settings import FPS, CHUNK_SIZE, TILE_SIZE

from gameObject import GameObject
from Buildings.building import Building
from Buildings.belt import Belt

class EventManager:
    activePlaceable = Building
    directionVector = pygame.Vector2(1, 0)

    def checkEvents():
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
                
                if event.key == pygame.K_LEFT:
                    World.cursorSize -= 1
                    World.cursorSize = max(1, World.cursorSize)
                if event.key == pygame.K_RIGHT:
                    World.cursorSize += 1
                    World.cursorSize = min(5, World.cursorSize)


                if event.key == pygame.K_1:
                    EventManager.activePlaceable = Building
                if event.key == pygame.K_2:
                    EventManager.activePlaceable = Belt
                
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
    
    def checkMousePresses():
        mousePressed = pygame.mouse.get_pressed(3)
        if mousePressed:
            print("_________________________")
            mousePos = pygame.mouse.get_pos()
            mousePos = pygame.Vector2(mousePos[0], mousePos[1])
            worldMousePos = Renderer.mainCamera.convertScreenToWorld(mousePos)
            
            evenOffset = 0 if World.cursorSize % 2 == 1 else 0.5
            evenOffset -= World.cursorSize//2
            evenOffsetVector = pygame.Vector2(evenOffset, evenOffset)
            worldMousePos += evenOffsetVector

            snappedMousePosition = worldMousePos//1

            if mousePressed[0]:
                newGameObject = GameObject(snappedMousePosition, pygame.Vector2(World.cursorSize, World.cursorSize))
                if World.addGameObject(newGameObject):
                    print("Placed")
                # else:
                #     print("Can't place")
                # if EventManager.activePlaceable == Building:
                #     newBuilding = EventManager.activePlaceable(snappedMousePosition, pygame.Vector2(1, 1))
                # elif EventManager.activePlaceable == Belt:
                #     # newBuilding = activePlaceable(snappedMousePosition, pygame.Vector2(1, 1), Renderer.mainCamera.mouseDirection, Renderer.mainCamera.mouseDirection)
                #     newBuilding = EventManager.activePlaceable(snappedMousePosition, pygame.Vector2(1, 1), EventManager.directionVector, EventManager.directionVector)
                # newBuilding.place()
            if mousePressed[2]:
                World.removeGameObject(snappedMousePosition)