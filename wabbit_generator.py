#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pygame, sys, os, random, time
from objects.Bomb import Bomb
from objects.Saper import Saper
from objects.Wall import Wall
from pygame.locals import *

Solution_A = []
saper_map = []


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

# #################################################################################################################


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


def get_saper_surrounding(Grid, x, y):
    s = ""
    s = s + " | 1x1:." + check_type(Grid, x - 2, y - 2) + " 1x2:." + check_type(Grid, x - 2, y - 1)
    s = s + " 1x3:." + check_type(Grid, x - 2, y) + " 1x4:." + check_type(Grid, x - 2, y + 1)
    s = s + " 1x5:." + check_type(Grid, x - 2, y + 2)

    s = s + " 2x1:." + check_type(Grid, x - 1, y - 2) + " 2x2:." + check_type(Grid, x - 1, y - 1)
    s = s + " 2x3:." + check_type(Grid, x - 1, y) + " 2x4:." + check_type(Grid, x - 1, y + 1)
    s = s + " 2x5:." + check_type(Grid, x - 1, y + 2)

    s = s + " 3x1:." + check_type(Grid, x, y - 2) + " 3x2:." + check_type(Grid, x, y - 1)
    s = s + " 3x4:." + check_type(Grid, x, y + 1) + " 3x5:." + check_type(Grid, x, y + 2)

    s = s + " 4x1:." + check_type(Grid, x + 1, y - 2) + " 4x2:." + check_type(Grid, x + 1, y - 1)
    s = s + " 4x3:." + check_type(Grid, x + 1, y) + " 4x4:." + check_type(Grid, x + 1, y + 1)
    s = s + " 4x5:." + check_type(Grid, x + 1, y + 2)

    s = s + " 5x1:." + check_type(Grid, x + 2, y - 2) + " 5x2:." + check_type(Grid, x + 2, y - 1)
    s = s + " 5x3:." + check_type(Grid, x + 2, y) + " 5x4:." + check_type(Grid, x + 2, y + 1)
    s = s + " 5x5:." + check_type(Grid, x + 2, y + 2)
    return s


def write_to_file(file, string):
    f = open(file, "a")
    f.write(string)
    f.write("\n")
    f.close()


maps = (os.popen("ls maps").read()).split("\n")

saper_x = 0
saper_y = 0
saper_x_movement = 0
saper_y_movement = 0
game_loop = 0
map_counter = 1
wabbit_loop_counter = 0
flag = True

while True:
    if game_loop >= len(Solution_A):
        game_loop = 0
        saper_map = []
        read_map(maps[map_counter])
        dest = []
        priority = []
        for i in range(len(saper_map)):
            for j in range(len(saper_map[i])):
                if saper_map[i][j].__class__.__name__ == "Saper":
                    saper_x = i
                    saper_y = j

        for i in range(len(saper_map)):
            for j in range(len(saper_map[i])):
                if saper_map[i][j].__class__.__name__ == "Bomb":
                    dest.append([i, j])
                    priority.append(heuristic_function_cost([saper_x, saper_y], [i, j]))

        A_star_pf(saper_map, [saper_x, saper_y], dest, priority)

        if map_counter >= len(maps)-2:
            wabbit_loop_counter = wabbit_loop_counter + 1
            print("wabbit loop counter: " + str(wabbit_loop_counter))
#            print("map counter: " + str(map_counter))
            map_counter = 0
        else:
            map_counter = map_counter + 1
            print("map counter: " + str(map_counter))
        if wabbit_loop_counter > 100:
            os.popen("vw wabbit_examples -f wabbit_model")
            time.sleep(5)
            sys.exit()

    s = ""
    if Solution_A[game_loop] == "R":
        if saper_x < len(saper_map)-1:
            saper_x_movement = saper_x + 1
            saper_y_movement = saper_y
            s = "1"

    elif Solution_A[game_loop] == "L":
        if saper_x > 0:
            saper_x_movement = saper_x - 1
            saper_y_movement = saper_y
            s = "3"

    elif Solution_A[game_loop] == "D":
        if saper_y < len(saper_map[0])-1:
            saper_y_movement = saper_y + 1
            saper_x_movement = saper_x
            s = "2"

    elif Solution_A[game_loop] == "U":
        if saper_y > 0:
            saper_y_movement = saper_y - 1
            saper_x_movement = saper_x
            s = "4"

    s = s + get_saper_surrounding(saper_map, saper_x, saper_y)
    write_to_file("wabbit_examples", s)
    game_loop = game_loop + 1

    if saper_x_movement != saper_x or saper_y_movement != saper_y:
        if saper_map[saper_x_movement][saper_y_movement] is None:
            saper_map[saper_x_movement][saper_y_movement] = saper_map[saper_x][saper_y]
            saper_map[saper_x][saper_y] = None
            saper_x = saper_x_movement
            saper_y = saper_y_movement

        elif saper_map[saper_x_movement][saper_y_movement].__class__.__name__ == "Bomb":
            saper_map[saper_x][saper_y].defuse(saper_map[saper_x_movement][saper_y_movement])
            saper_x_movement = saper_x
            saper_y_movement = saper_y

#    for i in range(len(saper_map)):
#      for j in range(len(saper_map[i])):
#           if saper_map[i][j].__class__.__name__ == "Bomb":
#                if saper_map[i][j].time == 0 and saper_map[i][j] != "exploded":
#                    saper_map[i][j].type = "exploded"
#                saper_map[i][j].tick()
