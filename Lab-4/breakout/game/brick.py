"""
Brick: a single block. Three types:

  NORMAL        - destroyed after 1 hit
  STRONG        - needs 3 hits (changes shade as it gets damaged)
  UNBREAKABLE   - can never be destroyed
"""

import math

import pygame

NORMAL = "normal"
STRONG = "strong"
UNBREAKABLE = "unbreakable"

STRONG_HITS = 3

COLOR_NORMAL = (200, 90, 90)
COLOR_UNBREAKABLE = (125, 125, 135)
# Strong brick shade by hits remaining: darker = healthier.
COLOR_STRONG = {
    3: (60, 100, 210),
    2: (100, 145, 235),
    1: (165, 190, 245),
}


class Brick:
    def __init__(self, x, y, width, height, kind=NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.kind = kind
        if kind == STRONG:
            self.hits_remaining = STRONG_HITS
        elif kind == UNBREAKABLE:
            self.hits_remaining = math.inf
        else:
            self.hits_remaining = 1

    @property
    def breakable(self):
        return self.kind != UNBREAKABLE

    @property
    def color(self):
        if self.kind == UNBREAKABLE:
            return COLOR_UNBREAKABLE
        if self.kind == STRONG:
            return COLOR_STRONG[max(1, min(STRONG_HITS, self.hits_remaining))]
        return COLOR_NORMAL

    def hit(self):
        """Register one hit. Returns True if the brick is now destroyed."""
        if not self.breakable:
            return False
        self.hits_remaining -= 1
        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
