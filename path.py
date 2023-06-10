import pygame

from settings import CHUNK_SIZE
from world import World

from listElement import PathPoint
from item import Item

class Path:
    def __init__(self):
        self.firstPathPoint = None
        self.lastPathPoint = None
        self.pathLength = 0
        self.distanceToEnd = 0

        self.firstItem = None
        self.lastItem = None
        self.gapItem = None

        self.speed = 5

    #region Path Functions
    def addPoint(self, position):
        if self.firstPathPoint == None:
            self.firstPathPoint = PathPoint(position)
            self.lastPathPoint = self.firstPathPoint
            return
        
        distanceToLastPoint = (position - self.lastPathPoint.position).length()
        self.lastPathPoint.next = PathPoint(position)
        self.pathLength += distanceToLastPoint
        self.distanceToEnd += distanceToLastPoint
        self.lastPathPoint = self.lastPathPoint.next
        self.lastPathPoint.distance = distanceToLastPoint

    def addPath(self, path):
        pass
    
    # def removePath(self):
    #     chunkPosition = self.firstPathPoint.position//CHUNK_SIZE
    #     chunk = World.worldData.get(str(chunkPosition))
    #     if chunk:
    #         chunk.paths.remove(self)
    #     del(self)
    
    def printPathPoints(self):
        currentPoint = self.firstPathPoint
        while currentPoint != None:
            print(currentPoint.__repr__())
            currentPoint = currentPoint.next

    #endregion  
    
    def addItem(self, distance=0):
        self.distanceToEnd -= distance

        if self.firstItem == None:
            self.firstItem = Item(distance)
            self.lastItem = self.firstItem
            self.gapItem = self.lastItem
            return
        self.lastItem.next = Item(distance)
        self.lastItem.next.previous = self.lastItem
        self.lastItem = self.lastItem.next
        self.pathLength -= self.lastItem.size.x
        self.gapItem = self.lastItem

    # def printItems(self):
    #     currentItem = self.firstItem
    #     while currentItem != None:
    #         print(currentItem.distance)
    #         currentItem = currentItem.next
    
    def draw(self, renderer):
        print(self.firstItem.distance)
        currentPoint = self.firstPathPoint
        currentItem = self.firstItem
        cumulativeItemDistance = 0
        cumulativePointDistance = 0

        while currentPoint.next != None:
            # Draws the line between the two path points
            point1 = renderer.mainCamera.convertWorldToScreen(currentPoint.position)
            point2 = renderer.mainCamera.convertWorldToScreen(currentPoint.next.position)
            pygame.draw.line(renderer.win, (255,255,255), point1, point2, 1)

            cumulativePointDistance += currentPoint.next.distance

            # Move to the next set of points
            currentPoint = currentPoint.next

        #draw all the items
        while currentItem != None:
            cumulativeItemDistance += currentItem.distance
            position = self.getPositionAtDistance(cumulativeItemDistance)
            print(position)
            currentItem.draw(renderer, position)
            currentItem = currentItem.next

    def getPositionAtDistance(self, distance):
        currentPoint = self.firstPathPoint
        cumulativeDistance = 0
        while currentPoint.next != None:
            if cumulativeDistance + currentPoint.next.distance > distance:
                return currentPoint.position + (currentPoint.next.position - currentPoint.position).normalize() * (distance - cumulativeDistance)
            cumulativeDistance += currentPoint.next.distance
            currentPoint = currentPoint.next
        return currentPoint.position

        
    # def getPositionAtDistance(self, distance):
    #     currentPoint = self.firstPathPoint
    #     cumulativeDistance = 0
    #     while currentPoint.next != None:
    #         if cumulativeDistance + currentPoint.next.distance > distance:
    #             return currentPoint.position + (currentPoint.next.position - currentPoint.position).normalize() * (distance - cumulativeDistance)
    #         cumulativeDistance += currentPoint.next.distance
    #         currentPoint = currentPoint.next
    #     return currentPoint.position

        


    def updateItems(self, deltaTime):
        distanceToMove = self.speed * deltaTime
        self.distanceToEnd -= distanceToMove
        if self.firstItem.distance < self.pathLength:
            self.firstItem.distance += distanceToMove
        else:
            self.firstItem.distance = self.pathLength
        
        if self.distanceToEnd < 0 and self.gapItem != None:
            self.gapItem.distance -= distanceToMove
            print("test", self.gapItem.distance)
            if self.gapItem.distance < self.gapItem.size.x:
                self.gapItem.distance = self.gapItem.size.x
                self.gapItem = self.gapItem.prev
