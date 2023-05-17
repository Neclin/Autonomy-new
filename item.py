import pygame

class Item():
    def __init__(self, distance=0, next=None, prev=None):
        self.distance = distance
        self.distanceToEnd = 0
        self.position = None
        self.next = next
        self.prev = prev
        self.size = pygame.Vector2(0.25, 0.25)

    def draw(self, renderer, position):
        itemRect = renderer.convertWorldRectToScreen(position, self.size)
        itemRect.center = itemRect.topleft
        pygame.draw.rect(renderer.win, (255,0,0), itemRect, 1)

    def update(self, position):
        self.position = position