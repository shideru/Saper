#!/usr/bin/python
# -*- coding: utf-8 -*-


import pygame
import sys
import os
import random
from random import randint
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
        if Grid[x][y].type == "Done":
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
read_map("map2.txt")

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



# set up the window
GAMEBOARD = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Saper')

background_image = pygame.image.load("images/background.png")

prv_out_bk_1 = 0
prv_out_bk_2 = 0

counter = 0

flag1 = True
flag2 = False

my_tree = build_tree(training_data)

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
            if saper_map[saper_x_movement][saper_y_movement].type == "A":
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

    # Refresh Screen
    pygame.display.flip()

    fpsClock.tick(FPS)
