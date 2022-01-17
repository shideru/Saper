#!/usr/bin/python
# -*- coding: utf-8 -*-


import pygame
import sys
import os
import random
from objects.Bomb import Bomb
from objects.Saper import Saper
from objects.Wall import Wall
from pygame.locals import *


def check_type(Grid, x, y):
    if x < 0 or x > len(Grid)-1 or y < 0 or y > len(Grid[0])-1:
        return str(0)
    if Grid[x][y] is None:
        return str(10)
    if Grid[x][y].__class__.__name__ == "Wall":
        return str(1)
    if Grid[x][y].__class__.__name__ == "Bomb":
        if Grid[x][y].type == "done":
            return str(5)
        else:
            return str(50)


def saper_get_surrounding(grid, x, y):
    s = ""
    s = s + " | 1x1:." + check_type(grid, x - 2, y - 2) + " 1x2:." + check_type(grid, x - 2, y - 1)
    s = s + " 1x3:." + check_type(grid, x - 2, y) + " 1x4:." + check_type(grid, x - 2, y + 1)
    s = s + " 1x5:." + check_type(grid, x - 2, y + 2)

    s = s + " 2x1:." + check_type(grid, x - 1, y - 2) + " 2x2:." + check_type(grid, x - 1, y - 1)
    s = s + " 2x3:." + check_type(grid, x - 1, y) + " 2x4:." + check_type(grid, x - 1, y + 1)
    s = s + " 2x5:." + check_type(grid, x - 1, y + 2)

    s = s + " 3x1:." + check_type(grid, x, y - 2) + " 3x2:." + check_type(grid, x, y - 1)
    s = s + " 3x4:." + check_type(grid, x, y + 1) + " 3x5:." + check_type(grid, x, y + 2)

    s = s + " 4x1:." + check_type(grid, x + 1, y - 2) + " 4x2:." + check_type(grid, x + 1, y - 1)
    s = s + " 4x3:." + check_type(grid, x + 1, y) + " 4x4:." + check_type(grid, x + 1, y + 1)
    s = s + " 4x5:." + check_type(grid, x + 1, y + 2)

    s = s + " 5x1:." + check_type(grid, x + 2, y - 2) + " 5x2:." + check_type(grid, x + 2, y - 1)
    s = s + " 5x3:." + check_type(grid, x + 2, y) + " 5x4:." + check_type(grid, x + 2, y + 1)
    s = s + " 5x5:." + check_type(grid, x + 2, y + 2)
    return s


def write_to_file(file, string):
    f = open(file, "w")
    f.write(string)
    f.write("\n")
    f.close()


def read_map(file):
    f = open("maps/" + file, "r")
    s = f.read()
    saper_map.append([])
    index = 0
    for i in range(len(s)-1):
        if s[i] == "0":
            saper_map[index].append(None)
        if s[i] == "1":
            saper_map[index].append(Wall())
        if s[i] == "2":
            saper_map[index].append(Saper())
        if s[i] == "3":
            saper_map[index].append(Bomb(random.randint(400, 601), "A"))
        if s[i] == "\n":
            saper_map.append([])
            index = index + 1


pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

saper_map = []
read_map("map1.txt")

saper_x = 0
saper_y = 0
saper_x_movement = 0
saper_y_movement = 0

for i in range(len(saper_map)):
    for j in range(len(saper_map[i])):
        if saper_map[i][j].__class__.__name__ == "Saper":
            saper_x = i
            saper_y = j

defused = 0

# List of used graphics
Saper_A_image = pygame.image.load("images/saper_A.png")
Bomb_Image = pygame.image.load("images/Bomb.png")  # Instead of Bomb_A
Bomb_Defused = pygame.image.load("images/Bomb_Defused.png")  # Instead of thumbs up
Wall_image = pygame.image.load("images/Wall.png")

# set up the window
GAMEBOARD = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Saper')

background_image = pygame.image.load("images/background.png")

prv_out_bk_1 = 0
prv_out_bk_2 = 0

counter = 0

flag1 = True
flag2 = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    s = saper_get_surrounding(saper_map, saper_x, saper_y)
    write_to_file("wabbit_move", s)
    output = float(os.popen("vw -i wabbit_model wabbit_move -p /dev/stdout --quiet").read())
    print(output)

    if prv_out_bk_1 == output or prv_out_bk_2 == output:
        counter = counter + 1

    if counter > 21:
        counter = 0
        output = random.randint(0, 5)

    prv_out_bk_2 = prv_out_bk_1
    prv_out_bk_1 = output

    if output < 1.5:
        if saper_x < len(saper_map)-1:
            saper_x_movement = saper_x + 1
            saper_y_movement = saper_y

    elif output < 2.5:
        if saper_x > 0:
            saper_x_movement = saper_x - 1
            saper_y_movement = saper_y

    elif output < 3.5:
        if saper_y < len(saper_map[0])-1:
            saper_y_movement = saper_y + 1
            saper_x_movement = saper_x
    else:
        if saper_y > 0:
            saper_y_movement = saper_y - 1
            saper_x_movement = saper_x

    if saper_x_movement != saper_x or saper_y_movement != saper_y:
        if saper_map[saper_x_movement][saper_y_movement] is None:
            saper_map[saper_x_movement][saper_y_movement] = saper_map[saper_x][saper_y]
            saper_map[saper_x][saper_y] = None
            saper_x = saper_x_movement
            saper_y = saper_y_movement

        elif saper_map[saper_x_movement][saper_y_movement].__class__.__name__ == "Tools":
            saper_map[saper_x][saper_y].change_tool(saper_map[saper_x_movement][saper_y_movement])
            saper_x_movement = saper_x
            saper_y_movement = saper_y

        elif saper_map[saper_x_movement][saper_y_movement].__class__.__name__ == "Bomb":
            defused = defused + saper_map[saper_x][saper_y].defuse(saper_map[saper_x_movement][saper_y_movement])
            saper_x_movement = saper_x
            saper_y_movement = saper_y

    GAMEBOARD.blit(background_image, (0, 0))
    for i in range(len(saper_map)):
        for j in range(len(saper_map[i])):
            if saper_map[i][j].__class__.__name__ == "Saper":
                if saper_map[i][j].tool == "A":
                    GAMEBOARD.blit(Saper_A_image, [i * 50, j * 50])

            elif saper_map[i][j].__class__.__name__ == "Wall":
                GAMEBOARD.blit(Wall_image, [i * 50, j * 50])

            elif saper_map[i][j].__class__.__name__ == "Bomb":
                if saper_map[i][j].type == "done":
                    GAMEBOARD.blit(Bomb_Defused, [i * 50, j * 50])

                elif saper_map[i][j].type == "A":
                    GAMEBOARD.blit(Bomb_Image, [i * 50, j * 50])

    # Refresh Screen
    pygame.display.flip()

    fpsClock.tick(FPS)
