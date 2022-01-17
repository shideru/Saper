#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, random
from objects.Bomb import Bomb
from objects.Saper import Saper
from objects.Wall import Wall
from pygame.locals import *

# Defining the program environment
# list containing the map of the game
saper_map = []

# Define the Frames Per Second setting
FPS = 30
fpsClock = pygame.time.Clock()

# Define window size for the environment to run in
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Define saper coordinates - Those are just arbitrary, the map will decide position
saper_x = 0
saper_y = 0

# Define the coordinates of the saper movement
saper_x_movement = 0
saper_y_movement = 0

# List containing the coordinates of the bombs on the map
dest = []

# List containing the bomb priority and their respective coordinates from the 'dest' list
priority = []

# List containing the Path to follow found by the A star algorithm
Solution_A = []


# List of used graphics
Saper_A_image = pygame.image.load("images/saper_A.png")

Bomb_Image = pygame.image.load("images/Bomb.png")  # Instead of Bomb_A

Bomb_Defused = pygame.image.load("images/Bomb_Defused.png")  # Instead of thumbs up

Wall_image = pygame.image.load("images/Wall.png")

# defused bomb counter
defused = 0

# Defining all the functions
# -------------------------------------------------------------------------------------------------------------------- #
# Procedure used to calculate the cost by returning the distance from our point to the target point
def heuristic_function_cost(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def A_star_pf(Grid, start, dest, priority):  #A_star(map, [x, y], dest, priority)
    Closed_set = []
    Open_set = [start]
    Saper_came_from = []
    g_Score = []
    f_Score = []
    Grid2 = []
    goal = dest[priority.index(min(priority))]
    dest.pop(priority.index(min(priority)))
    priority.pop(priority.index(min(priority)))

    for i in range(len(Grid)):
        g_Score.append([])
        f_Score.append([])
        Saper_came_from.append([])
        Grid2.append([])
        for j in range(len(Grid[i])):
            g_Score[i].append(1000)
            f_Score[i].append(1000)
            Saper_came_from[i].append([i, j])
            if Grid[i][j] is None or Grid[i][j].__class__.__name__ == "Saper" or (i == goal[0] and j == goal[1]):
                Grid2[i].append(None)
            else:
                Grid2[i].append(Wall())

    g_Score[start[0]][start[1]] = 0
    f_Score[start[0]][start[1]] = heuristic_function_cost(start, goal)
    flag3 = True
    while (len(Open_set) > 0) and flag3:
        current = Open_set[0]
        current_id = 0
        for l in range(len(Open_set)):
            if f_Score[Open_set[l][0]][Open_set[l][1]] < f_Score[current[0]][current[1]]:
                current = Open_set[l]
                current_id = l

        if current[0] == goal[0] and current[1] == goal[1]:
            flag3 = False

        Open_set.pop(current_id)
        Closed_set.append(current)

        for k in range(4):
            flag2 = False
            if k == 0 and Grid2[current[0] + 1][current[1]].__class__.__name__ != "Wall":
                neighbor = [current[0] + 1, current[1]]
                flag2 = True
            if k == 1 and Grid2[current[0] - 1][current[1]].__class__.__name__ != "Wall":
                flag2 = True
                neighbor = [current[0] - 1, current[1]]
            if k == 2 and Grid2[current[0]][current[1] + 1].__class__.__name__ != "Wall":
                flag2 = True
                neighbor = [current[0], current[1] + 1]
            if k == 3 and Grid2[current[0]][current[1] - 1].__class__.__name__ != "Wall":
                flag2 = True
                neighbor = [current[0], current[1] - 1]

            if flag2:
                flag1 = True
                for l in range(len(Closed_set)):
                    if Closed_set[l][0] == neighbor[0] and Closed_set[l][1] == neighbor[1]:
                        flag1 = False

            if flag2 and flag1:
                for l in range(len(Closed_set)):
                    if Closed_set[l][0] == neighbor[0] and Closed_set[l][1] == neighbor[1]:
                        flag2 = False
                if flag2:
                    flag1 = True
                    poss_g_Score = g_Score[current[0]][current[1]] + 1

                    for l in range(len(Open_set)):
                        if Open_set[l][0] == neighbor[0] and Open_set[l][1] == neighbor[1]:
                            flag1 = False
                    if flag1:
                        Open_set.append(neighbor)
                    elif poss_g_Score >= g_Score[neighbor[0]][neighbor[1]]:
                        continue

                    Saper_came_from[neighbor[0]][neighbor[1]] = [current[0], current[1]]
                    g_Score[neighbor[0]][neighbor[1]] = poss_g_Score
                    f_Score[neighbor[0]][neighbor[1]] = g_Score[neighbor[0]][neighbor[1]] + heuristic_function_cost(neighbor, goal)
    Path = []
    temp0 = goal[0]
    temp1 = goal[1]
    Path.append([temp0, temp1])
    while not (temp0 == start[0] and temp1 == start[1]):
        Path.append([Saper_came_from[temp0][temp1][0], Saper_came_from[temp0][temp1][1]])
        help1 = temp0
        help2 = temp1
        temp0 = Saper_came_from[help1][help2][0]
        temp1 = Saper_came_from[help1][help2][1]

    for i in range(len(Path) - 1, 0, -1):
        if Path[i][0] + 1 == Path[i - 1][0] and Path[i][1] == Path[i - 1][1]:
            Solution_A.append("R")
        elif Path[i][0] - 1 == Path[i - 1][0] and Path[i][1] == Path[i - 1][1]:
            Solution_A.append("L")
        elif Path[i][0] == Path[i - 1][0] and Path[i][1] + 1 == Path[i - 1][1]:
            Solution_A.append("D")
        elif Path[i][0] == Path[i - 1][0] and Path[i][1] - 1 == Path[i - 1][1]:
            Solution_A.append("U")

    if len(dest) > 0:
        A_star_pf(Grid, Saper_came_from[goal[0]][goal[1]], dest, priority)


# -------------------------------------------------------------------------------------------------------------------- #
# Procedure translating an encoded map from a file to a usable format and adding it to the list of maps
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
            saper_map[index].append(Bomb(random.randint(200, 600), "A"))
        if s[i] == "\n":
            saper_map.append([])
            index = index + 1


# Initialize all the required pygame modules
pygame.init()

# Call the translating function for the specified map
read_map("map2.txt")

# Procedure finding the saper coordinates on the translated map and assigning them to the objects XY coordinates
for i in range(len(saper_map)):
    for j in range(len(saper_map[i])):
        if saper_map[i][j].__class__.__name__ == "Saper":
            saper_x = i
            saper_y = j


# Procedure finding the bomb coordinates and the bomb priority
# and appending them respectively to the 'dest' list and 'priority' list
for i in range(len(saper_map)):
    for j in range(len(saper_map[i])):
        if saper_map[i][j].__class__.__name__ == "Bomb":
            dest.append([i, j])
            priority.append(saper_map[i][j].priority)

# Execution of the A star algorithm on the given map
A_star_pf(saper_map, [saper_x, saper_y], dest, priority)

# Set up the graphic environment of the program
GAMEBOARD = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
# set_mode((size_width, size height), flags, depth)

# Set the window name
pygame.display.set_caption('Autonomiczny Saper')

# Set the background image
background_image = pygame.image.load("images/background.png")

# Set up the flag to check if the saper is done clearing the bombs
saper_done_flag = True

# Control variable for movement operations
game_loop = 0

# Set up the main movement loop and action loop
while True:
# -------------------------------------------------------------------------------------------------------------------- #
    if game_loop >= len(Solution_A) and saper_done_flag:
        saper_done_flag = False
# -------------------------------------------------------------------------------------------------------------------- #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
# -------------------------------------------------------------------------------------------------------------------- #
    if saper_done_flag:
        if Solution_A[game_loop] == "R":
            if saper_x < len(saper_map) - 1:
                saper_x_movement = saper_x + 1
                saper_y_movement = saper_y

        elif Solution_A[game_loop] == "L":
            if saper_x > 0:
                saper_x_movement = saper_x - 1
                saper_y_movement = saper_y

        elif Solution_A[game_loop] == "D":
            if saper_y < len(saper_map[0]) - 1:
                saper_y_movement = saper_y + 1
                saper_x_movement = saper_x

        elif Solution_A[game_loop] == "U":
            if saper_y > 0:
                saper_y_movement = saper_y - 1
                saper_x_movement = saper_x

        game_loop = game_loop + 1

        if saper_x_movement != saper_x or saper_y_movement != saper_y:
            if saper_map[saper_x_movement][saper_y_movement] is None:
                saper_map[saper_x_movement][saper_y_movement] = saper_map[saper_x][saper_y]
                saper_map[saper_x][saper_y] = None
                saper_x = saper_x_movement
                saper_y = saper_y_movement

            elif saper_map[saper_x_movement][saper_y_movement].__class__.__name__ == "Bomb":
                defused = defused + saper_map[saper_x][saper_y].defuse(saper_map[saper_x_movement][saper_y_movement])
                saper_x_movement = saper_x
                saper_y_movement = saper_y
# -------------------------------------------------------------------------------------------------------------------- #
    GAMEBOARD.blit(background_image, (0, 0))
    for i in range(len(saper_map)):
        for j in range(len(saper_map[i])):
            if saper_map[i][j].__class__.__name__ == "Saper":
                if saper_map[i][j].tool == "A":
                    GAMEBOARD.blit(Saper_A_image, [i*50, j*50])

            elif saper_map[i][j].__class__.__name__ == "Wall":
                GAMEBOARD.blit(Wall_image, [i*50, j*50])

            elif saper_map[i][j].__class__.__name__ == "Bomb":
                if saper_map[i][j].type == "done":
                    GAMEBOARD.blit(Bomb_Defused, [i*50, j*50])

                elif saper_map[i][j].type == "A":
                    GAMEBOARD.blit(Bomb_Image, [i*50, j*50])

    # Refresh the GAMEBOARD screen
    pygame.display.flip()
