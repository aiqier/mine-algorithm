# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *
from aco import World, Map
pygame.init()
# set up the window
X = 60
Y = 40
UNIT = 20
ANT_COUNT = 50
FOOD_COUNT = 2000
DISPLAYSURF = pygame.display.set_mode((X*UNIT, Y*UNIT), 0, 32)
pygame.display.set_caption('蚁群算法')
sienna_color = (160, 82, 45)
green_color = (34, 139, 34)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
yellow_color = (255, 255, 0)
bg = green_color
pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.get_surface()
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('arial', 10)
world = World(X, Y, ANT_COUNT, FOOD_COUNT)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == K_ESCAPE:
            sys.exit()
    time_passed = clock.tick(100)
    time_passed_seconds = time_passed / 1000.0
    DISPLAYSURF.fill(bg)
    md = world.run()
    landform, ants, foods, smells = md.next()
    for x, item in enumerate(landform):
        for y, i in enumerate(item):
            if i == Map.HOME:
                pygame.draw.rect(DISPLAYSURF, sienna_color, (x, y, UNIT*2, UNIT*2))
                text1 = font1.render(str(foods[0]), True, white_color, black_color)
                screen.blit(text1, (x, y))
            elif i == Map.FOOD:
                pygame.draw.rect(DISPLAYSURF, yellow_color, ((x - 1) * UNIT, (y - 1) * UNIT, UNIT*2, UNIT*2))
                text2 = font1.render(str(foods[1]), True, white_color, black_color)
                screen.blit(text2, ((x - 1) * UNIT, (y - 1) * UNIT))
            elif i == Map.OBSTACLE:
                pygame.draw.rect(DISPLAYSURF, black_color, (x*UNIT, y*UNIT, UNIT, UNIT))
    for ant in ants:
        if ant.has_food():
            pygame.draw.circle(screen, yellow_color, (ant.x * UNIT, ant.y * UNIT), 3, 3)
        else:
            pygame.draw.circle(screen, black_color, (ant.x * UNIT, ant.y * UNIT), 3, 3)
    pygame.display.update()