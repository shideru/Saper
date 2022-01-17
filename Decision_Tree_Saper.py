#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, random
from objects.Bomb import Bomb
from objects.Saper import Saper
from objects.Wall import Wall
from pygame.locals import *
from random import randint

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

Bomb_RR = pygame.image.load("images/Bomb_R.png")  # Bomb defused
Bomb_GG = pygame.image.load("images/Bomb_G.png")  # Bomb defused
Bomb_BB = pygame.image.load("images/Bomb_B.png")  # Bomb defused
Bomb_YY = pygame.image.load("images/Bomb_Y.png")  # Bomb defused
Bomb_RB = pygame.image.load("images/Bomb_RB.png")  # Bomb defused
Bomb_GB = pygame.image.load("images/Bomb_GB.png")  # Bomb defused
Bomb_YB = pygame.image.load("images/Bomb_YB.png")  # Bomb defused
Bomb_GR = pygame.image.load("images/Bomb_GR.png")  # Bomb defused
Bomb_BR = pygame.image.load("images/Bomb_BR.png")  # Bomb defused
Bomb_YR = pygame.image.load("images/Bomb_YR.png")  # Bomb defused
Bomb_RY = pygame.image.load("images/Bomb_RY.png")  # Bomb defused
Bomb_GY = pygame.image.load("images/Bomb_GY.png")  # Bomb defused
Bomb_BY = pygame.image.load("images/Bomb_BY.png")  # Bomb defused
Bomb_BG = pygame.image.load("images/Bomb_BG.png")  # Bomb defused
Bomb_YG = pygame.image.load("images/Bomb_YG.png")  # Bomb defused
Bomb_RG = pygame.image.load("images/Bomb_RG.png")  # Bomb defused

Wall_image = pygame.image.load("images/Wall.png")

# defused bomb counter
defused = 0
# Defining all the functions
# -------------------------------------------------------------------------------------------------------------------- #
# Decision tree classification and regression tree.
header = ["A", "B", "C", "cut"]
training_data = [
    ['Green', 'Green', 'Red', 'Red'],
    ['Green', 'Red', 'Green', 'Red'],
    ['Red', 'Green', 'Green', 'Red'],
    ['Red', 'Green', 'Blue', 'Red'],
    ['Green', 'Red', 'Blue', 'Red'],
    ['Blue', 'Red', 'Blue', 'Red'],
    ['Green', 'Yellow', 'Red', 'Red'],
    ['Yellow', 'Yellow', 'Red', 'Red'],
    ['Green', 'Yellow', 'Blue', 'Yellow'],
    ['Blue', 'Yellow', 'Blue', 'Yellow'],
    ['Blue', 'Blue', 'Yellow', 'Yellow'],
    ['Yellow', 'Blue', 'Blue', 'Yellow'],
    ['Yellow', 'Yellow', 'Blue', 'Blue'],
    ['Blue', 'Yellow', 'Yellow', 'Blue'],
    ['Green', 'Green', 'Yellow', 'Yellow'],
    ['Green', 'Green', 'Blue', 'Blue'],
]




def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:


    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):

    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):

    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity




def info_gain(left, right, current_uncertainty):

    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):

    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1

    for col in range(n_features):

        values = set([row[col] for row in rows])

        for val in values:

            question = Question(col, val)

            true_rows, false_rows = partition(rows, question)


            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:


    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):

    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    print (spacing + str(node.question))

    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)




def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs



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
# Building the tree
my_tree = build_tree(training_data)
print_tree(my_tree)

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
                kod = randint(0, len(training_data)-1)
                options = []
                for lbl in classify(training_data[kod], my_tree).keys():
                    options.append(lbl)
                defused = defused + saper_map[saper_x][saper_y].defuse(saper_map[saper_x_movement][saper_y_movement])
                typ = training_data[kod][-1] + " " + random.choice(options)
                print(typ)
                saper_map[saper_x_movement][saper_y_movement].type = typ
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
                    image_select = Bomb_Defused
                elif saper_map[i][j].type == "Red Red":
                    image_select = Bomb_RR
                elif saper_map[i][j].type == "Green Green":
                    image_select = Bomb_GG
                elif saper_map[i][j].type == "Yellow Yellow":
                    image_select = Bomb_YY
                elif saper_map[i][j].type == "Blue Blue":
                    image_select = Bomb_BB
                elif saper_map[i][j].type == "Blue Red":
                    image_select = Bomb_RB
                elif saper_map[i][j].type == "Blue Green":
                    image_select = Bomb_GB
                elif saper_map[i][j].type == "Blue Yellow":
                    image_select = Bomb_YB
                elif saper_map[i][j].type == "Yellow Red":
                    image_select = Bomb_RY
                elif saper_map[i][j].type == "Yellow Green":
                    image_select = Bomb_GY
                elif saper_map[i][j].type == "Yellow Blue":
                    image_select = Bomb_BY
                elif saper_map[i][j].type == "Green Red":
                    image_select = Bomb_RG
                elif saper_map[i][j].type == "Green Yellow":
                    image_select = Bomb_YG
                elif saper_map[i][j].type == "Green Blue":
                    image_select = Bomb_BG
                elif saper_map[i][j].type == "Red Blue":
                    image_select = Bomb_BR
                elif saper_map[i][j].type == "Red Green":
                    image_select = Bomb_GR
                elif saper_map[i][j].type == "Red Yellow":
                    image_select = Bomb_YR
                elif saper_map[i][j].type == "A":
                    image_select = Bomb_Image
                GAMEBOARD.blit(image_select, [i * 50, j * 50])

    # Refresh the GAMEBOARD screen
    pygame.display.flip()
