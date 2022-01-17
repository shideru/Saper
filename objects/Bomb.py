#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from pygame.locals import *


class Bomb:
    def __init__(self, priority, type):
        self.priority = priority
        self.type = type
        self.code = []
        for i in range(3):
            self.code.append(random.randint(0, 1796))

    def priority(self):
        return self.priority
