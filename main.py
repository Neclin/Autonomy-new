import pygame
import time

from renderer import Renderer 
from path import Path
from settings import FPS

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        
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
    
    

newPath = Path()
newPath.addPoint(0, 0)
newPath.addPoint(1, 1)
newPath.addPoint(1, 0)
newPath.addPoint(3, 2)
newPath.addItem(0.50)
newPath.addItem(0.50)
newPath.addItem(0)
Renderer.objectToDraw.append(newPath)

frame1 = time.time()
deltaTime = 0
while True:
    # Constantly executing code goes here
    checkEvents()

    frame2 = time.time()
    if frame2 - frame1 >= 1/FPS:
        deltaTime = frame2 - frame1
        frame1 = frame2
        # Frame based code goes here
        checkKeys(deltaTime)
        newPath.updateItems(deltaTime)
        Renderer.drawToScreen()
    
