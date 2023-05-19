import pygame

from listElement import PathPoint
from item import Item

class Path:
    def __init__(self):
        self.pointsHead = None
        self.tail = None
        self.pathLength = 0

        self.lastItem = None
        self.mostFarItem = None

        self.itemWithTheGaps = None
        
        self.distanceFromStart = 0
        self.distanceFromEnd = 0

        self.speed = 5

    def addPoint(self, x, y):
        if self.pointsHead == None:
            self.pointsHead = PathPoint(pygame.Vector2(x,y))
            self.tail = self.pointsHead
            return
        
        self.tail.next = PathPoint(pygame.Vector2(x,y))
        distanceToLastPoint = (self.tail.next.position - self.tail.position).length()
        self.tail.next.distance = self.tail.distance + distanceToLastPoint
        self.pathLength += distanceToLastPoint
        self.distanceFromEnd += distanceToLastPoint
        self.tail = self.tail.next

    def addPath(self, path):
        self.tail.next = path.pointsHead
        self.pathLength += path.pathLength
        self.distanceFromEnd += path.pathLength
        del(path)
    
    def addItem(self, distance=0):
        if self.lastItem == None:
            self.lastItem = Item(distance)
            self.mostFarItem = self.lastItem
            self.itemWithTheGaps = self.lastItem
        else:
            newItem = Item(distance)
            newItem.next = self.lastItem
            self.lastItem.prev = newItem
            self.lastItem = newItem

        self.distanceFromEnd -= distance

    def printItems(self):
        currentItem = self.lastItem
        while currentItem != None:
            print(currentItem.distance)
            currentItem = currentItem.next
    
    def draw(self, renderer):
        currentPoint = self.pointsHead
        while currentPoint.next != None:
            point1 = renderer.mainCamera.convertWorldToScreen(currentPoint.position)
            point2 = renderer.mainCamera.convertWorldToScreen(currentPoint.next.position)
            pygame.draw.line(renderer.win, (255,255,255), point1, point2, 1)
            currentPoint = currentPoint.next

        cumulativeDistance = 0
        currentItem = self.lastItem
        while currentItem != None:
            cumulativeDistance += currentItem.distance
            currentItem.draw(renderer, self.getPositionAtDistance(cumulativeDistance))
            currentItem = currentItem.next
    
    def getPositionAtDistance(self, distance):
        currentPoint = self.pointsHead
        while currentPoint.next != None:
            if distance >= currentPoint.distance and distance < currentPoint.next.distance:
                distanceRatio = (distance - currentPoint.distance) / (currentPoint.next.distance - currentPoint.distance)
                return currentPoint.position + (currentPoint.next.position - currentPoint.position) * distanceRatio
            currentPoint = currentPoint.next
        return currentPoint.position

    def updateItems(self, deltaTime):
        if self.itemWithTheGaps == self.lastItem and self.distanceFromEnd == 0:
            return
        if self.lastItem == None:
            return
        amountToMove = deltaTime * self.speed
        if self.distanceFromEnd > 0:
            self.lastItem.distance += amountToMove
            self.distanceFromEnd -= amountToMove
            if self.distanceFromEnd < 0:
                self.lastItem.distance += self.distanceFromEnd
                self.distanceFromEnd = 0
        else:
            self.itemWithTheGaps.distance -= amountToMove
            if self.itemWithTheGaps.distance < 0.25:
                amountToMoveNextItem = -self.itemWithTheGaps.distance + 0.25
                self.itemWithTheGaps.distance = 0.25
                self.itemWithTheGaps = self.itemWithTheGaps.prev
                self.itemWithTheGaps.distance -= amountToMoveNextItem

            self.lastItem.distance += amountToMove
        