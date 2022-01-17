#!/usr/bin/python
# -*- coding: utf-8 -*-


import pygame, sys, random
from objects.Bomb import Bomb
from objects.Saper import Saper
from objects.Wall import Wall
from pygame.locals import *
from sklearn.datasets import load_digits
import matplotlib.pylab as pl
from sklearn import tree

# lista z ścieżką do przejścia znalezioną przez algorytm
Solution = []

# lista zawierająca mapę
map = []

def bfs_find(Grid, start, dest):
    Closed_set = []
    Open_set = [start]
    cameFrom = []
    Grid2 = []

    for i in range(len(Grid)):
        cameFrom.append([])
        Grid2.append([])
        for j in range(len(Grid[i])):
            cameFrom[i].append([i, j])
            flag = False
            for k in range(len(dest)):
                if i == dest[k][0] and j == dest[k][1]:
                    flag = True

            if Grid[i][j] is None or Grid[i][j].__class__.__name__ == "Saper" or flag:
                Grid2[i].append(None)
            else:
                Grid2[i].append(Wall())

    flag3 = True

    while(len(Open_set) > 0) and flag3:
        current = Open_set[0]

        for j in range(len(dest)):
            if current[0] == dest[j][0] and current[1] == dest[j][1]:
                flag3 = False
                goal = j
                continue

        Open_set.pop(0)
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
                for l in range(len(Closed_set)):
                    if Closed_set[l][0] == neighbor[0] and Closed_set[l][1] == neighbor[1]:
                        flag2 = False
                if flag2:
                    Open_set.append(neighbor)
                    cameFrom[neighbor[0]][neighbor[1]] = [current[0], current[1]]

    Path = []
    temp0 = dest[goal][0]
    temp1 = dest[goal][1]
    g = dest[goal]

    Path.append([temp0, temp1])
    while not(temp0 == start[0] and temp1 == start[1]):
        Path.append([cameFrom[temp0][temp1][0], cameFrom[temp0][temp1][1]])
        help1 = temp0
        help2 = temp1
        temp0 = cameFrom[help1][help2][0]
        temp1 = cameFrom[help1][help2][1]

    for i in range(len(Path)-1, 0, -1):
        if Path[i][0] + 1 == Path[i-1][0] and Path[i][1] == Path[i-1][1]:
            Solution.append("R")
        elif Path[i][0] - 1 == Path[i-1][0] and Path[i][1] == Path[i-1][1]:
            Solution.append("L")
        elif Path[i][0] == Path[i-1][0] and Path[i][1] + 1 == Path[i-1][1]:
            Solution.append("D")
        elif Path[i][0] == Path[i-1][0] and Path[i][1] - 1 == Path[i-1][1]:
            Solution.append("U")

    dest.pop(goal)

    if len(dest) > 0:
        bfs_find(Grid, cameFrom[g[0]][g[1]], dest)

# procedura wpisująca zakodowaną w pliku mapę i przerabia ją na odpowiedni format równocześnie wpisując ją na liste map
def read_map(file):
    f = open("maps/" + file, "r")
    s = f.read()
    map.append([])
    index = 0
    for i in range(len(s)-1):
        if s[i] == "0":
            map[index].append(None)
        if s[i] == "1":
            map[index].append(Wall())
        if s[i] == "2":
            map[index].append(Saper())
        if s[i] == "3":
            map[index].append(Bomb(random.randint(400, 601), "A"))
        if s[i] == "\n":
            map.append([])
            index = index + 1


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

def decode(code,counter,bomb_code):
    pl.figure()
    pl.gray()
    i=1
    r=[]
    for x in code:
        pl.subplot(1, len(code), i)
        i=i+1
        pl.matshow(digits.images[x], fignum=False)
        photo = x_dig[x].reshape(1, -1)
        r.append(str(classifier.predict(photo)))
    res = listToString(r)
    decoded = []
    for a in res:
        if a != "[" and a != "]":
            decoded.append(a)
    filename = "wyniki\ "+"bomba nr "+str(counter)+" kod odczytany "+listToString(decoded)+" kod prawdziwy "+str(listToString(bomb_code))+".png"
    pl.savefig(filename)
    pl.close()
    return decoded




pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

read_map("map3.txt")
# koordynaty Sapera (jeszcze nie przypisane)
x = 0
y = 0

# koordynaty ruchu Sapera
x_r = 0
y_r = 0

# lista zawierająca współrzędne bomb na mapie
dest = []

# znalezienie współrzędnych Sapera na danej mapie i przypisanie je do zmiennych x i y
for i in range(len(map)):
    for j in range(len(map[i])):
        if map[i][j].__class__.__name__ == "Saper":
            x = i
            y = j

# znalezienie współrzędnych bomb i priorytetów oraz wpisanie je na listy dest i prioryty
for i in range(len(map)):
    for j in range(len(map[i])):
        if map[i][j].__class__.__name__ == "Bomb":
            dest.append([i,j])

# wykonanie algorytmu bfs na danej mapie
bfs_find(map, [x, y], dest)

# licznik bomb które wybuchły
detonated = 0

# licznik rozbrojeń
defused = 0

# Grafika
Saper_A_image = pygame.image.load("images/saper_A.png")
Bomb_A_image = pygame.image.load("images/Bomb.png")
Thumbs_up_image = pygame.image.load("images/Thumbs_up.png")
Wall_image = pygame.image.load("images/Wall.png")
Hole_image = pygame.image.load("images/Hole.png")

# set up the window
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Saper')

# obraz w tle
background_image = pygame.image.load("images/background.png")

# licznik do obsługi ruchów
loop = 0

# flaga do obsługi zakończenia przechodzenia Sapera po mapie
flag = True

#uczenie
digits = load_digits()

#Define variables
n_samples = len(digits.images)
x_dig = digits.images.reshape((n_samples, -1))
y_dig = digits.target

#Create random indices
sample_index = random.sample(range(int(len(x_dig))), int(len(x_dig)/5)) #20-80
valid_index=[i for i in range(len(x_dig)) if i not in sample_index]

#Sample and validation images
sample_images=[x_dig[i] for i in sample_index]
valid_images=[x_dig[i] for i in valid_index]

#Sample and validation targets
sample_target=[y_dig[i] for i in sample_index]
valid_target=[y_dig[i] for i in valid_index]

#Using the Random Forest Classifier
classifier = tree.DecisionTreeClassifier()

#Fit model with sample data
classifier.fit(sample_images, sample_target)

#Attempt to predict validation data
score=classifier.score(valid_images, valid_target)
#tree.export_graphviz(classifier, out_file='tree.doc')
print("Dokładność uczenia: "+str(score))

#fig, axes = pl.subplots(nrows = 1, ncols = 1, figsize = (4, 4), dpi=500)
#tree.plot_tree(classifier,
#               feature_names = digits.feature_names,
#              class_names= str(digits.target_names),
#               filled = False)
#fig.savefig('tree.png')
#pl.close()

# główna pętla
bomb_counter = 1
while True:
    if loop >= len(Solution) and flag:
        flag = False
        print("Number of detonated bombs: ", detonated)
        print("Number of defused bombs: ", defused)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if flag:
        if Solution[loop] == "R":
            if x < len(map) - 1:
                x_r = x + 1
                y_r = y

        elif Solution[loop] == "L":
            if x > 0:
                x_r = x - 1
                y_r = y

        elif Solution[loop] == "D":
            if y < len(map[0]) - 1:
                y_r = y + 1
                x_r = x

        elif Solution[loop] == "U":
            if y > 0:
                y_r = y - 1
                x_r = x
        loop = loop + 1

        if x_r != x or y_r != y:
            if map[x_r][y_r] is None:
                map[x_r][y_r] = map[x][y]
                map[x][y] = None
                x = x_r
                y = y_r


            elif map[x_r][y_r].__class__.__name__ == "Bomb":
#rozbrajanie bomby
                real_code_temp=[]
                for c in map[x_r][y_r].code:
                    real_code_temp.append(digits.target[c])
                real_code = listToString(str(real_code_temp))
                bomb_code=[]
                for c in real_code:
                    if c != "[" and c != "]" and c != "," and c != " ":
                        bomb_code = bomb_code + list(c)
                decode_rez = decode(map[x_r][y_r].code, bomb_counter,bomb_code)
                defused_rez = map[x][y].defuse(map[x_r][y_r], decode_rez, bomb_code)
                if defused_rez == 1:
                    defused += 1;
                else:
                    detonated += 1;
                bomb_counter = bomb_counter+1
                x_r = x
                y_r = y

    DISPLAYSURF.blit(background_image, (0, 0))
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] is not None:
                if map[i][j].__class__.__name__ == "Saper":
                     if map[i][j].tool == "A":
                        DISPLAYSURF.blit(Saper_A_image, [i*50, j*50])

                     elif map[i][j].tool == "B":
                        DISPLAYSURF.blit(Saper_B_image, [i*50, j*50])

                     elif map[i][j].tool == "C":
                        DISPLAYSURF.blit(Saper_C_image, [i*50, j*50])

                     elif map[i][j].tool == "none":
                        DISPLAYSURF.blit(Saper_image, [i*50, j*50])

                elif map[i][j].__class__.__name__ == "Bomb":


                    if map[i][j].type == "exploded":
                        DISPLAYSURF.blit(Hole_image, [i * 50, j * 50])

                    elif map[i][j].type == "done":
                        DISPLAYSURF.blit(Thumbs_up_image, [i * 50, j * 50])

                    elif map[i][j].type == "A":
                        DISPLAYSURF.blit(Bomb_A_image, [i * 50, j * 50])

                    elif map[i][j].type == "B":
                        DISPLAYSURF.blit(Bomb_B_image, [i * 50, j * 50])

                    elif map[i][j].type == "C":
                        DISPLAYSURF.blit(Bomb_C_image, [i * 50, j * 50])
                    map[i][j].tick()

                elif map[i][j].__class__.__name__ == "Wall":
                    DISPLAYSURF.blit(Wall_image, [i * 50, j * 50])

    # Refresh Screen
    pygame.display.flip()

    fpsClock.tick(FPS)
