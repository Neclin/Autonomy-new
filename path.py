import pygame

from renderer import Renderer
mainCamera = Renderer.mainCamera

from listElement import PathPoint
from item import Item

class Path:
    def __init__(self):
        self.pointsHead = None
        self.tail = None
        self.pathLength = 0

        self.lastItem = None
        self.firstItem = None

        self.speed = 1

    def addPoint(self, x, y):
        if self.pointsHead == None:
            self.pointsHead = PathPoint(pygame.Vector2(x,y))
            self.tail = self.pointsHead
            return
        
        self.tail.next = PathPoint(pygame.Vector2(x,y))
        distanceToLastPoint = (self.tail.next.value - self.tail.value).length()
        self.tail.next.distance = self.tail.distance + distanceToLastPoint
        self.pathLength += distanceToLastPoint
        self.tail = self.tail.next
    
    def addItem(self, distance=0):
        if self.lastItem == None:
            self.lastItem = Item(distance)
            self.firstItem = self.lastItem
            return
        else:
            self.lastItem.next = Item(distance)
            self.lastItem.next.prev = self.lastItem
            self.lastItem = self.lastItem.next

    def printItems(self):
        currentItem = self.lastItem
        while currentItem != None:
            print(currentItem.position)
            currentItem = currentItem.next
    
    def draw(self, win):
        currentPoint = self.pointsHead
        while currentPoint.next != None:
            point1 = mainCamera.convertWorldToScreen(currentPoint.value)
            point2 = mainCamera.convertWorldToScreen(currentPoint.next.value)
            pygame.draw.line(win, (255,255,255), point1, point2, 1)
            currentPoint = currentPoint.next

        cumulativeDistance = 0
        currentItem = self.lastItem
        while currentItem != None:
            cumulativeDistance += currentItem.distance
            currentItem.draw(win, self.getPositionAtDistance(cumulativeDistance))
            currentItem = currentItem.next
    
    def getPositionAtDistance(self, distance):
        currentPoint = self.pointsHead
        while currentPoint.next != None:
            if distance >= currentPoint.distance and distance < currentPoint.next.distance:
                distanceRatio = (distance - currentPoint.distance) / (currentPoint.next.distance - currentPoint.distance)
                return currentPoint.value + (currentPoint.next.value - currentPoint.value) * distanceRatio
            currentPoint = currentPoint.next
        return currentPoint.value

    def updateItems(self, deltaTime):
        pass