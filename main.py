import pygame
import time
import math

from renderer import Renderer 
from eventManager import EventManager
from world import World
from path import Path
from settings import FPS, CHUNK_SIZE

from Buildings.building import Building
from Buildings.belt import Belt
    
def quadraticBezier(p0, p1, p2, t):
    return (1-t)**2 * p0 + 2*(1-t)*t*p1 + t**2 * p2

Buildings = {"Building": Building,
             "Belt": Belt}

startLoading = time.time()
World.loadAllChunks(Buildings)
print(f"Loading took {time.time() - startLoading} seconds")

# newPath = Path()
# newPath.addPoint(pygame.Vector2(1, 1))
# newPath.addPoint(pygame.Vector2(2, 1))
# newPath.addPoint(pygame.Vector2(3, 1))
# newPath.addPoint(pygame.Vector2(4, 2))
# newPath.addPoint(pygame.Vector2(3, 2))
# newPath.addPoint(pygame.Vector2(2, 6))
# World.addPath(newPath)
# newPath.addItem(0.3)
# newPath.addItem(0.5)
# newPath.addItem(0.3)

# newPath.printPathPoints()

frame1 = time.time()
tick = 0
animationFrame = 0
deltaTime = 0
while True:
    # Constantly executing code goes here
    EventManager.checkEvents()
    EventManager.checkMousePresses()

    frame2 = time.time()
    if frame2 - frame1 >= 1/FPS:
        #print("FPS: ", 1/deltaTime) if deltaTime != 0 else None
        #print(len(World.worldData))
        deltaTime = frame2 - frame1
        frame1 = frame2
        # Frame based code goes here  
        EventManager.checkKeys(deltaTime)

        Renderer.drawToScreen(deltaTime)

        tick += 1

        if tick % 2 == 0:
            Renderer.animationFrame += 1
            Renderer.animationFrame %= 8    
