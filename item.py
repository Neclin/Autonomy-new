import pygame

from renderer import Renderer
mainCamera = Renderer.mainCamera

class Item():
    def __init__(self, distance=0, next=None, prev=None):
        self.distance = distance
        self.distanceToEnd = 0
        self.position = None
        self.next = next
        self.prev = prev
        self.size = pygame.Vector2(0.25, 0.25)

    def draw(self, win, position):
        itemRect = mainCamera.convertWorldRectToScreen(position, self.size)
        itemRect.center = itemRect.topleft
        pygame.draw.rect(win, (255,0,0), itemRect, 1)

    def update(self, position):
        self.position = position