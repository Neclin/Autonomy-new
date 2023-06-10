import pygame

from path import Path

testPath = Path()
testPath.addPoint(pygame.Vector2(0, 0))
testPath.addPoint(pygame.Vector2(0, 1))
testPath.addPoint(pygame.Vector2(0, 2))
testPath.addPoint(pygame.Vector2(0, 3))
testPath.addPoint(pygame.Vector2(0, 4))

testPath.printPathPoints()
