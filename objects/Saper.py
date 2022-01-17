#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from objects.Bomb import Bomb
from pygame.locals import *


class Saper():
    def __init__(self):
        self.tool = "A"

    def defuse(self, bomb):
        bomb.type = "done"
        return 1
