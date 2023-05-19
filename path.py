import pygame

from settings import CHUNK_SIZE
from world import World

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

    def addPoint(self, position):
        if self.pointsHead == None:
            self.pointsHead = PathPoint(position)
            self.tail = self.pointsHead
            return
        
        self.tail.next = PathPoint(position)
        distanceToLastPoint = (self.tail.next.position - self.tail.position).length()
        self.tail.next.distance = distanceToLastPoint
        self.pathLength += distanceToLastPoint
        self.distanceFromEnd += distanceToLastPoint
        self.tail = self.tail.next

    def addPath(self, path):
        # Merge the two linked lists for paths
        self.tail.next = path.pointsHead
        path.pointsHead.prev = self.tail
        self.tail = path.tail

        # Transfer the item linked list
        self.lastItem = path.lastItem
        self.itemWithTheGaps = path.itemWithTheGaps
        self.mostFarItem = path.mostFarItem

        if self.lastItem != None:
            self.lastItem.distance += self.pathLength
            self.distanceFromEnd = path.distanceFromEnd
        else:
            self.distanceFromEnd += path.distanceFromEnd
        self.pathLength += path.pathLength
        path.removePath()
    
    def removePath(self):
        chunkPosition = self.pointsHead.position//CHUNK_SIZE
        chunk = World.worldData.get(str(chunkPosition))
        if chunk:
            chunk.paths.remove(self)
        del(self)
            
    
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
        cumulativeDistance = 0
        while currentPoint.next != None:
            if cumulativeDistance + currentPoint.next.distance > distance:
                return currentPoint.position + (currentPoint.next.position - currentPoint.position).normalize() * (distance - cumulativeDistance)
            cumulativeDistance += currentPoint.next.distance
            currentPoint = currentPoint.next
        return currentPoint.position


    def updateItems(self, deltaTime):
        print(self.pathLength, self.distanceFromEnd, self.itemWithTheGaps, end=" ")
        if self.lastItem != None:
            print(self.lastItem.distance, end=" ")
        print()
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
        